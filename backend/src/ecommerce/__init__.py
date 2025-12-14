"""E-commerce domain for Shopify integration."""

from src.ecommerce.client import ShopifyClient
from src.ecommerce.exceptions import (
    OrderNotFoundError,
    ProductNotFoundError,
    ShopifyAPIError,
    ShopifyConfigurationError,
    ShopifyError,
    ShopifyRateLimitError,
)
from src.ecommerce.tools import ECOMMERCE_TOOLS, check_order_status, get_product_info

__all__ = [
    # Client
    "ShopifyClient",
    # Exceptions
    "ShopifyError",
    "ShopifyAPIError",
    "ShopifyRateLimitError",
    "ShopifyConfigurationError",
    "ProductNotFoundError",
    "OrderNotFoundError",
    # Tools
    "ECOMMERCE_TOOLS",
    "get_product_info",
    "check_order_status",
]
