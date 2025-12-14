"""Tests for Instagram webhook endpoints and client."""
import hashlib
import hmac
import json
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient, Response

from src.instagram import service as instagram_service
from src.instagram.client import InstagramClient
from src.instagram.exceptions import (
    InstagramAPIError,
    RateLimitError,
    SignatureVerificationError,
    WebhookVerificationError,
)
from src.instagram.schemas import InstagramWebhookPayload


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def valid_verify_token() -> str:
    """Return a valid verify token for testing."""
    return "test_verify_token_12345"


@pytest.fixture
def app_secret() -> str:
    """Return an app secret for testing."""
    return "test_app_secret_12345"


@pytest.fixture
def sample_webhook_payload() -> dict:
    """Return a sample Instagram webhook payload."""
    return {
        "object": "instagram",
        "entry": [
            {
                "id": "123456789",
                "time": 1234567890,
                "messaging": [
                    {
                        "sender": {"id": "987654321"},
                        "recipient": {"id": "123456789"},
                        "timestamp": 1234567890,
                        "message": {
                            "mid": "mid.1234567890",
                            "text": "Hello, this is a test message!",
                        },
                    }
                ],
            }
        ],
    }


def compute_signature(payload: bytes, secret: str) -> str:
    """Compute HMAC-SHA256 signature for a payload."""
    signature = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return f"sha256={signature}"


# ============================================================================
# Webhook Verification Tests (GET /webhooks/instagram)
# ============================================================================


@pytest.mark.asyncio
async def test_webhook_verification_success(
    client: AsyncClient, valid_verify_token: str
) -> None:
    """Test successful webhook verification."""
    with patch.object(
        instagram_service.settings, "instagram_verify_token", valid_verify_token
    ):
        response = await client.get(
            "/webhooks/instagram",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": valid_verify_token,
                "hub.challenge": "test_challenge_12345",
            },
        )

    assert response.status_code == 200
    assert response.text == "test_challenge_12345"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"


@pytest.mark.asyncio
async def test_webhook_verification_invalid_token(
    client: AsyncClient, valid_verify_token: str
) -> None:
    """Test webhook verification with invalid token."""
    with patch.object(
        instagram_service.settings, "instagram_verify_token", valid_verify_token
    ):
        response = await client.get(
            "/webhooks/instagram",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong_token",
                "hub.challenge": "test_challenge",
            },
        )

    assert response.status_code == 403
    assert "Invalid verify token" in response.json()["detail"]


@pytest.mark.asyncio
async def test_webhook_verification_invalid_mode(
    client: AsyncClient, valid_verify_token: str
) -> None:
    """Test webhook verification with invalid mode."""
    with patch.object(
        instagram_service.settings, "instagram_verify_token", valid_verify_token
    ):
        response = await client.get(
            "/webhooks/instagram",
            params={
                "hub.mode": "unsubscribe",  # Invalid mode
                "hub.verify_token": valid_verify_token,
                "hub.challenge": "test_challenge",
            },
        )

    assert response.status_code == 403
    assert "Invalid mode" in response.json()["detail"]


@pytest.mark.asyncio
async def test_webhook_verification_missing_params(client: AsyncClient) -> None:
    """Test webhook verification with missing parameters."""
    response = await client.get(
        "/webhooks/instagram",
        params={"hub.mode": "subscribe"},  # Missing other params
    )

    assert response.status_code == 422  # Validation error


# ============================================================================
# Signature Verification Tests
# ============================================================================


def test_verify_signature_success(app_secret: str) -> None:
    """Test successful signature verification."""
    payload = b'{"test": "data"}'
    signature = compute_signature(payload, app_secret)

    with patch.object(instagram_service.settings, "instagram_app_secret", app_secret):
        # Should not raise
        instagram_service.verify_signature(payload, signature)


def test_verify_signature_invalid(app_secret: str) -> None:
    """Test signature verification with invalid signature."""
    payload = b'{"test": "data"}'
    invalid_signature = "sha256=0000000000000000000000000000000000000000000000000000000000000000"

    with patch.object(instagram_service.settings, "instagram_app_secret", app_secret):
        with pytest.raises(SignatureVerificationError) as exc_info:
            instagram_service.verify_signature(payload, invalid_signature)

        assert "Invalid signature" in str(exc_info.value)


def test_verify_signature_missing() -> None:
    """Test signature verification with missing header."""
    payload = b'{"test": "data"}'

    with pytest.raises(SignatureVerificationError) as exc_info:
        instagram_service.verify_signature(payload, "")

    assert "Missing signature header" in str(exc_info.value)


def test_verify_signature_malformed() -> None:
    """Test signature verification with malformed header."""
    payload = b'{"test": "data"}'
    malformed_signature = "invalid_format"

    with pytest.raises(SignatureVerificationError) as exc_info:
        instagram_service.verify_signature(payload, malformed_signature)

    assert "Malformed signature header" in str(exc_info.value)


# ============================================================================
# Webhook Event Tests (POST /webhooks/instagram)
# ============================================================================


