"""Tests for the Shopify e-commerce integration."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.ai_agent.graph import build_agent_graph, get_agent, reset_agent
from src.ai_agent.nodes import call_tools, generate_response
from src.ai_agent.schemas import AgentState, MessageIntent
from src.ecommerce.client import ShopifyClient
from src.ecommerce.exceptions import (
    OrderNotFoundError,
    ProductNotFoundError,
    ShopifyAPIError,
    ShopifyRateLimitError,
)
from src.ecommerce.schemas import (
    OrderStatusResult,
    ProductSearchResult,
)
from src.ecommerce.tools import check_order_status, get_product_info


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def mock_shopify_settings():
    """Mock Shopify configuration settings."""
    with patch("src.ecommerce.client.settings") as mock_settings:
        mock_settings.shopify_store_url = "test-store.myshopify.com"
        mock_settings.shopify_api_key = "test_api_key"
        mock_settings.shopify_access_token = "shpat_test_token"
        yield mock_settings


@pytest.fixture
def sample_product_response():
    """Sample Shopify product API response."""
    return {
        "products": [
            {
                "id": 12345,
                "title": "Classic T-Shirt",
                "body_html": "<p>A comfortable cotton t-shirt</p>",
                "vendor": "Test Brand",
                "product_type": "Apparel",
                "handle": "classic-t-shirt",
                "status": "active",
                "variants": [
                    {
                        "id": 67890,
                        "product_id": 12345,
                        "title": "Small / Black",
                        "price": "29.99",
                        "sku": "TSHIRT-S-BLK",
                        "inventory_quantity": 50,
                        "option1": "Small",
                        "option2": "Black",
                    }
                ],
                "images": [
                    {
                        "id": 11111,
                        "product_id": 12345,
                        "src": "https://cdn.shopify.com/test-image.jpg",
                        "alt": "Classic T-Shirt",
                        "position": 1,
                    }
                ],
            },
            {
                "id": 12346,
                "title": "Premium T-Shirt",
                "body_html": "<p>Premium quality cotton t-shirt</p>",
                "vendor": "Test Brand",
                "product_type": "Apparel",
                "handle": "premium-t-shirt",
                "status": "active",
                "variants": [
                    {
                        "id": 67891,
                        "product_id": 12346,
                        "title": "Medium / White",
                        "price": "39.99",
                        "sku": "TSHIRT-M-WHT",
                        "inventory_quantity": 25,
                        "option1": "Medium",
                        "option2": "White",
                    }
                ],
                "images": [],
            },
        ]
    }


@pytest.fixture
def sample_order_response():
    """Sample Shopify order API response."""
    return {
        "orders": [
            {
                "id": 98765,
                "name": "#1001",
                "email": "customer@example.com",
                "financial_status": "paid",
                "fulfillment_status": "fulfilled",
                "total_price": "59.98",
                "currency": "USD",
                "created_at": "2024-01-15T10:30:00-05:00",
                "updated_at": "2024-01-16T14:00:00-05:00",
                "line_items": [
                    {"id": 1, "title": "Classic T-Shirt", "quantity": 2, "price": "29.99"}
                ],
                "fulfillments": [
                    {
                        "id": 55555,
                        "order_id": 98765,
                        "status": "success",
                        "tracking_number": "1Z999AA10123456784",
                        "tracking_url": "https://ups.com/track/1Z999AA10123456784",
                        "tracking_company": "UPS",
                    }
                ],
                "shipping_address": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "city": "New York",
                    "country": "United States",
                    "zip": "10001",
                },
            }
        ]
    }


@pytest.fixture
def sample_order_unfulfilled_response():
    """Sample Shopify order API response for unfulfilled order."""
    return {
        "orders": [
            {
                "id": 98766,
                "name": "#1002",
                "email": "customer2@example.com",
                "financial_status": "paid",
                "fulfillment_status": None,
                "total_price": "29.99",
                "currency": "USD",
                "created_at": "2024-01-17T10:30:00-05:00",
                "updated_at": "2024-01-17T10:30:00-05:00",
                "line_items": [
                    {"id": 2, "title": "Premium T-Shirt", "quantity": 1, "price": "29.99"}
                ],
                "fulfillments": [],
                "shipping_address": {
                    "city": "Los Angeles",
                    "country": "United States",
                },
            }
        ]
    }


@pytest.fixture
def empty_product_response():
    """Empty product search response."""
    return {"products": []}


@pytest.fixture
def empty_order_response():
    """Empty order search response."""
    return {"orders": []}


@pytest.fixture
def initial_state_product_inquiry() -> AgentState:
    """Create initial state for product inquiry."""
    return AgentState(
        sender_id="user_123",
        recipient_id="page_456",
        current_message="Do you have any t-shirts?",
        intent=MessageIntent.PRODUCT_INQUIRY,
        confidence=0.95,
        messages=[],
        response=None,
        tool_results=[],
        error=None,
    )


@pytest.fixture
def initial_state_order_status() -> AgentState:
    """Create initial state for order status inquiry."""
    return AgentState(
        sender_id="user_123",
        recipient_id="page_456",
        current_message="What is the status of order #1001?",
        intent=MessageIntent.ORDER_STATUS,
        confidence=0.92,
        messages=[],
        response=None,
        tool_results=[],
        error=None,
    )


@pytest.fixture(autouse=True)
def reset_agent_graph():
    """Reset the agent graph before each test."""
    reset_agent()


# ============================================================================
# ShopifyClient Unit Tests
# ============================================================================


@pytest.mark.asyncio
async def test_shopify_client_context_manager_required():
    """Test that ShopifyClient must be used as context manager."""
    client = ShopifyClient(
        store_url="test.myshopify.com",
        api_key="test_key",
        access_token="shpat_test",
    )

    with pytest.raises(RuntimeError) as exc_info:
        client._get_client()

    assert "async context manager" in str(exc_info.value)


@pytest.mark.asyncio
async def test_shopify_client_search_products_success(
    mock_shopify_settings,
    sample_product_response,
):
    """Test successful product search."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_product_response
    mock_response.headers = {"X-Shopify-Shop-Api-Call-Limit": "5/40"}

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.aclose = AsyncMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        async with ShopifyClient() as client:
            client._client = mock_client_instance
            products = await client.search_products("t-shirt", limit=3)

        assert len(products) == 2
        assert products[0].title == "Classic T-Shirt"
        assert products[0].price == "29.99"
        assert products[0].available is True
        assert products[0].inventory_quantity == 50


