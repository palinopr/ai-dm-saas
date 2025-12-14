"""Custom exceptions for Instagram domain."""


class InstagramError(Exception):
    """Base exception for Instagram-related errors."""

    pass


class WebhookVerificationError(InstagramError):
    """Raised when webhook verification fails."""

    pass


class SignatureVerificationError(InstagramError):
    """Raised when webhook signature verification fails."""

    pass


class InstagramAPIError(InstagramError):
    """Raised when Instagram Graph API returns an error."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(InstagramAPIError):
    """Raised when Instagram API rate limit is exceeded."""

    pass
