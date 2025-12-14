"""AI Agent domain for LangGraph-based message processing."""

from src.ai_agent.exceptions import (
    AgentProcessingError,
    AIAgentError,
    IntentClassificationError,
    LLMConnectionError,
    ResponseGenerationError,
)
from src.ai_agent.schemas import (
    AgentState,
    MessageIntent,
    ProcessMessageRequest,
    ProcessMessageResponse,
)
from src.ai_agent.service import process_message, process_message_with_context

__all__ = [
    # Exceptions
    "AIAgentError",
    "IntentClassificationError",
    "ResponseGenerationError",
    "AgentProcessingError",
    "LLMConnectionError",
    # Schemas
    "MessageIntent",
    "AgentState",
    "ProcessMessageRequest",
    "ProcessMessageResponse",
    # Service functions
    "process_message",
    "process_message_with_context",
]
