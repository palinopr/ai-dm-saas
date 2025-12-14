"""Instagram service with business logic for webhook handling."""
import hashlib
import hmac
import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai_agent import service as ai_agent_service
from src.ai_agent.exceptions import AgentProcessingError
from src.ai_agent.schemas import ProcessMessageRequest
from src.config import settings
from src.instagram.client import InstagramClient
from src.instagram.exceptions import SignatureVerificationError, WebhookVerificationError
from src.instagram.schemas import InstagramMessaging, InstagramWebhookPayload
from src.models.conversation import Conversation
from src.models.instagram_account import InstagramAccount
from src.models.instagram_user import InstagramUser
from src.models.message import Message, MessageDirection, MessageType

logger = logging.getLogger(__name__)


def verify_webhook_challenge(
    mode: str,
    verify_token: str,
    challenge: str,
) -> str:
    """
    Verify the webhook subscription challenge from Meta.

    Args:
        mode: The hub.mode parameter (should be "subscribe")
        verify_token: The hub.verify_token parameter
        challenge: The hub.challenge parameter to return if valid

    Returns:
        The challenge string if verification succeeds

    Raises:
        WebhookVerificationError: If mode or token is invalid
    """
    if mode != "subscribe":
        logger.warning(f"Invalid webhook mode: {mode}")
        raise WebhookVerificationError(f"Invalid mode: {mode}")

    if verify_token != settings.instagram_verify_token:
        logger.warning("Invalid verify token received")
        raise WebhookVerificationError("Invalid verify token")

    logger.info("Webhook verification successful")
    return challenge


