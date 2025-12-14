"""Instagram router with webhook endpoints."""
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from src.instagram import service as instagram_service
from src.instagram.dependencies import verify_webhook_signature
from src.instagram.exceptions import WebhookVerificationError
from src.instagram.schemas import InstagramWebhookPayload, WebhookResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get("/instagram")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
) -> Response:
    """
    Handle webhook verification challenge from Meta.

    Meta sends a GET request with hub.mode, hub.verify_token, and hub.challenge
    parameters when you subscribe to webhooks. We must verify the token and
    return the challenge value to confirm subscription.

    Args:
        hub_mode: Should be "subscribe"
        hub_verify_token: Token to verify against our configured token
        hub_challenge: Challenge value to echo back

    Returns:
        The challenge value as plain text if verification succeeds

    Raises:
        HTTPException: If verification fails
    """
    try:
        challenge = instagram_service.verify_webhook_challenge(
            mode=hub_mode,
            verify_token=hub_verify_token,
            challenge=hub_challenge,
        )
        # Return challenge as plain text (not JSON)
        return Response(content=challenge, media_type="text/plain")
    except WebhookVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.post("/instagram", response_model=WebhookResponse)
async def receive_webhook(
    payload: InstagramWebhookPayload,
    _body: bytes = Depends(verify_webhook_signature),
) -> WebhookResponse:
    """
    Receive and process webhook events from Instagram.

    Meta sends POST requests with message events. We must verify the
    signature, process the payload, and return a 200 OK response quickly
    to acknowledge receipt (within 5 seconds).

    Args:
        payload: The parsed webhook payload
        _body: Raw request body (used for signature verification)

    Returns:
        Acknowledgment response
    """
    logger.info(f"Received Instagram webhook event with {len(payload.entry)} entries")

    # Process the webhook event asynchronously
    await instagram_service.process_webhook_event(payload)

    # Always return OK to acknowledge receipt
    return WebhookResponse(status="ok")
