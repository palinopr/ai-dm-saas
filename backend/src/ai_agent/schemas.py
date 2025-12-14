"""Pydantic models and type definitions for the AI Agent domain."""

from enum import Enum
from typing import TypedDict

from pydantic import BaseModel, Field


class MessageIntent(str, Enum):
    """Classified intent of an incoming message."""

    PRODUCT_INQUIRY = "product_inquiry"
    ORDER_STATUS = "order_status"
    GENERAL_QUESTION = "general_question"
    GREETING = "greeting"
    UNKNOWN = "unknown"


class AgentState(TypedDict):
    """
    State that flows through the LangGraph nodes.

    This TypedDict defines the shape of data passed between nodes in the graph.
    """

    # Conversation context
    sender_id: str
    recipient_id: str

    # Current message being processed
    current_message: str

    # Classification result
    intent: MessageIntent | None
    confidence: float

    # Conversation history (list of message dicts)
    messages: list[dict[str, str]]

    # Generated response
    response: str | None

    # Tool results storage (for e-commerce tools)
    tool_results: list[str]

    # Error tracking
    error: str | None


class ProcessMessageRequest(BaseModel):
    """Request schema for processing an incoming message."""

    sender_id: str = Field(..., description="ID of the message sender")
    recipient_id: str = Field(..., description="ID of the message recipient (page)")
    message_text: str = Field(..., description="The text content of the message")
    message_id: str | None = Field(None, description="Optional Instagram message ID")


class ProcessMessageResponse(BaseModel):
    """Response schema from message processing."""

    response_text: str = Field(..., description="The generated response text")
    intent: MessageIntent = Field(..., description="Classified intent of the message")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