@pytest.mark.asyncio
async def test_shopify_client_search_products_empty(
    mock_shopify_settings,
    empty_product_response,
):
    """Test product search with no results."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = empty_product_response
    mock_response.headers = {}

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.aclose = AsyncMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        async with ShopifyClient() as client:
            client._client = mock_client_instance
            products = await client.search_products("nonexistent product")

        assert len(products) == 0


@pytest.mark.asyncio
async def test_shopify_client_get_order_status_success(
    mock_shopify_settings,
    sample_order_response,
):
    """Test successful order status retrieval."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_order_response
    mock_response.headers = {}

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.aclose = AsyncMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        async with ShopifyClient() as client:
            client._client = mock_client_instance
            order = await client.get_order_status("#1001")

        assert order.order_number == "#1001"
        assert order.financial_status == "paid"
        assert order.fulfillment_status == "fulfilled"
        assert order.tracking_numbers == ["1Z999AA10123456784"]
        assert order.shipping_address_city == "New York"


@pytest.mark.asyncio
async def test_shopify_client_get_order_status_not_found(
    mock_shopify_settings,
    empty_order_response,
):
    """Test order status retrieval when order not found."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = empty_order_response
    mock_response.headers = {}

    mock_404_response = MagicMock()
    mock_404_response.status_code = 404
    mock_404_response.json.return_value = {"errors": "Not Found"}
    mock_404_response.headers = {}

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = [mock_response, mock_404_response]
        mock_client_instance.aclose = AsyncMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        async with ShopifyClient() as client:
            client._client = mock_client_instance
            with pytest.raises(OrderNotFoundError):
                await client.get_order_status("99999")


@pytest.mark.asyncio
async def test_shopify_client_rate_limit_error(mock_shopify_settings):
    """Test handling of rate limit errors."""
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.headers = {"Retry-After": "2.0"}

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.aclose = AsyncMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        async with ShopifyClient() as client:
            client._client = mock_client_instance
            with pytest.raises(ShopifyRateLimitError) as exc_info:
                await client.search_products("test")

        assert exc_info.value.retry_after == 2.0
        assert exc_info.value.status_code == 429


@pytest.mark.asyncio
async def test_shopify_client_api_error(mock_shopify_settings):
    """Test handling of generic API errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"errors": "Internal Server Error"}
    mock_response.text = "Internal Server Error"
    mock_response.headers = {}

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.aclose = AsyncMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        async with ShopifyClient() as client:
            client._client = mock_client_instance
            with pytest.raises(ShopifyAPIError) as exc_info:
                await client.search_products("test")

        assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_shopify_client_clean_html():
    """Test HTML cleaning function."""
    client = ShopifyClient(
        store_url="test.myshopify.com",
        api_key="test",
        access_token="test",
    )

    assert client._clean_html("<p>Hello <b>World</b></p>") == "Hello World"
    assert client._clean_html(None) == ""
    assert client._clean_html("") == ""
    assert client._clean_html("Plain text") == "Plain text"


