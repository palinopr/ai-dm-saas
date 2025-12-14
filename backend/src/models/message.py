"""Message model for individual DM messages."""
from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if False:  # TYPE_CHECKING
    from src.models.conversation import Conversation


class MessageDirection(str, Enum):
    """Direction of message - inbound from customer or outbound from business."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"


class MessageType(str, Enum):
    """Type of message content."""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    STICKER = "sticker"


class Message(Base):
    """
    An individual message in a conversation.

    Stores the message content, metadata, and AI processing results.
    """

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    instagram_message_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )
    direction: Mapped[MessageDirection] = mapped_column(
        SQLEnum(MessageDirection),
        index=True,
    )
    message_type: Mapped[MessageType] = mapped_column(
        SQLEnum(MessageType),
        default=MessageType.TEXT,
    )
    content: Mapped[str] = mapped_column(Text)

    # AI Processing metadata (for outbound AI responses)
    intent: Mapped[str | None] = mapped_column(String(50), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    instagram_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )
