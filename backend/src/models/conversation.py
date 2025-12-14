"""Conversation model for tracking DM threads."""
from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if False:  # TYPE_CHECKING
    from src.models.instagram_account import InstagramAccount
    from src.models.instagram_user import InstagramUser
    from src.models.message import Message


class ConversationStatus(str, Enum):
    """Status of a conversation."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    CLOSED = "closed"


class Conversation(Base):
    """
    A conversation thread between a business and a customer.

    Links an InstagramAccount (business) with an InstagramUser (customer).
    Contains metadata about the conversation state.
    """

    __tablename__ = "conversations"
    __table_args__ = (
        UniqueConstraint(
            "instagram_account_id",
            "instagram_user_id",
            name="uq_conversations_account_user",
        ),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    instagram_account_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("instagram_accounts.id", ondelete="CASCADE"),
        index=True,
    )
    instagram_user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("instagram_users.id", ondelete="CASCADE"),
        index=True,
    )
    status: Mapped[ConversationStatus] = mapped_column(
        SQLEnum(ConversationStatus),
        default=ConversationStatus.ACTIVE,
    )
    last_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )
    unread_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    instagram_account: Mapped["InstagramAccount"] = relationship(
        "InstagramAccount",
        back_populates="conversations",
    )
    instagram_user: Mapped["InstagramUser"] = relationship(
        "InstagramUser",
        back_populates="conversations",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at.asc()",
    )