# ============================================================================
# Tool Tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_product_info_tool_success(
    mock_shopify_settings,
    sample_product_response,
):
    """Test get_product_info tool with successful search."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = sample_product_response
    mock_response.headers = {}

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client_instance.aclose = AsyncMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=None)

        with patch("src.ecommerce.tools.ShopifyClient") as MockShopifyClient:
            mock_shopify_instance = AsyncMock()
            mock_shopify_instance.search_products.return_value = [
                ProductSearchResult(
                    id="12345",
                    title="Classic T-Shirt",
                    description="A comfortable cotton t-shirt",
                    price="29.99",
                    currency="USD",
                    inventory_quantity=50,
                    available=True,
                    image_url="https://cdn.shopify.com/test-image.jpg",
                    handle="classic-t-shirt",
                    vendor="Test Brand",
                )
            ]
            MockShopifyClient.return_value.__aenter__ = AsyncMock(
                return_value=mock_shopify_instance
            )
            MockShopifyClient.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await get_product_info.ainvoke("t-shirt")

        assert "Classic T-Shirt" in result
        assert "$29.99" in result
        assert "In Stock" in result


@pytest.mark.asyncio
async def test_get_product_info_tool_not_found(mock_shopify_settings):
    """Test get_product_info tool when no products found."""
    with patch("src.ecommerce.tools.ShopifyClient") as MockShopifyClient:
        mock_shopify_instance = AsyncMock()
        mock_shopify_instance.search_products.return_value = []
        MockShopifyClient.return_value.__aenter__ = AsyncMock(
            return_value=mock_shopify_instance
        )
        MockShopifyClient.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await get_product_info.ainvoke("nonexistent product")

    assert "couldn't find any products" in result.lower()


@pytest.mark.asyncio
async def test_get_product_info_tool_rate_limit(mock_shopify_settings):
    """Test get_product_info tool handling rate limit."""
    with patch("src.ecommerce.tools.ShopifyClient") as MockShopifyClient:
        mock_shopify_instance = AsyncMock()
        mock_shopify_instance.search_products.side_effect = ShopifyRateLimitError(
            "Rate limit exceeded", status_code=429, retry_after=2.0
        )
        MockShopifyClient.return_value.__aenter__ = AsyncMock(
            return_value=mock_shopify_instance
        )
        MockShopifyClient.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await get_product_info.ainvoke("test")

    assert "try again" in result.lower()


@pytest.mark.asyncio
async def test_check_order_status_tool_success(
    mock_shopify_settings,
):
    """Test check_order_status tool with successful lookup."""
    with patch("src.ecommerce.tools.ShopifyClient") as MockShopifyClient:
        mock_shopify_instance = AsyncMock()
        mock_shopify_instance.get_order_status.return_value = OrderStatusResult(
            order_id="98765",
            order_number="#1001",
            email="customer@example.com",
            financial_status="paid",
            fulfillment_status="fulfilled",
            total_price="59.98",
            currency="USD",
            created_at="2024-01-15T10:30:00-05:00",
            updated_at="2024-01-16T14:00:00-05:00",
            line_items_count=2,
            tracking_numbers=["1Z999AA10123456784"],
            shipping_address_city="New York",
            shipping_address_country="United States",
        )
        MockShopifyClient.return_value.__aenter__ = AsyncMock(
            return_value=mock_shopify_instance
        )
        MockShopifyClient.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await check_order_status.ainvoke("#1001")

    assert "#1001" in result
    assert "$59.98" in result
    assert "Shipped" in result
    assert "1Z999AA10123456784" in result


@pytest.mark.asyncio
async def test_check_order_status_tool_not_found(mock_shopify_settings):
    """Test check_order_status tool when order not found."""
    with patch("src.ecommerce.tools.ShopifyClient") as MockShopifyClient:
        mock_shopify_instance = AsyncMock()
        mock_shopify_instance.get_order_status.side_effect = OrderNotFoundError(
            "Order not found", status_code=404
        )
        MockShopifyClient.return_value.__aenter__ = AsyncMock(
            return_value=mock_shopify_instance
        )
        MockShopifyClient.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await check_order_status.ainvoke("#99999")

    assert "couldn't find" in result.lower()
    assert "order" in result.lower()


@pytest.mark.asyncio
async def test_check_order_status_tool_rate_limit(mock_shopify_settings):
    """Test check_order_status tool handling rate limit."""
    with patch("src.ecommerce.tools.ShopifyClient") as MockShopifyClient:
        mock_shopify_instance = AsyncMock()
        mock_shopify_instance.get_order_status.side_effect = ShopifyRateLimitError(
            "Rate limit exceeded", status_code=429, retry_after=2.0
        )
        MockShopifyClient.return_value.__aenter__ = AsyncMock(
            return_value=mock_shopify_instance
        )
        MockShopifyClient.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await check_order_status.ainvoke("#1001")

    assert "try again" in result.lower()


# ============================================================================
# Schema Tests
# ============================================================================


def test_product_search_result_schema():
    """Test ProductSearchResult schema validation."""
    result = ProductSearchResult(
        id="12345",
        title="Test Product",
        description="A test product description",
        price="29.99",
        currency="USD",
        inventory_quantity=10,
        available=True,
        image_url="https://example.com/image.jpg",
        handle="test-product",
        vendor="Test Vendor",
    )

    assert result.id == "12345"
    assert result.title == "Test Product"
    assert result.price == "29.99"
    assert result.available is True


def test_order_status_result_schema():
    """Test OrderStatusResult schema validation."""
    result = OrderStatusResult(
        order_id="12345",
        order_number="#1001",
        email="test@example.com",
        financial_status="paid",
        fulfillment_status="fulfilled",
        total_price="49.99",
        currency="USD",
        created_at="2024-01-15T10:00:00Z",
        updated_at="2024-01-16T10:00:00Z",
        line_items_count=2,
        tracking_numbers=["TRACK123"],
        shipping_address_city="New York",
        shipping_address_country="United States",
    )

    assert result.order_number == "#1001"
    assert result.financial_status == "paid"
    assert result.line_items_count == 2


def test_order_status_get_summary_fulfilled():
    """Test OrderStatusResult.get_status_summary for fulfilled order."""
    result = OrderStatusResult(
        order_id="12345",
        order_number="#1001",
        email="test@example.com",
        financial_status="paid",
        fulfillment_status="fulfilled",
        total_price="49.99",
        currency="USD",
        created_at="2024-01-15T10:00:00Z",
        updated_at="2024-01-16T10:00:00Z",
        line_items_count=1,
        tracking_numbers=["1Z999AA1"],
    )

    summary = result.get_status_summary()
    assert "paid" in summary.lower()
    assert "shipped" in summary.lower()
    assert "1Z999AA1" in summary


def test_order_status_get_summary_unfulfilled():
    """Test OrderStatusResult.get_status_summary for unfulfilled order."""
    result = OrderStatusResult(
        order_id="12345",
        order_number="#1001",
        email="test@example.com",
        financial_status="paid",
        fulfillment_status="unfulfilled",
        total_price="49.99",
        currency="USD",
        created_at="2024-01-15T10:00:00Z",
        updated_at="2024-01-16T10:00:00Z",
        line_items_count=1,
        tracking_numbers=[],
    )

    summary = result.get_status_summary()
    assert "paid" in summary.lower()
    assert "prepared" in summary.lower() or "shipping" in summary.lower()


def test_order_status_get_summary_partial():
    """Test OrderStatusResult.get_status_summary for partially fulfilled order."""
    result = OrderStatusResult(
        order_id="12345",
        order_number="#1001",
        email="test@example.com",
        financial_status="paid",
        fulfillment_status="partial",
        total_price="99.99",
        currency="USD",
        created_at="2024-01-15T10:00:00Z",
        updated_at="2024-01-16T10:00:00Z",
        line_items_count=3,
        tracking_numbers=[],
    )

    summary = result.get_status_summary()
    assert "paid" in summary.lower()
    assert "partial" in summary.lower()


# ============================================================================
# Node Tests (call_tools and generate_response with tool results)
# ============================================================================


@pytest.mark.asyncio
async def test_call_tools_product_inquiry(
    initial_state_product_inquiry,
    mock_shopify_settings,
):
    """Test call_tools node for product inquiry."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(content="t-shirts")
        mock_get_llm.return_value = mock_llm

        with patch("src.ai_agent.nodes.get_product_info") as mock_tool:
            mock_tool.ainvoke = AsyncMock(return_value="Product: Classic T-Shirt - $29.99")

            result = await call_tools(initial_state_product_inquiry)

    assert len(result["tool_results"]) == 1
    assert "Classic T-Shirt" in result["tool_results"][0]
    assert result["error"] is None


