"""Instagram Graph API client for sending messages."""
import logging
from types import TracebackType
from typing import Self

import httpx

from src.config import settings
from src.instagram.exceptions import InstagramAPIError, RateLimitError
from src.instagram.schemas import InstagramUserProfile, SendMessageResponse

logger = logging.getLogger(__name__)

GRAPH_API_BASE_URL = "https://graph.facebook.com/v21.0"


class InstagramClient:
    """
    Async client for Instagram Graph API.

    Usage:
        async with InstagramClient() as client:
            response = await client.send_message(recipient_id, "Hello!")
    """

    def __init__(
        self,
        access_token: str | None = None,
        page_id: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize the Instagram client.

        Args:
            access_token: Instagram page access token (defaults to settings)
            page_id: Instagram page ID (defaults to settings)
            timeout: Request timeout in seconds
        """
        self.access_token = access_token or settings.instagram_access_token
        self.page_id = page_id or settings.instagram_page_id
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        """Enter async context manager."""
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        """Get the HTTP client, raising if not initialized."""
        if self._client is None:
            raise RuntimeError(
                "InstagramClient must be used as an async context manager"
            )
        return self._client

    async def _handle_response(self, response: httpx.Response) -> dict:
        """
        Handle API response and raise appropriate exceptions.

        Args:
            response: The HTTP response

        Returns:
            The response JSON data

        Raises:
            RateLimitError: If rate limit is exceeded
            InstagramAPIError: For other API errors
        """
        if response.status_code == 429:
            raise RateLimitError(
                "Instagram API rate limit exceeded",
                status_code=429,
            )

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_message = error_data.get("error", {}).get(
                    "message", "Unknown error"
                )
            except Exception:
                error_message = response.text or "Unknown error"

            raise InstagramAPIError(
                f"Instagram API error: {error_message}",
                status_code=response.status_code,
            )

        return response.json()

    async def send_message(
        self,
        recipient_id: str,
        message_text: str,
    ) -> SendMessageResponse:
        """
        Send a text message to a user.

        Args:
            recipient_id: The Instagram-scoped ID of the recipient
            message_text: The message text to send

        Returns:
            Response with recipient_id and message_id

        Raises:
            InstagramAPIError: If the API request fails
        """
        client = self._get_client()

        url = f"{GRAPH_API_BASE_URL}/{self.page_id}/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text},
        }

        logger.info(f"Sending message to {recipient_id}")
        response = await client.post(url, json=payload)
        data = await self._handle_response(response)

        return SendMessageResponse(
            recipient_id=data.get("recipient_id", recipient_id),
            message_id=data.get("message_id", ""),
        )

    async def send_media_message(
        self,
        recipient_id: str,
        media_url: str,
        media_type: str = "image",
    ) -> SendMessageResponse:
        """
        Send a media message (image, video, etc.) to a user.

        Args:
            recipient_id: The Instagram-scoped ID of the recipient
            media_url: URL of the media to send
            media_type: Type of media ("image", "video", "audio", "file")

        Returns:
            Response with recipient_id and message_id

        Raises:
            InstagramAPIError: If the API request fails
        """
        client = self._get_client()

        url = f"{GRAPH_API_BASE_URL}/{self.page_id}/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": media_type,
                    "payload": {"url": media_url},
                }
            },
        }

        logger.info(f"Sending {media_type} to {recipient_id}")
        response = await client.post(url, json=payload)
        data = await self._handle_response(response)

        return SendMessageResponse(
            recipient_id=data.get("recipient_id", recipient_id),
            message_id=data.get("message_id", ""),
        )

    async def get_user_profile(self, user_id: str) -> InstagramUserProfile:
        """
        Get a user's profile information.

        Args:
            user_id: The Instagram-scoped ID of the user

        Returns:
            User profile information

        Raises:
            InstagramAPIError: If the API request fails
        """
        client = self._get_client()

        url = f"{GRAPH_API_BASE_URL}/{user_id}"
        params = {"fields": "id,username,name"}

        logger.info(f"Fetching profile for user {user_id}")
        response = await client.get(url, params=params)
        data = await self._handle_response(response)

        return InstagramUserProfile(
            id=data.get("id", user_id),
            username=data.get("username"),
            name=data.get("name"),
        )
