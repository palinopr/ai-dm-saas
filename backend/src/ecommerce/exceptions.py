"""Custom exceptions for the ecommerce/Shopify domain."""


class ShopifyError(Exception):
    """Base exception for all Shopify-related errors."""

    pass


class ShopifyAPIError(ShopifyError):
    """Raised when Shopify API returns an error."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
    ) -> None:
        """
        Initialize the Shopify API error.

        Args:
            message: Error message
            status_code: HTTP status code from the API response
        """
        super().__init__(message)
        self.status_code = status_code


class ShopifyRateLimitError(ShopifyAPIError):
    """Raised when Shopify API rate limit is exceeded (HTTP 429)."""

    def __init__(
        self,
        message: str,
        status_code: int = 429,
        retry_after: float = 2.0,
    ) -> None:
        """
        Initialize the rate limit error.

        Args:
            message: Error message
            status_code: HTTP status code (always 429)
            retry_after: Seconds to wait before retrying
        """
        super().__init__(message, status_code)
        self.retry_after = retry_after


class ShopifyConfigurationError(ShopifyError):
    """Raised when Shopify configuration is missing or invalid."""

    pass


class ProductNotFoundError(ShopifyAPIError):
    """Raised when a requested product is not found."""

    pass


class OrderNotFoundError(ShopifyAPIError):
    """Raised when a requested order is not found."""

    pass