@pytest.mark.asyncio
async def test_call_tools_order_status(
    initial_state_order_status,
    mock_shopify_settings,
):
    """Test call_tools node for order status."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(content="#1001")
        mock_get_llm.return_value = mock_llm

        with patch("src.ai_agent.nodes.check_order_status") as mock_tool:
            mock_tool.ainvoke = AsyncMock(return_value="Order #1001: Shipped!")

            result = await call_tools(initial_state_order_status)

    assert len(result["tool_results"]) == 1
    assert "#1001" in result["tool_results"][0]
    assert result["error"] is None


@pytest.mark.asyncio
async def test_call_tools_order_status_unknown_order_id(
    initial_state_order_status,
    mock_shopify_settings,
):
    """Test call_tools node when order ID cannot be extracted."""
    initial_state_order_status["current_message"] = "What's the status of my order?"

    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(content="unknown")
        mock_get_llm.return_value = mock_llm

        result = await call_tools(initial_state_order_status)

    assert len(result["tool_results"]) == 1
    assert "order number" in result["tool_results"][0].lower()
    assert result["error"] is None


@pytest.mark.asyncio
async def test_call_tools_handles_exception(
    initial_state_product_inquiry,
    mock_shopify_settings,
):
    """Test call_tools node exception handling."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = Exception("LLM failed")
        mock_get_llm.return_value = mock_llm

        result = await call_tools(initial_state_product_inquiry)

    assert len(result["tool_results"]) == 1
    assert "encountered an issue" in result["tool_results"][0].lower()
    assert result["error"] is not None


