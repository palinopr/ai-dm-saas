"""Instagram user model for customer profiles."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if False:  # TYPE_CHECKING
    from src.models.conversation import Conversation


class InstagramUser(Base):
    """
    Instagram user profile (the customer messaging the business).

    This stores basic profile info about customers who message
    the business via Instagram DMs.
    """

    __tablename__ = "instagram_users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    instagram_user_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )
    username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    profile_picture_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
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
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="instagram_user",
    )