def verify_signature(payload: bytes, signature_header: str) -> None:
    """
    Verify the HMAC-SHA256 signature of the webhook payload.

    Args:
        payload: The raw request body bytes
        signature_header: The X-Hub-Signature-256 header value

    Raises:
        SignatureVerificationError: If signature is missing, malformed, or invalid
    """
    if not signature_header:
        logger.warning("Missing X-Hub-Signature-256 header")
        raise SignatureVerificationError("Missing signature header")

    if not signature_header.startswith("sha256="):
        logger.warning(f"Malformed signature header: {signature_header[:20]}...")
        raise SignatureVerificationError("Malformed signature header")

    expected_signature = signature_header[7:]  # Remove "sha256=" prefix

    # Compute HMAC-SHA256 signature
    computed_signature = hmac.new(
        key=settings.instagram_app_secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    # Use constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(computed_signature, expected_signature):
        logger.warning("Invalid webhook signature")
        raise SignatureVerificationError("Invalid signature")

    logger.debug("Webhook signature verified successfully")


def extract_messages(payload: InstagramWebhookPayload) -> list[InstagramMessaging]:
    """
    Extract all messaging events from the webhook payload.

    Args:
        payload: The parsed webhook payload

    Returns:
        List of messaging events
    """
    messages: list[InstagramMessaging] = []

    for entry in payload.entry:
        if entry.messaging:
            messages.extend(entry.messaging)

    return messages


async def get_or_create_instagram_account(
    db: AsyncSession,
    instagram_page_id: str,
) -> InstagramAccount | None:
    """
    Get an Instagram account by page ID.

    Note: For now, we only retrieve existing accounts. In production, accounts
    would be created during the OAuth connection flow, not during webhook processing.

    Args:
        db: Database session
        instagram_page_id: The Instagram page ID (recipient ID from webhook)

    Returns:
        The InstagramAccount if found, None otherwise
    """
    query = select(InstagramAccount).where(
        InstagramAccount.instagram_page_id == instagram_page_id,
        InstagramAccount.is_active == True,  # noqa: E712
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_or_create_instagram_user(
    db: AsyncSession,
    instagram_user_id: str,
) -> InstagramUser:
    """
    Get or create an Instagram user by their Instagram user ID.

    Args:
        db: Database session
        instagram_user_id: The Instagram user ID (sender ID from webhook)

    Returns:
        The InstagramUser (existing or newly created)
    """
    query = select(InstagramUser).where(
        InstagramUser.instagram_user_id == instagram_user_id
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user:
        return user

    # Create new user
    user = InstagramUser(instagram_user_id=instagram_user_id)
    db.add(user)
    await db.flush()

    logger.info(f"Created new InstagramUser for {instagram_user_id}")
    return user


async def get_or_create_conversation(
    db: AsyncSession,
    instagram_account_id: str,
    instagram_user_id: str,
) -> Conversation:
    """
    Get or create a conversation between an Instagram account and user.

    Args:
        db: Database session
        instagram_account_id: The InstagramAccount UUID
        instagram_user_id: The InstagramUser UUID

    Returns:
        The Conversation (existing or newly created)
    """
    query = select(Conversation).where(
        Conversation.instagram_account_id == instagram_account_id,
        Conversation.instagram_user_id == instagram_user_id,
    )
    result = await db.execute(query)
    conversation = result.scalar_one_or_none()

    if conversation:
        return conversation

    # Create new conversation
    conversation = Conversation(
        instagram_account_id=instagram_account_id,
        instagram_user_id=instagram_user_id,
    )
    db.add(conversation)
    await db.flush()

    logger.info(
        f"Created new Conversation for account {instagram_account_id} "
        f"and user {instagram_user_id}"
    )
    return conversation


async def store_message(
    db: AsyncSession,
    conversation_id: str,
    instagram_message_id: str | None,
    direction: MessageDirection,
    content: str,
    message_type: MessageType = MessageType.TEXT,
    intent: str | None = None,
    confidence: float | None = None,
    is_ai_generated: bool = False,
    instagram_timestamp: datetime | None = None,
) -> Message:
    """
    Store a message in the database.

    Args:
        db: Database session
        conversation_id: The Conversation UUID
        instagram_message_id: The Instagram message ID (mid)
        direction: Whether the message is inbound or outbound
        content: The message text
        message_type: Type of message content
        intent: Detected intent (for AI responses)
        confidence: Confidence score (for AI responses)
        is_ai_generated: Whether the message was generated by AI
        instagram_timestamp: Original timestamp from Instagram

    Returns:
        The created Message
    """
    message = Message(
        conversation_id=conversation_id,
        instagram_message_id=instagram_message_id,
        direction=direction,
        message_type=message_type,
        content=content,
        intent=intent,
        confidence=confidence,
        is_ai_generated=is_ai_generated,
        instagram_timestamp=instagram_timestamp,
    )
    db.add(message)
    await db.flush()

    return message


async def update_conversation_after_message(
    db: AsyncSession,
    conversation: Conversation,
    is_inbound: bool,
) -> None:
    """
    Update conversation metadata after a new message.

    Args:
        db: Database session
        conversation: The Conversation to update
        is_inbound: Whether the message was inbound (from customer)
    """
    from datetime import datetime, timezone

    conversation.last_message_at = datetime.now(timezone.utc)

    if is_inbound:
        conversation.unread_count += 1

    await db.flush()


async def process_webhook_event(
    db: AsyncSession,
    payload: InstagramWebhookPayload,
) -> None:
    """
    Process an incoming webhook event.

    This function handles the business logic for processing Instagram messages.
    It persists messages to the database, sends them through the AI agent,
    and replies via the Instagram API.

    Args:
        db: Database session
        payload: The parsed webhook payload
    """
    messages = extract_messages(payload)

    for message in messages:
        if message.message and message.message.text:
            sender_id = message.sender.id
            recipient_id = message.recipient.id  # This is the page ID
            message_text = message.message.text
            message_id = message.message.mid
            timestamp = datetime.fromtimestamp(
                message.timestamp / 1000
            ) if message.timestamp else None

            logger.info(f"Received message from {sender_id}: {message_text}")

            try:
                # Get the Instagram account (business page)
                instagram_account = await get_or_create_instagram_account(
                    db, recipient_id
                )

                if not instagram_account:
                    logger.warning(
                        f"No registered InstagramAccount found for page {recipient_id}. "
                        "Message will be processed but not persisted."
                    )
                    # Still process through AI and respond, but don't persist
                    await _process_without_persistence(
                        sender_id, recipient_id, message_text, message_id
                    )
                    continue

                # Get or create the Instagram user (customer)
                instagram_user = await get_or_create_instagram_user(db, sender_id)

                # Get or create the conversation
                conversation = await get_or_create_conversation(
                    db, instagram_account.id, instagram_user.id
                )

                # Store the inbound message
                await store_message(
                    db=db,
                    conversation_id=conversation.id,
                    instagram_message_id=message_id,
                    direction=MessageDirection.INBOUND,
                    content=message_text,
                    instagram_timestamp=timestamp,
                )

                # Update conversation metadata
                await update_conversation_after_message(
                    db, conversation, is_inbound=True
                )

                # Process through AI agent
                request = ProcessMessageRequest(
                    sender_id=sender_id,
                    recipient_id=recipient_id,
                    message_text=message_text,
                    message_id=message_id,
                )

                response = await ai_agent_service.process_message(request)

                # Send response back via Instagram
                async with InstagramClient() as client:
                    await client.send_message(
                        recipient_id=sender_id,
                        message_text=response.response_text,
                    )

                # Store the outbound AI response
                await store_message(
                    db=db,
                    conversation_id=conversation.id,
                    instagram_message_id=None,  # We don't get a mid for sent messages
                    direction=MessageDirection.OUTBOUND,
                    content=response.response_text,
                    intent=response.intent.value,
                    confidence=response.confidence,
                    is_ai_generated=True,
                )

                # Update conversation (outbound doesn't increase unread)
                await update_conversation_after_message(
                    db, conversation, is_inbound=False
                )

                # Commit the transaction
                await db.commit()

                logger.info(
                    f"Sent AI response to {sender_id} "
                    f"(intent: {response.intent.value}, confidence: {response.confidence:.2f})"
                )

            except AgentProcessingError as e:
                logger.error(f"AI agent error for message from {sender_id}: {e}")
                # Rollback any uncommitted changes
                await db.rollback()

                # Send a fallback message
                try:
                    async with InstagramClient() as client:
                        await client.send_message(
                            recipient_id=sender_id,
                            message_text="Thanks for your message! A team member will respond shortly.",
                        )
                except Exception as send_error:
                    logger.error(f"Failed to send fallback message: {send_error}")

            except Exception as e:
                logger.error(f"Error processing message from {sender_id}: {e}")
                await db.rollback()


async def _process_without_persistence(
    sender_id: str,
    recipient_id: str,
    message_text: str,
    message_id: str,
) -> None:
    """
    Process a message without database persistence.

    Used when the Instagram account is not registered in our system.

    Args:
        sender_id: The sender's Instagram ID
        recipient_id: The page's Instagram ID
        message_text: The message content
        message_id: The Instagram message ID
    """
    try:
        request = ProcessMessageRequest(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_text=message_text,
            message_id=message_id,
        )

        response = await ai_agent_service.process_message(request)

        async with InstagramClient() as client:
            await client.send_message(
                recipient_id=sender_id,
                message_text=response.response_text,
            )

        logger.info(
            f"Sent AI response to {sender_id} (no persistence) "
            f"(intent: {response.intent.value}, confidence: {response.confidence:.2f})"
        )

    except Exception as e:
        logger.error(f"Error processing message without persistence: {e}")
        try:
            async with InstagramClient() as client:
                await client.send_message(
                    recipient_id=sender_id,
                    message_text="Thanks for your message! A team member will respond shortly.",
                )
        except Exception as send_error:
            logger.error(f"Failed to send fallback message: {send_error}")