@pytest.mark.asyncio
async def test_generate_response_with_tool_results(
    initial_state_product_inquiry,
):
    """Test generate_response incorporates tool results."""
    initial_state_product_inquiry["tool_results"] = [
        "**Classic T-Shirt**\n- Price: $29.99 USD\n- Status: In Stock"
    ]

    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content="Great news! We have the Classic T-Shirt in stock for $29.99!"
        )
        mock_get_llm.return_value = mock_llm

        result = await generate_response(initial_state_product_inquiry)

    assert result["response"] is not None
    assert result["error"] is None


# ============================================================================
# Integration Tests (Agent with Tools)
# ============================================================================


@pytest.mark.asyncio
async def test_agent_graph_includes_call_tools_node():
    """Test that the agent graph includes the call_tools node."""
    graph = build_agent_graph()

    assert "call_tools" in graph.nodes
    assert "classify_intent" in graph.nodes
    assert "generate_response" in graph.nodes
    assert "handle_error" in graph.nodes


@pytest.mark.asyncio
async def test_agent_processes_product_inquiry_with_tools(mock_shopify_settings):
    """Test full agent flow with product inquiry triggering tools."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = [
            # Classification response
            MagicMock(content='{"intent": "product_inquiry", "confidence": 0.95}'),
            # Product query extraction
            MagicMock(content="t-shirts"),
            # Response generation
            MagicMock(content="We have great t-shirts! The Classic T-Shirt is $29.99 and in stock."),
        ]
        mock_get_llm.return_value = mock_llm

        with patch("src.ai_agent.nodes.get_product_info") as mock_tool:
            mock_tool.ainvoke = AsyncMock(
                return_value="**Classic T-Shirt**\n- Price: $29.99 USD\n- Status: In Stock"
            )

            agent = get_agent()

            result = await agent.ainvoke(
                {
                    "sender_id": "user_123",
                    "recipient_id": "page_456",
                    "current_message": "Do you have any t-shirts?",
                    "intent": None,
                    "confidence": 0.0,
                    "messages": [],
                    "response": None,
                    "tool_results": [],
                    "error": None,
                }
            )

    assert result["intent"] == MessageIntent.PRODUCT_INQUIRY
    assert result["response"] is not None
    assert len(result["tool_results"]) == 1


@pytest.mark.asyncio
async def test_agent_processes_order_status_with_tools(mock_shopify_settings):
    """Test full agent flow with order status triggering tools."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = [
            # Classification response
            MagicMock(content='{"intent": "order_status", "confidence": 0.92}'),
            # Order ID extraction
            MagicMock(content="#1001"),
            # Response generation
            MagicMock(content="Your order #1001 has been shipped! Tracking: 1Z999AA1"),
        ]
        mock_get_llm.return_value = mock_llm

        with patch("src.ai_agent.nodes.check_order_status") as mock_tool:
            mock_tool.ainvoke = AsyncMock(
                return_value="**Order #1001**\n- Shipped! Tracking: 1Z999AA10123456784"
            )

            agent = get_agent()

            result = await agent.ainvoke(
                {
                    "sender_id": "user_123",
                    "recipient_id": "page_456",
                    "current_message": "Where is my order #1001?",
                    "intent": None,
                    "confidence": 0.0,
                    "messages": [],
                    "response": None,
                    "tool_results": [],
                    "error": None,
                }
            )

    assert result["intent"] == MessageIntent.ORDER_STATUS
    assert result["response"] is not None
    assert len(result["tool_results"]) == 1


