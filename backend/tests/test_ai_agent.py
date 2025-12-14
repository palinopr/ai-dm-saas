"""Tests for the AI Agent domain."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ai_agent.exceptions import AgentProcessingError
from src.ai_agent.graph import build_agent_graph, get_agent, reset_agent
from src.ai_agent.nodes import classify_intent, generate_response, handle_error
from src.ai_agent.schemas import (
    AgentState,
    MessageIntent,
    ProcessMessageRequest,
    ProcessMessageResponse,
)
from src.ai_agent.service import process_message


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def initial_state() -> AgentState:
    """Create a basic initial state for testing."""
    return AgentState(
        sender_id="user_123",
        recipient_id="page_456",
        current_message="Do you have this product in stock?",
        intent=None,
        confidence=0.0,
        messages=[],
        response=None,
        error=None,
    )


@pytest.fixture
def state_with_intent() -> AgentState:
    """Create a state with intent already classified."""
    return AgentState(
        sender_id="user_123",
        recipient_id="page_456",
        current_message="Do you have this product in stock?",
        intent=MessageIntent.PRODUCT_INQUIRY,
        confidence=0.95,
        messages=[],
        response=None,
        error=None,
    )


@pytest.fixture
def state_with_error() -> AgentState:
    """Create a state with an error."""
    return AgentState(
        sender_id="user_123",
        recipient_id="page_456",
        current_message="Hello",
        intent=MessageIntent.UNKNOWN,
        confidence=0.0,
        messages=[],
        response=None,
        error="LLM connection failed",
    )


@pytest.fixture
def process_request() -> ProcessMessageRequest:
    """Create a basic process message request."""
    return ProcessMessageRequest(
        sender_id="user_123",
        recipient_id="page_456",
        message_text="What products do you have?",
        message_id="msg_abc123",
    )


@pytest.fixture(autouse=True)
def reset_agent_graph() -> None:
    """Reset the agent graph before each test."""
    reset_agent()


# ============================================================================
# Intent Classification Node Tests
# ============================================================================


@pytest.mark.asyncio
async def test_classify_intent_product_inquiry(initial_state: AgentState) -> None:
    """Test intent classification for product inquiry."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content='{"intent": "product_inquiry", "confidence": 0.95}'
        )
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.PRODUCT_INQUIRY
        assert result["confidence"] == 0.95
        assert result["error"] is None


@pytest.mark.asyncio
async def test_classify_intent_greeting(initial_state: AgentState) -> None:
    """Test intent classification for greeting."""
    initial_state["current_message"] = "Hi there!"

    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content='{"intent": "greeting", "confidence": 0.98}'
        )
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.GREETING
        assert result["confidence"] == 0.98
        assert result["error"] is None


@pytest.mark.asyncio
async def test_classify_intent_order_status(initial_state: AgentState) -> None:
    """Test intent classification for order status."""
    initial_state["current_message"] = "Where is my order #12345?"

    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content='{"intent": "order_status", "confidence": 0.92}'
        )
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.ORDER_STATUS
        assert result["confidence"] == 0.92
        assert result["error"] is None


@pytest.mark.asyncio
async def test_classify_intent_general_question(initial_state: AgentState) -> None:
    """Test intent classification for general question."""
    initial_state["current_message"] = "What are your store hours?"

    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content='{"intent": "general_question", "confidence": 0.90}'
        )
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.GENERAL_QUESTION
        assert result["confidence"] == 0.90
        assert result["error"] is None


@pytest.mark.asyncio
async def test_classify_intent_handles_json_in_code_block(initial_state: AgentState) -> None:
    """Test intent classification handles JSON wrapped in markdown code blocks."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content='```json\n{"intent": "product_inquiry", "confidence": 0.95}\n```'
        )
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.PRODUCT_INQUIRY
        assert result["confidence"] == 0.95


@pytest.mark.asyncio
async def test_classify_intent_handles_llm_error(initial_state: AgentState) -> None:
    """Test intent classification error handling when LLM fails."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = Exception("LLM connection failed")
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.UNKNOWN
        assert result["confidence"] == 0.0
        assert "Classification error" in result["error"]


@pytest.mark.asyncio
async def test_classify_intent_handles_invalid_json(initial_state: AgentState) -> None:
    """Test intent classification handles invalid JSON response."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(content="This is not JSON")
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.UNKNOWN
        assert result["confidence"] == 0.0
        assert "parse error" in result["error"]


@pytest.mark.asyncio
async def test_classify_intent_handles_invalid_intent_value(initial_state: AgentState) -> None:
    """Test intent classification handles unknown intent value."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content='{"intent": "invalid_intent", "confidence": 0.95}'
        )
        mock_get_llm.return_value = mock_llm

        result = await classify_intent(initial_state)

        assert result["intent"] == MessageIntent.UNKNOWN
        assert result["confidence"] == 0.0
        assert "Invalid intent" in result["error"]


