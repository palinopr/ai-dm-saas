"""Instagram service with business logic for webhook handling."""
import hashlib
import hmac
import logging

from src.ai_agent import service as ai_agent_service
from src.ai_agent.exceptions import AgentProcessingError
from src.ai_agent.schemas import ProcessMessageRequest
from src.config import settings
from src.instagram.client import InstagramClient
from src.instagram.exceptions import SignatureVerificationError, WebhookVerificationError
from src.instagram.schemas import InstagramMessaging, InstagramWebhookPayload

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


async def process_webhook_event(payload: InstagramWebhookPayload) -> None:
    """
    Process an incoming webhook event.

    This function handles the business logic for processing Instagram messages.
    It sends messages through the AI agent and replies via the Instagram API.

    Args:
        payload: The parsed webhook payload
    """
    messages = extract_messages(payload)

    for message in messages:
        if message.message and message.message.text:
            logger.info(
                f"Received message from {message.sender.id}: {message.message.text}"
            )

            try:
                # Process through AI agent
                request = ProcessMessageRequest(
                    sender_id=message.sender.id,
                    recipient_id=message.recipient.id,
                    message_text=message.message.text,
                    message_id=message.message.mid,
                )

                response = await ai_agent_service.process_message(request)

                # Send response back via Instagram
                async with InstagramClient() as client:
                    await client.send_message(
                        recipient_id=message.sender.id,
                        message_text=response.response_text,
                    )

                logger.info(
                    f"Sent AI response to {message.sender.id} "
                    f"(intent: {response.intent.value}, confidence: {response.confidence:.2f})"
                )

            except AgentProcessingError as e:
                logger.error(f"AI agent error for message from {message.sender.id}: {e}")
                # Send a fallback message
                try:
                    async with InstagramClient() as client:
                        await client.send_message(
                            recipient_id=message.sender.id,
                            message_text="Thanks for your message! A team member will respond shortly.",
                        )
                except Exception as send_error:
                    logger.error(f"Failed to send fallback message: {send_error}")

            except Exception as e:
                logger.error(f"Error processing message from {message.sender.id}: {e}")