@pytest.mark.asyncio
async def test_agent_greeting_bypasses_tools():
    """Test that greeting intent bypasses tool calling."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = [
            # Classification response
            MagicMock(content='{"intent": "greeting", "confidence": 0.98}'),
            # Response generation (no tool extraction call)
            MagicMock(content="Hello! How can I help you today?"),
        ]
        mock_get_llm.return_value = mock_llm

        agent = get_agent()

        result = await agent.ainvoke(
            {
                "sender_id": "user_123",
                "recipient_id": "page_456",
                "current_message": "Hi there!",
                "intent": None,
                "confidence": 0.0,
                "messages": [],
                "response": None,
                "tool_results": [],
                "error": None,
            }
        )

    assert result["intent"] == MessageIntent.GREETING
    assert result["response"] == "Hello! How can I help you today?"
    assert result["tool_results"] == []  # No tools called


@pytest.mark.asyncio
async def test_agent_general_question_bypasses_tools():
    """Test that general question intent bypasses tool calling."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = [
            # Classification response
            MagicMock(content='{"intent": "general_question", "confidence": 0.90}'),
            # Response generation
            MagicMock(content="Our store hours are 9 AM to 6 PM, Monday through Saturday."),
        ]
        mock_get_llm.return_value = mock_llm

        agent = get_agent()

        result = await agent.ainvoke(
            {
                "sender_id": "user_123",
                "recipient_id": "page_456",
                "current_message": "What are your store hours?",
                "intent": None,
                "confidence": 0.0,
                "messages": [],
                "response": None,
                "tool_results": [],
                "error": None,
            }
        )

    assert result["intent"] == MessageIntent.GENERAL_QUESTION
    assert "store hours" in result["response"].lower()
    assert result["tool_results"] == []


# ============================================================================
# Exception Tests
# ============================================================================


def test_shopify_api_error_includes_status_code():
    """Test ShopifyAPIError includes status code."""
    error = ShopifyAPIError("Test error", status_code=500)
    assert error.status_code == 500
    assert "Test error" in str(error)


def test_shopify_rate_limit_error_includes_retry_after():
    """Test ShopifyRateLimitError includes retry_after."""
    error = ShopifyRateLimitError("Rate limited", status_code=429, retry_after=2.5)
    assert error.status_code == 429
    assert error.retry_after == 2.5


def test_product_not_found_error():
    """Test ProductNotFoundError."""
    error = ProductNotFoundError("Product not found", status_code=404)
    assert error.status_code == 404
    assert "Product not found" in str(error)


def test_order_not_found_error():
    """Test OrderNotFoundError."""
    error = OrderNotFoundError("Order not found", status_code=404)
    assert error.status_code == 404
    assert "Order not found" in str(error)