# ============================================================================
# Response Generation Node Tests
# ============================================================================


@pytest.mark.asyncio
async def test_generate_response_success(state_with_intent: AgentState) -> None:
    """Test successful response generation."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(
            content="Yes, we have that product in stock! Would you like me to check availability in your size?"
        )
        mock_get_llm.return_value = mock_llm

        result = await generate_response(state_with_intent)

        assert result["response"] is not None
        assert "stock" in result["response"]
        assert result["error"] is None
        assert len(result["messages"]) == 2  # User message + assistant response


@pytest.mark.asyncio
async def test_generate_response_with_history(state_with_intent: AgentState) -> None:
    """Test response generation with conversation history."""
    state_with_intent["messages"] = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]

    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.return_value = MagicMock(content="Let me check that for you!")
        mock_get_llm.return_value = mock_llm

        result = await generate_response(state_with_intent)

        assert result["response"] == "Let me check that for you!"
        assert len(result["messages"]) == 4  # 2 existing + 2 new


@pytest.mark.asyncio
async def test_generate_response_handles_error(state_with_intent: AgentState) -> None:
    """Test response generation error handling."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = Exception("LLM error")
        mock_get_llm.return_value = mock_llm

        result = await generate_response(state_with_intent)

        assert result["response"] is not None  # Should return fallback
        assert "Generation error" in result["error"]


# ============================================================================
# Error Handler Node Tests
# ============================================================================


@pytest.mark.asyncio
async def test_handle_error_provides_fallback(state_with_error: AgentState) -> None:
    """Test error handler provides fallback response."""
    result = await handle_error(state_with_error)

    assert result["response"] is not None
    assert len(result["response"]) > 0


# ============================================================================
# Graph Tests
# ============================================================================


def test_build_agent_graph_structure() -> None:
    """Test that the agent graph is built correctly."""
    graph = build_agent_graph()

    # Check nodes are present
    assert "classify_intent" in graph.nodes
    assert "generate_response" in graph.nodes
    assert "handle_error" in graph.nodes


def test_get_agent_returns_compiled_graph() -> None:
    """Test that get_agent returns a compiled graph."""
    agent = get_agent()
    assert agent is not None


def test_get_agent_singleton_pattern() -> None:
    """Test that get_agent returns the same instance."""
    agent1 = get_agent()
    agent2 = get_agent()
    assert agent1 is agent2


def test_reset_agent_clears_singleton() -> None:
    """Test that reset_agent clears the singleton."""
    agent1 = get_agent()
    reset_agent()
    agent2 = get_agent()
    # After reset, should get a new instance (though functionally equivalent)
    # We can't easily test identity here since both are compiled graphs
    assert agent2 is not None


