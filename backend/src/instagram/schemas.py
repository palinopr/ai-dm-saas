"""Instagram schemas for request/response validation."""
from typing import Literal

from pydantic import BaseModel, Field


# ============================================================================
# Webhook Verification (GET /webhooks/instagram)
# ============================================================================


class WebhookVerificationQuery(BaseModel):
    """Query parameters for webhook verification challenge from Meta."""

    hub_mode: str = Field(alias="hub.mode")
    hub_verify_token: str = Field(alias="hub.verify_token")
    hub_challenge: str = Field(alias="hub.challenge")


# ============================================================================
# Webhook Event Payload (POST /webhooks/instagram)
# ============================================================================


class InstagramSender(BaseModel):
    """Sender information in a message."""

    id: str


class InstagramRecipient(BaseModel):
    """Recipient information in a message."""

    id: str


class InstagramMessageContent(BaseModel):
    """Content of an Instagram message."""

    mid: str
    text: str | None = None


class InstagramMessaging(BaseModel):
    """A single messaging event."""

    sender: InstagramSender
    recipient: InstagramRecipient
    timestamp: int
    message: InstagramMessageContent | None = None


class InstagramEntry(BaseModel):
    """A single entry in the webhook payload."""

    id: str
    time: int
    messaging: list[InstagramMessaging] | None = None


class InstagramWebhookPayload(BaseModel):
    """Webhook payload from Instagram."""

    object: Literal["instagram"]
    entry: list[InstagramEntry]


# ============================================================================
# Webhook Response
# ============================================================================


class WebhookResponse(BaseModel):
    """Standard response for webhook POST requests."""

    status: str = "ok"


# ============================================================================
# Instagram Graph API - Send Message
# ============================================================================


class SendMessageRequest(BaseModel):
    """Request to send a message via Instagram Graph API."""

    recipient_id: str
    message_text: str


class SendMessageResponse(BaseModel):
    """Response from Instagram Graph API after sending a message."""

    recipient_id: str
    message_id: str


# ============================================================================
# Instagram Graph API - User Profile
# ============================================================================


class InstagramUserProfile(BaseModel):
    """User profile from Instagram Graph API."""

    id: str
    username: str | None = None
    name: str | None = None
