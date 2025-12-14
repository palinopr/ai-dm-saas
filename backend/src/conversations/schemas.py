"""Conversation schemas for request/response validation."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ConversationStatusEnum(str, Enum):
    """Status of a conversation."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    CLOSED = "closed"


class MessageDirectionEnum(str, Enum):
    """Direction of message."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"


class MessageTypeEnum(str, Enum):
    """Type of message content."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    STICKER = "sticker"


# Instagram User schemas
class InstagramUserResponse(BaseModel):
    """Schema for Instagram user in responses."""

    id: str
    instagram_user_id: str
    username: str | None
    name: str | None
    profile_picture_url: str | None

    class Config:
        from_attributes = True


# Message schemas
class MessageResponse(BaseModel):
    """Schema for message in responses."""

    id: str
    conversation_id: str
    instagram_message_id: str | None
    direction: MessageDirectionEnum
    message_type: MessageTypeEnum
    content: str
    intent: str | None
    confidence: float | None
    is_ai_generated: bool
    instagram_timestamp: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


# Conversation schemas
class ConversationResponse(BaseModel):
    """Schema for conversation in responses."""

    id: str
    instagram_account_id: str
    status: ConversationStatusEnum
    last_message_at: datetime | None
    unread_count: int
    created_at: datetime
    updated_at: datetime
    instagram_user: InstagramUserResponse
    last_message_preview: str | None = None

    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    """Schema for detailed conversation with messages."""

    id: str
    instagram_account_id: str
    status: ConversationStatusEnum
    last_message_at: datetime | None
    unread_count: int
    created_at: datetime
    updated_at: datetime
    instagram_user: InstagramUserResponse

    class Config:
        from_attributes = True


class ConversationStatusUpdate(BaseModel):
    """Schema for updating conversation status."""

    status: ConversationStatusEnum


# Pagination schemas
class PaginationMeta(BaseModel):
    """Pagination metadata."""

    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


class PaginatedConversationsResponse(BaseModel):
    """Paginated list of conversations."""

    items: list[ConversationResponse]
    meta: PaginationMeta


class PaginatedMessagesResponse(BaseModel):
    """Paginated list of messages."""

    items: list[MessageResponse]
    meta: PaginationMeta
