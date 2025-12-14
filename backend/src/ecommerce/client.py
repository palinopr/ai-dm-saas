"""Shopify REST Admin API client for product and order operations."""

import logging
import re
from types import TracebackType
from typing import Self

import httpx

from src.config import settings
from src.ecommerce.exceptions import (
    OrderNotFoundError,
    ProductNotFoundError,
    ShopifyAPIError,
    ShopifyRateLimitError,
)
from src.ecommerce.schemas import (
    OrderStatusResult,
    ProductSearchResult,
    ShopifyProduct,
)

logger = logging.getLogger(__name__)


class ShopifyClient:
    """
    Async client for Shopify REST Admin API (2024-01 version).

    This client must be used as an async context manager to ensure proper
    resource cleanup.

    Usage:
        async with ShopifyClient() as client:
            products = await client.search_products("t-shirt")
            order = await client.get_order_status("12345")
    """

    API_VERSION = "2024-01"

    def __init__(
        self,
        store_url: str | None = None,
        api_key: str | None = None,
        access_token: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize the Shopify client.

        Args:
            store_url: Shopify store URL (e.g., "mystore.myshopify.com")
            api_key: Shopify API key (optional, for identification)
            access_token: Shopify Admin API access token (required)
            timeout: Request timeout in seconds
        """
        self.store_url = store_url or settings.shopify_store_url
        self.api_key = api_key or settings.shopify_api_key
        self.access_token = access_token or settings.shopify_access_token
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

        # Construct base URL for API requests
        self.base_url = f"https://{self.store_url}/admin/api/{self.API_VERSION}"

    async def __aenter__(self) -> Self:
        """Enter async context manager and initialize HTTP client."""
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            headers={
                "X-Shopify-Access-Token": self.access_token,
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
        """Exit async context manager and cleanup HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        """
        Get the HTTP client, raising if not initialized.

        Raises:
            RuntimeError: If client is used outside of async context manager
        """
        if self._client is None:
            raise RuntimeError(
                "ShopifyClient must be used as an async context manager. "
                "Use: async with ShopifyClient() as client: ..."
            )
        return self._client

    async def _handle_response(
        self,
        response: httpx.Response,
        not_found_exception: type[ShopifyAPIError] | None = None,
    ) -> dict:
        """
        Handle API response and raise appropriate exceptions.

        Shopify uses bucket-based rate limiting:
        - 40 requests per app per store per second (burst)
        - X-Shopify-Shop-Api-Call-Limit header shows current usage

        Args:
            response: The HTTP response from Shopify
            not_found_exception: Exception type to raise for 404 responses

        Returns:
            The response JSON data as a dictionary

        Raises:
            ShopifyRateLimitError: If rate limit exceeded (429)
            ProductNotFoundError/OrderNotFoundError: If resource not found (404)
            ShopifyAPIError: For other API errors (4xx, 5xx)
        """
        # Check rate limit headers for proactive monitoring
        call_limit = response.headers.get("X-Shopify-Shop-Api-Call-Limit", "")
        if call_limit:
            try:
                current, max_limit = call_limit.split("/")
                if int(current) >= int(max_limit) - 5:
                    logger.warning(f"Approaching Shopify rate limit: {call_limit}")
            except ValueError:
                pass  # Ignore malformed headers

        # Handle rate limit exceeded
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "2")
            try:
                retry_seconds = float(retry_after)
            except ValueError:
                retry_seconds = 2.0
            raise ShopifyRateLimitError(
                f"Shopify API rate limit exceeded. Retry after {retry_seconds}s",
                status_code=429,
                retry_after=retry_seconds,
            )

        # Handle not found
        if response.status_code == 404:
            if not_found_exception:
                raise not_found_exception(
                    "Resource not found",
                    status_code=404,
                )
            raise ShopifyAPIError("Resource not found", status_code=404)

        # Handle other errors
        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_message = error_data.get("errors", "Unknown error")
                if isinstance(error_message, dict):
                    # Shopify sometimes returns errors as a dict
                    error_message = str(error_message)
            except Exception:
                error_message = response.text or "Unknown error"

            raise ShopifyAPIError(
                f"Shopify API error: {error_message}",
                status_code=response.status_code,
            )

        return response.json()

    def _clean_html(self, html: str | None) -> str:
        """
        Remove HTML tags from a string for plain text display.

        Args:
            html: HTML string to clean

        Returns:
            Plain text with HTML tags removed
        """
        if not html:
            return ""
        clean_pattern = re.compile("<.*?>")
        return re.sub(clean_pattern, "", html).strip()

    def _extract_tracking_numbers(self, order: dict) -> list[str]:
        """
        Extract tracking numbers from order fulfillments.

        Args:
            order: Order dictionary from Shopify API

        Returns:
            List of tracking numbers from all fulfillments
        """
        tracking_numbers: list[str] = []
        fulfillments = order.get("fulfillments", [])
        for fulfillment in fulfillments:
            tracking_number = fulfillment.get("tracking_number")
            if tracking_number:
                tracking_numbers.append(tracking_number)
        return tracking_numbers

    async def search_products(
        self,
        query: str,
        limit: int = 5,
    ) -> list[ProductSearchResult]:
        """
        Search for products by name/title.

        Args:
            query: Search query (product name or keywords)
            limit: Maximum number of results to return (default 5)

        Returns:
            List of matching products with basic information

        Raises:
            ShopifyAPIError: If the API request fails
            ShopifyRateLimitError: If rate limit is exceeded
        """
        client = self._get_client()

        url = f"{self.base_url}/products.json"
        params = {
            "title": query,
            "limit": limit,
            "status": "active",
            "fields": "id,title,body_html,vendor,product_type,handle,variants,images",
        }

        logger.info(f"Searching Shopify products with query: {query}")
        response = await client.get(url, params=params)
        data = await self._handle_response(response)

        products = data.get("products", [])
        results: list[ProductSearchResult] = []

        for product in products:
            # Get primary variant for price and inventory
            variants = product.get("variants", [])
            primary_variant = variants[0] if variants else {}

            # Get first image URL
            images = product.get("images", [])
            image_url = images[0].get("src") if images else None

            results.append(
                ProductSearchResult(
                    id=str(product.get("id")),
                    title=product.get("title", ""),
                    description=self._clean_html(product.get("body_html")),
                    price=primary_variant.get("price", "0.00"),
                    currency="USD",  # Default currency
                    inventory_quantity=primary_variant.get("inventory_quantity", 0),
                    available=primary_variant.get("inventory_quantity", 0) > 0,
                    image_url=image_url,
                    handle=product.get("handle", ""),
                    vendor=product.get("vendor"),
                    product_type=product.get("product_type"),
                )
            )

        logger.info(f"Found {len(results)} products for query: {query}")
        return results

    async def get_product_details(
        self,
        product_id: str,
    ) -> ShopifyProduct:
        """
        Get detailed information about a specific product.

        Args:
            product_id: The Shopify product ID

        Returns:
            Full product details including all variants

        Raises:
            ProductNotFoundError: If product doesn't exist
            ShopifyAPIError: If the API request fails
        """
        client = self._get_client()

        url = f"{self.base_url}/products/{product_id}.json"

        logger.info(f"Fetching Shopify product details: {product_id}")
        response = await client.get(url)
        data = await self._handle_response(response, ProductNotFoundError)

        product = data.get("product", {})
        return ShopifyProduct.model_validate(product)

    async def get_order_status(
        self,
        order_id: str,
    ) -> OrderStatusResult:
        """
        Get order status by order ID or order number.

        Shopify order IDs are numeric, but customers often reference
        order numbers (e.g., "#1001"). This method handles both formats.

        Args:
            order_id: Order ID or order number (with or without # prefix)

        Returns:
            Order status information including fulfillment and tracking

        Raises:
            OrderNotFoundError: If order doesn't exist
            ShopifyAPIError: If the API request fails
        """
        client = self._get_client()

        # Clean up order ID (remove # if present)
        clean_order_id = order_id.lstrip("#")

        # Try to get by order number first (more common for customers)
        url = f"{self.base_url}/orders.json"
        params = {
            "name": f"#{clean_order_id}",
            "status": "any",
            "limit": 1,
        }

        logger.info(f"Looking up Shopify order: {order_id}")
        response = await client.get(url, params=params)
        data = await self._handle_response(response)

        orders = data.get("orders", [])

        # If not found by order number, try by order ID directly
        if not orders:
            url = f"{self.base_url}/orders/{clean_order_id}.json"
            response = await client.get(url)
            data = await self._handle_response(response, OrderNotFoundError)
            order = data.get("order", {})
        else:
            order = orders[0]

        if not order:
            raise OrderNotFoundError(
                f"Order {order_id} not found",
                status_code=404,
            )

        shipping_address = order.get("shipping_address", {}) or {}

        return OrderStatusResult(
            order_id=str(order.get("id")),
            order_number=order.get("name", ""),
            email=order.get("email", ""),
            financial_status=order.get("financial_status", ""),
            fulfillment_status=order.get("fulfillment_status") or "unfulfilled",
            total_price=order.get("total_price", "0.00"),
            currency=order.get("currency", "USD"),
            created_at=order.get("created_at", ""),
            updated_at=order.get("updated_at", ""),
            line_items_count=len(order.get("line_items", [])),
            tracking_numbers=self._extract_tracking_numbers(order),
            shipping_address_city=shipping_address.get("city"),
            shipping_address_country=shipping_address.get("country"),
        )
