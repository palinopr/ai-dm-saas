"""Conversation service with business logic."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.conversation import Conversation, ConversationStatus
from src.models.instagram_account import InstagramAccount
from src.models.message import Message


async def get_conversations_for_user(
    db: AsyncSession,
    user_id: str,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Conversation], int]:
    """
    Get paginated conversations for a user.

    Returns conversations where the user owns the Instagram account,
    ordered by last_message_at descending.
    """
    # Get the user's Instagram accounts
    accounts_query = select(InstagramAccount.id).where(
        InstagramAccount.user_id == user_id,
        InstagramAccount.is_active == True,  # noqa: E712
    )

    # Count total conversations
    count_query = (
        select(func.count(Conversation.id))
        .where(Conversation.instagram_account_id.in_(accounts_query))
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Get paginated conversations with instagram_user loaded
    offset = (page - 1) * page_size
    conversations_query = (
        select(Conversation)
        .where(Conversation.instagram_account_id.in_(accounts_query))
        .options(selectinload(Conversation.instagram_user))
        .order_by(Conversation.last_message_at.desc().nulls_last())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(conversations_query)
    conversations = list(result.scalars().all())

    return conversations, total


async def get_conversation_by_id(
    db: AsyncSession,
    conversation_id: str,
    user_id: str,
) -> Conversation | None:
    """
    Get a single conversation by ID.

    Only returns the conversation if the user owns the associated Instagram account.
    """
    query = (
        select(Conversation)
        .join(InstagramAccount)
        .where(
            Conversation.id == conversation_id,
            InstagramAccount.user_id == user_id,
            InstagramAccount.is_active == True,  # noqa: E712
        )
        .options(selectinload(Conversation.instagram_user))
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_messages_for_conversation(
    db: AsyncSession,
    conversation_id: str,
    user_id: str,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Message], int] | None:
    """
    Get paginated messages for a conversation.

    Returns None if the conversation doesn't exist or user doesn't have access.
    Messages are ordered by created_at ascending (oldest first).
    """
    # First verify user has access to this conversation
    conversation = await get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        return None

    # Count total messages
    count_query = (
        select(func.count(Message.id))
        .where(Message.conversation_id == conversation_id)
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Get paginated messages
    offset = (page - 1) * page_size
    messages_query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(messages_query)
    messages = list(result.scalars().all())

    return messages, total


async def update_conversation_status(
    db: AsyncSession,
    conversation_id: str,
    user_id: str,
    status: ConversationStatus,
) -> Conversation | None:
    """
    Update conversation status.

    Returns None if conversation doesn't exist or user doesn't have access.
    """
    conversation = await get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        return None

    conversation.status = status
    await db.commit()
    await db.refresh(conversation)

    return conversation


async def mark_conversation_as_read(
    db: AsyncSession,
    conversation_id: str,
    user_id: str,
) -> Conversation | None:
    """
    Mark all messages in a conversation as read by resetting unread_count.

    Returns None if conversation doesn't exist or user doesn't have access.
    """
    conversation = await get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        return None

    conversation.unread_count = 0
    await db.commit()
    await db.refresh(conversation)

    return conversation


async def get_last_message_preview(
    db: AsyncSession,
    conversation_id: str,
) -> str | None:
    """Get the last message content for a conversation preview."""
    query = (
        select(Message.content)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(1)
    )
    result = await db.execute(query)
    content = result.scalar_one_or_none()

    if content:
        # Truncate for preview
        return content[:100] + "..." if len(content) > 100 else content
    return None
