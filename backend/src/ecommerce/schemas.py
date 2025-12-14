"""Pydantic models for Shopify API responses and tool outputs."""

from typing import Literal

from pydantic import BaseModel, Field


# ============================================================================
# Shopify Product Schemas
# ============================================================================


class ShopifyProductImage(BaseModel):
    """Shopify product image."""

    id: int
    product_id: int
    src: str
    alt: str | None = None
    position: int = 1


class ShopifyProductVariant(BaseModel):
    """Shopify product variant with price and inventory information."""

    id: int
    product_id: int
    title: str
    price: str
    sku: str | None = None
    inventory_quantity: int = 0
    inventory_management: str | None = None
    option1: str | None = None
    option2: str | None = None
    option3: str | None = None
    weight: float | None = None
    weight_unit: str = "kg"
    available: bool = True


class ShopifyProduct(BaseModel):
    """Full Shopify product representation."""

    id: int
    title: str
    body_html: str | None = None
    vendor: str | None = None
    product_type: str | None = None
    handle: str
    status: Literal["active", "archived", "draft"] = "active"
    tags: str = ""
    variants: list[ShopifyProductVariant] = Field(default_factory=list)
    images: list[ShopifyProductImage] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


# ============================================================================
# Shopify Order Schemas
# ============================================================================


class ShopifyLineItem(BaseModel):
    """Line item in a Shopify order."""

    id: int
    product_id: int | None = None
    variant_id: int | None = None
    title: str
    quantity: int
    price: str
    sku: str | None = None


class ShopifyFulfillment(BaseModel):
    """Order fulfillment information with tracking details."""

    id: int
    order_id: int
    status: str
    tracking_number: str | None = None
    tracking_url: str | None = None
    tracking_company: str | None = None


class ShopifyShippingAddress(BaseModel):
    """Shipping address for an order."""

    first_name: str | None = None
    last_name: str | None = None
    address1: str | None = None
    city: str | None = None
    province: str | None = None
    country: str | None = None
    zip: str | None = None


class ShopifyOrder(BaseModel):
    """Full Shopify order representation."""

    id: int
    name: str  # Order number like "#1001"
    email: str | None = None
    financial_status: str
    fulfillment_status: str | None = None
    total_price: str
    currency: str = "USD"
    line_items: list[ShopifyLineItem] = Field(default_factory=list)
    fulfillments: list[ShopifyFulfillment] = Field(default_factory=list)
    shipping_address: ShopifyShippingAddress | None = None
    created_at: str
    updated_at: str


# ============================================================================
# Tool Response Schemas (Simplified for AI Agent)
# ============================================================================


class ProductSearchResult(BaseModel):
    """Simplified product information for AI agent tools."""

    id: str
    title: str
    description: str
    price: str
    currency: str = "USD"
    inventory_quantity: int
    available: bool
    image_url: str | None = None
    handle: str
    vendor: str | None = None
    product_type: str | None = None


class OrderStatusResult(BaseModel):
    """Simplified order status information for AI agent tools."""

    order_id: str
    order_number: str
    email: str
    financial_status: str  # paid, pending, refunded, etc.
    fulfillment_status: str  # fulfilled, unfulfilled, partial
    total_price: str
    currency: str = "USD"
    created_at: str
    updated_at: str
    line_items_count: int
    tracking_numbers: list[str] = Field(default_factory=list)
    shipping_address_city: str | None = None
    shipping_address_country: str | None = None

    def get_status_summary(self) -> str:
        """Generate a human-readable status summary for the AI agent."""
        payment = "paid" if self.financial_status == "paid" else self.financial_status

        if self.fulfillment_status == "fulfilled":
            if self.tracking_numbers:
                tracking_str = ", ".join(self.tracking_numbers)
                return f"Payment: {payment}. Shipped! Tracking: {tracking_str}"
            return f"Payment: {payment}. Shipped!"
        elif self.fulfillment_status == "partial":
            return f"Payment: {payment}. Partially shipped."
        else:
            return f"Payment: {payment}. Order is being prepared for shipping."


# ============================================================================
# Tool Input Schemas
# ============================================================================


class ProductSearchInput(BaseModel):
    """Input schema for product search tool."""

    product_name: str = Field(
        ...,
        description="The product name or search query",
        min_length=1,
        max_length=200,
    )


class OrderStatusInput(BaseModel):
    """Input schema for order status tool."""

    order_id: str = Field(
        ...,
        description="The order ID or order number (e.g., '12345' or '#1001')",
        min_length=1,
        max_length=50,
    )
