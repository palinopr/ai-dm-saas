"""Instagram dependencies for FastAPI."""
from fastapi import Header, HTTPException, Request, status

from src.instagram import service as instagram_service
from src.instagram.exceptions import SignatureVerificationError


async def verify_webhook_signature(
    request: Request,
    x_hub_signature_256: str | None = Header(None),
) -> bytes:
    """
    FastAPI dependency to verify webhook signature.

    This dependency reads the raw request body, verifies the HMAC-SHA256
    signature, and returns the raw body for further processing.

    Args:
        request: The FastAPI request object
        x_hub_signature_256: The X-Hub-Signature-256 header

    Returns:
        The raw request body bytes

    Raises:
        HTTPException: If signature verification fails
    """
    body = await request.body()

    try:
        instagram_service.verify_signature(body, x_hub_signature_256 or "")
    except SignatureVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    return body
