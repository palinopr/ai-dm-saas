"""LangGraph tools for Shopify e-commerce operations."""

import logging
from typing import Annotated

from langchain_core.tools import tool

from src.ecommerce.client import ShopifyClient
from src.ecommerce.exceptions import (
    OrderNotFoundError,
    ProductNotFoundError,
    ShopifyAPIError,
    ShopifyRateLimitError,
)

logger = logging.getLogger(__name__)


@tool
async def get_product_info(
    product_name: Annotated[str, "The name of the product to search for"],
) -> str:
    """
    Search for products by name and return their details.

    Use this tool when a customer asks about a specific product,
    wants to know prices, availability, or product details.

    Args:
        product_name: The name or description of the product to search for

    Returns:
        A formatted string with product information or an error message
    """
    logger.info(f"Tool: get_product_info called with: {product_name}")

    try:
        async with ShopifyClient() as client:
            products = await client.search_products(product_name, limit=3)

        if not products:
            return (
                f"I couldn't find any products matching '{product_name}'. "
                "Could you provide more details or try a different search term?"
            )

        # Format results for the LLM
        results = []
        for product in products:
            availability = "In Stock" if product.available else "Out of Stock"
            result = (
                f"**{product.title}**\n"
                f"- Price: ${product.price} {product.currency}\n"
                f"- Status: {availability}"
            )
            if product.inventory_quantity > 0:
                result += f" ({product.inventory_quantity} available)"
            if product.description:
                # Truncate description if too long
                desc = (
                    product.description[:200] + "..."
                    if len(product.description) > 200
                    else product.description
                )
                result += f"\n- Description: {desc}"
            results.append(result)

        return "\n\n".join(results)

    except ShopifyRateLimitError:
        logger.warning("Shopify rate limit hit in get_product_info")
        return (
            "I'm having trouble accessing product information right now. "
            "Please try again in a moment."
        )
    except ShopifyAPIError as e:
        logger.error(f"Shopify API error in get_product_info: {e}")
        return (
            "I couldn't retrieve product information at this time. "
            "A team member can help you with this."
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_product_info: {e}")
        return (
            "I encountered an issue while looking up that product. "
            "Please try again or ask a team member."
        )


@tool
async def check_order_status(
    order_id: Annotated[str, "The order ID or order number (e.g., '12345' or '#1001')"],
) -> str:
    """
    Check the status of an order by order ID or order number.

    Use this tool when a customer asks about their order status,
    shipping updates, or tracking information.

    Args:
        order_id: The order ID or order number (can include # prefix)

    Returns:
        A formatted string with order status or an error message
    """
    logger.info(f"Tool: check_order_status called with: {order_id}")

    try:
        async with ShopifyClient() as client:
            order = await client.get_order_status(order_id)

        # Format the response
        status_summary = order.get_status_summary()

        result = (
            f"**Order {order.order_number}**\n"
            f"- {status_summary}\n"
            f"- Total: ${order.total_price} {order.currency}\n"
            f"- Items: {order.line_items_count} item(s)"
        )

        if order.shipping_address_city and order.shipping_address_country:
            result += (
                f"\n- Shipping to: {order.shipping_address_city}, "
                f"{order.shipping_address_country}"
            )

        return result

    except OrderNotFoundError:
        return (
            f"I couldn't find an order with ID '{order_id}'. "
            "Please double-check the order number and try again. "
            "It should be in your confirmation email."
        )
    except ShopifyRateLimitError:
        logger.warning("Shopify rate limit hit in check_order_status")
        return (
            "I'm having trouble accessing order information right now. "
            "Please try again in a moment."
        )
    except ShopifyAPIError as e:
        logger.error(f"Shopify API error in check_order_status: {e}")
        return (
            "I couldn't retrieve your order information at this time. "
            "A team member will be able to help you."
        )
    except Exception as e:
        logger.error(f"Unexpected error in check_order_status: {e}")
        return (
            "I encountered an issue while looking up your order. "
            "Please try again or contact our support team."
        )


# Export tools list for use in the agent
ECOMMERCE_TOOLS = [get_product_info, check_order_status]