@pytest.mark.asyncio
async def test_receive_webhook_success(
    client: AsyncClient,
    app_secret: str,
    sample_webhook_payload: dict,
) -> None:
    """Test receiving a webhook event with valid signature."""
    payload_bytes = json.dumps(sample_webhook_payload).encode("utf-8")
    signature = compute_signature(payload_bytes, app_secret)

    with patch.object(instagram_service.settings, "instagram_app_secret", app_secret):
        response = await client.post(
            "/webhooks/instagram",
            content=payload_bytes,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature-256": signature,
            },
        )

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_receive_webhook_invalid_signature(
    client: AsyncClient,
    sample_webhook_payload: dict,
) -> None:
    """Test receiving a webhook event with invalid signature."""
    payload_bytes = json.dumps(sample_webhook_payload).encode("utf-8")
    invalid_signature = "sha256=invalid"

    with patch.object(
        instagram_service.settings, "instagram_app_secret", "some_secret"
    ):
        response = await client.post(
            "/webhooks/instagram",
            content=payload_bytes,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature-256": invalid_signature,
            },
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_receive_webhook_missing_signature(
    client: AsyncClient,
    sample_webhook_payload: dict,
) -> None:
    """Test receiving a webhook event without signature header."""
    response = await client.post(
        "/webhooks/instagram",
        json=sample_webhook_payload,
        # No X-Hub-Signature-256 header
    )

    assert response.status_code == 401
    assert "Missing signature header" in response.json()["detail"]


# ============================================================================
# Service Function Tests
# ============================================================================


def test_verify_webhook_challenge_success(valid_verify_token: str) -> None:
    """Test webhook challenge verification success."""
    with patch.object(
        instagram_service.settings, "instagram_verify_token", valid_verify_token
    ):
        result = instagram_service.verify_webhook_challenge(
            mode="subscribe",
            verify_token=valid_verify_token,
            challenge="my_challenge",
        )

    assert result == "my_challenge"


def test_verify_webhook_challenge_invalid_mode(valid_verify_token: str) -> None:
    """Test webhook challenge with invalid mode."""
    with patch.object(
        instagram_service.settings, "instagram_verify_token", valid_verify_token
    ):
        with pytest.raises(WebhookVerificationError) as exc_info:
            instagram_service.verify_webhook_challenge(
                mode="invalid",
                verify_token=valid_verify_token,
                challenge="my_challenge",
            )

    assert "Invalid mode" in str(exc_info.value)


def test_extract_messages(sample_webhook_payload: dict) -> None:
    """Test extracting messages from webhook payload."""
    payload = InstagramWebhookPayload(**sample_webhook_payload)
    messages = instagram_service.extract_messages(payload)

    assert len(messages) == 1
    assert messages[0].sender.id == "987654321"
    assert messages[0].message is not None
    assert messages[0].message.text == "Hello, this is a test message!"


# ============================================================================
# Instagram Client Tests
# ============================================================================


@pytest.mark.asyncio
async def test_instagram_client_send_message() -> None:
    """Test InstagramClient send_message method."""
    mock_response_data = {
        "recipient_id": "987654321",
        "message_id": "mid.1234567890",
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = lambda: mock_response_data
        mock_post.return_value = mock_response

        async with InstagramClient(
            access_token="test_token", page_id="123456789"
        ) as client:
            response = await client.send_message(
                recipient_id="987654321",
                message_text="Hello from test!",
            )

        assert response.recipient_id == "987654321"
        assert response.message_id == "mid.1234567890"


@pytest.mark.asyncio
async def test_instagram_client_send_media_message() -> None:
    """Test InstagramClient send_media_message method."""
    mock_response_data = {
        "recipient_id": "987654321",
        "message_id": "mid.media123",
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = lambda: mock_response_data
        mock_post.return_value = mock_response

        async with InstagramClient(
            access_token="test_token", page_id="123456789"
        ) as client:
            response = await client.send_media_message(
                recipient_id="987654321",
                media_url="https://example.com/image.jpg",
                media_type="image",
            )

        assert response.recipient_id == "987654321"
        assert response.message_id == "mid.media123"


@pytest.mark.asyncio
async def test_instagram_client_get_user_profile() -> None:
    """Test InstagramClient get_user_profile method."""
    mock_response_data = {
        "id": "987654321",
        "username": "testuser",
        "name": "Test User",
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = lambda: mock_response_data
        mock_get.return_value = mock_response

        async with InstagramClient(
            access_token="test_token", page_id="123456789"
        ) as client:
            profile = await client.get_user_profile("987654321")

        assert profile.id == "987654321"
        assert profile.username == "testuser"
        assert profile.name == "Test User"


@pytest.mark.asyncio
async def test_instagram_client_rate_limit_error() -> None:
    """Test InstagramClient handles rate limit errors."""
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 429
        mock_post.return_value = mock_response

        async with InstagramClient(
            access_token="test_token", page_id="123456789"
        ) as client:
            with pytest.raises(RateLimitError):
                await client.send_message(
                    recipient_id="987654321",
                    message_text="Hello!",
                )


@pytest.mark.asyncio
async def test_instagram_client_api_error() -> None:
    """Test InstagramClient handles API errors."""
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status_code = 400
        mock_response.json = lambda: {
            "error": {"message": "Invalid recipient"}
        }
        mock_post.return_value = mock_response

        async with InstagramClient(
            access_token="test_token", page_id="123456789"
        ) as client:
            with pytest.raises(InstagramAPIError) as exc_info:
                await client.send_message(
                    recipient_id="invalid",
                    message_text="Hello!",
                )

        assert "Invalid recipient" in str(exc_info.value)
        assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_instagram_client_context_manager_required() -> None:
    """Test InstagramClient requires context manager usage."""
    client = InstagramClient(access_token="test", page_id="123")

    with pytest.raises(RuntimeError) as exc_info:
        await client.send_message("123", "test")

    assert "async context manager" in str(exc_info.value)
