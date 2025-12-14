"""Conversations router with API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_active_user
from src.conversations import service as conversations_service
from src.conversations.schemas import (
    ConversationDetailResponse,
    ConversationResponse,
    ConversationStatusUpdate,
    InstagramUserResponse,
    MessageResponse,
    PaginatedConversationsResponse,
    PaginatedMessagesResponse,
    PaginationMeta,
)
from src.database import get_db
from src.models.conversation import ConversationStatus
from src.models.user import User

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("", response_model=PaginatedConversationsResponse)
async def list_conversations(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PaginatedConversationsResponse:
    """List all conversations for the current user's Instagram accounts."""
    conversations, total = await conversations_service.get_conversations_for_user(
        db, current_user.id, page, page_size
    )

    # Build response with last message previews
    items = []
    for conv in conversations:
        preview = await conversations_service.get_last_message_preview(db, conv.id)
        items.append(
            ConversationResponse(
                id=conv.id,
                instagram_account_id=conv.instagram_account_id,
                status=conv.status,
                last_message_at=conv.last_message_at,
                unread_count=conv.unread_count,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                instagram_user=InstagramUserResponse(
                    id=conv.instagram_user.id,
                    instagram_user_id=conv.instagram_user.instagram_user_id,
                    username=conv.instagram_user.username,
                    name=conv.instagram_user.name,
                    profile_picture_url=conv.instagram_user.profile_picture_url,
                ),
                last_message_preview=preview,
            )
        )

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return PaginatedConversationsResponse(
        items=items,
        meta=PaginationMeta(
            total=total,
            page=page,
            page_size=page_size,
            has_next=page < total_pages,
            has_previous=page > 1,
        ),
    )


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ConversationDetailResponse:
    """Get a single conversation by ID."""
    conversation = await conversations_service.get_conversation_by_id(
        db, conversation_id, current_user.id
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationDetailResponse(
        id=conversation.id,
        instagram_account_id=conversation.instagram_account_id,
        status=conversation.status,
        last_message_at=conversation.last_message_at,
        unread_count=conversation.unread_count,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        instagram_user=InstagramUserResponse(
            id=conversation.instagram_user.id,
            instagram_user_id=conversation.instagram_user.instagram_user_id,
            username=conversation.instagram_user.username,
            name=conversation.instagram_user.name,
            profile_picture_url=conversation.instagram_user.profile_picture_url,
        ),
    )


@router.get("/{conversation_id}/messages", response_model=PaginatedMessagesResponse)
async def list_messages(
    conversation_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PaginatedMessagesResponse:
    """Get paginated messages for a conversation."""
    result = await conversations_service.get_messages_for_conversation(
        db, conversation_id, current_user.id, page, page_size
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    messages, total = result
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return PaginatedMessagesResponse(
        items=[
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                instagram_message_id=msg.instagram_message_id,
                direction=msg.direction,
                message_type=msg.message_type,
                content=msg.content,
                intent=msg.intent,
                confidence=msg.confidence,
                is_ai_generated=msg.is_ai_generated,
                instagram_timestamp=msg.instagram_timestamp,
                created_at=msg.created_at,
            )
            for msg in messages
        ],
        meta=PaginationMeta(
            total=total,
            page=page,
            page_size=page_size,
            has_next=page < total_pages,
            has_previous=page > 1,
        ),
    )


@router.patch("/{conversation_id}/status", response_model=ConversationDetailResponse)
async def update_status(
    conversation_id: str,
    status_update: ConversationStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ConversationDetailResponse:
    """Update conversation status."""
    # Map schema enum to model enum
    model_status = ConversationStatus(status_update.status.value)

    conversation = await conversations_service.update_conversation_status(
        db, conversation_id, current_user.id, model_status
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationDetailResponse(
        id=conversation.id,
        instagram_account_id=conversation.instagram_account_id,
        status=conversation.status,
        last_message_at=conversation.last_message_at,
        unread_count=conversation.unread_count,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        instagram_user=InstagramUserResponse(
            id=conversation.instagram_user.id,
            instagram_user_id=conversation.instagram_user.instagram_user_id,
            username=conversation.instagram_user.username,
            name=conversation.instagram_user.name,
            profile_picture_url=conversation.instagram_user.profile_picture_url,
        ),
    )


@router.post("/{conversation_id}/read", response_model=ConversationDetailResponse)
async def mark_as_read(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ConversationDetailResponse:
    """Mark all messages in a conversation as read."""
    conversation = await conversations_service.mark_conversation_as_read(
        db, conversation_id, current_user.id
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return ConversationDetailResponse(
        id=conversation.id,
        instagram_account_id=conversation.instagram_account_id,
        status=conversation.status,
        last_message_at=conversation.last_message_at,
        unread_count=conversation.unread_count,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        instagram_user=InstagramUserResponse(
            id=conversation.instagram_user.id,
            instagram_user_id=conversation.instagram_user.instagram_user_id,
            username=conversation.instagram_user.username,
            name=conversation.instagram_user.name,
            profile_picture_url=conversation.instagram_user.profile_picture_url,
        ),
    )