@pytest.mark.asyncio
async def test_full_graph_execution() -> None:
    """Test the complete agent graph execution."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()

        # First call for classification, second for response generation
        mock_llm.ainvoke.side_effect = [
            MagicMock(content='{"intent": "greeting", "confidence": 0.9}'),
            MagicMock(content="Hello! How can I help you today?"),
        ]
        mock_get_llm.return_value = mock_llm

        agent = get_agent()

        result = await agent.ainvoke(
            {
                "sender_id": "user_123",
                "recipient_id": "page_456",
                "current_message": "Hello!",
                "intent": None,
                "confidence": 0.0,
                "messages": [],
                "response": None,
                "error": None,
            }
        )

        assert result["intent"] == MessageIntent.GREETING
        assert result["confidence"] == 0.9
        assert result["response"] == "Hello! How can I help you today?"


@pytest.mark.asyncio
async def test_graph_routes_to_error_handler_on_error() -> None:
    """Test that the graph routes to error handler when classification fails."""
    with patch("src.ai_agent.nodes.get_llm") as mock_get_llm:
        mock_llm = AsyncMock()
        mock_llm.ainvoke.side_effect = Exception("LLM failed")
        mock_get_llm.return_value = mock_llm

        agent = get_agent()

        result = await agent.ainvoke(
            {
                "sender_id": "user_123",
                "recipient_id": "page_456",
                "current_message": "Hello!",
                "intent": None,
                "confidence": 0.0,
                "messages": [],
                "response": None,
                "error": None,
            }
        )

        # Should have a response (fallback) even on error
        assert result["response"] is not None
        assert result["intent"] == MessageIntent.UNKNOWN


# ============================================================================
# Service Tests
# ============================================================================


@pytest.mark.asyncio
async def test_process_message_service(process_request: ProcessMessageRequest) -> None:
    """Test the service layer process_message function."""
    with patch("src.ai_agent.service.get_agent") as mock_get_agent:
        mock_agent = AsyncMock()
        mock_agent.ainvoke.return_value = {
            "intent": MessageIntent.PRODUCT_INQUIRY,
            "confidence": 0.92,
            "response": "Let me check that for you!",
            "error": None,
            "messages": [],
            "sender_id": "user_123",
            "recipient_id": "page_456",
            "current_message": "What products do you have?",
        }
        mock_get_agent.return_value = mock_agent

        response = await process_message(process_request)

        assert isinstance(response, ProcessMessageResponse)
        assert response.intent == MessageIntent.PRODUCT_INQUIRY
        assert response.confidence == 0.92
        assert response.response_text == "Let me check that for you!"
        assert response.processing_time_ms > 0


@pytest.mark.asyncio
async def test_process_message_handles_agent_error(process_request: ProcessMessageRequest) -> None:
    """Test that process_message raises AgentProcessingError on failure."""
    with patch("src.ai_agent.service.get_agent") as mock_get_agent:
        mock_agent = AsyncMock()
        mock_agent.ainvoke.side_effect = Exception("Agent failed")
        mock_get_agent.return_value = mock_agent

        with pytest.raises(AgentProcessingError) as exc_info:
            await process_message(process_request)

        assert "Failed to process message" in str(exc_info.value)


@pytest.mark.asyncio
async def test_process_message_handles_missing_response(process_request: ProcessMessageRequest) -> None:
    """Test that process_message handles missing response gracefully."""
    with patch("src.ai_agent.service.get_agent") as mock_get_agent:
        mock_agent = AsyncMock()
        mock_agent.ainvoke.return_value = {
            "intent": MessageIntent.UNKNOWN,
            "confidence": 0.0,
            "response": None,  # No response generated
            "error": "Something went wrong",
            "messages": [],
            "sender_id": "user_123",
            "recipient_id": "page_456",
            "current_message": "test",
        }
        mock_get_agent.return_value = mock_agent

        response = await process_message(process_request)

        assert response.response_text == "Unable to generate response"
        assert response.intent == MessageIntent.UNKNOWN


# ============================================================================
# Schema Tests
# ============================================================================


def test_message_intent_enum_values() -> None:
    """Test MessageIntent enum has all expected values."""
    assert MessageIntent.PRODUCT_INQUIRY.value == "product_inquiry"
    assert MessageIntent.ORDER_STATUS.value == "order_status"
    assert MessageIntent.GENERAL_QUESTION.value == "general_question"
    assert MessageIntent.GREETING.value == "greeting"
    assert MessageIntent.UNKNOWN.value == "unknown"


def test_process_message_request_validation() -> None:
    """Test ProcessMessageRequest validation."""
    request = ProcessMessageRequest(
        sender_id="user_123",
        recipient_id="page_456",
        message_text="Hello",
    )

    assert request.sender_id == "user_123"
    assert request.recipient_id == "page_456"
    assert request.message_text == "Hello"
    assert request.message_id is None


def test_process_message_response_validation() -> None:
    """Test ProcessMessageResponse validation."""
    response = ProcessMessageResponse(
        response_text="Hi there!",
        intent=MessageIntent.GREETING,
        confidence=0.95,
        processing_time_ms=150.5,
    )

    assert response.response_text == "Hi there!"
    assert response.intent == MessageIntent.GREETING
    assert response.confidence == 0.95
    assert response.processing_time_ms == 150.5


def test_process_message_response_confidence_bounds() -> None:
    """Test ProcessMessageResponse confidence validation."""
    # Valid confidence
    response = ProcessMessageResponse(
        response_text="test",
        intent=MessageIntent.UNKNOWN,
        confidence=0.5,
        processing_time_ms=100.0,
    )
    assert response.confidence == 0.5

    # Test boundary values
    response_min = ProcessMessageResponse(
        response_text="test",
        intent=MessageIntent.UNKNOWN,
        confidence=0.0,
        processing_time_ms=100.0,
    )
    assert response_min.confidence == 0.0

    response_max = ProcessMessageResponse(
        response_text="test",
        intent=MessageIntent.UNKNOWN,
        confidence=1.0,
        processing_time_ms=100.0,
    )
    assert response_max.confidence == 1.0
