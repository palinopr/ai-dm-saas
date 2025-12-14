"""Instagram account model for linking business accounts to users."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if False:  # TYPE_CHECKING
    from src.models.conversation import Conversation
    from src.models.user import User


class InstagramAccount(Base):
    """
    Instagram business account linked to a User.

    A User (business owner) can connect multiple Instagram pages.
    This stores the page credentials and metadata.
    """

    __tablename__ = "instagram_accounts"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    instagram_page_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )
    instagram_username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    access_token: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
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
    user: Mapped["User"] = relationship("User", back_populates="instagram_accounts")
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="instagram_account",
        cascade="all, delete-orphan",
    )
