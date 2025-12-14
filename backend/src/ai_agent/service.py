"""Service layer for the AI Agent domain."""

import logging
import time

from src.ai_agent.exceptions import AgentProcessingError
from src.ai_agent.graph import get_agent
from src.ai_agent.schemas import (
    AgentState,
    MessageIntent,
    ProcessMessageRequest,
    ProcessMessageResponse,
)

logger = logging.getLogger(__name__)


async def process_message(request: ProcessMessageRequest) -> ProcessMessageResponse:
    """
    Process an incoming message through the AI agent.

    This is the main entry point for external callers (like the Instagram webhook).

    Args:
        request: The message processing request containing sender info and message text

    Returns:
        ProcessMessageResponse with the generated reply and metadata

    Raises:
        AgentProcessingError: If processing fails
    """
    start_time = time.time()

    try:
        agent = get_agent()

        # Prepare initial state
        initial_state: AgentState = {
            "sender_id": request.sender_id,
            "recipient_id": request.recipient_id,
            "current_message": request.message_text,
            "intent": None,
            "confidence": 0.0,
            "messages": [],
            "response": None,
            "error": None,
        }

        # Run the agent graph
        result = await agent.ainvoke(initial_state)

        processing_time = (time.time() - start_time) * 1000

        logger.info(
            f"Processed message for {request.sender_id} "
            f"(intent: {result.get('intent')}, time: {processing_time:.2f}ms)"
        )

        return ProcessMessageResponse(
            response_text=result.get("response") or "Unable to generate response",
            intent=result.get("intent") or MessageIntent.UNKNOWN,
            confidence=result.get("confidence", 0.0),
            processing_time_ms=processing_time,
        )

    except Exception as e:
        logger.error(f"Agent processing failed for {request.sender_id}: {e}")
        raise AgentProcessingError(f"Failed to process message: {str(e)}") from e


async def process_message_with_context(
    request: ProcessMessageRequest,
    conversation_history: list[dict[str, str]],
) -> ProcessMessageResponse:
    """
    Process a message with existing conversation history.

    Use this for multi-turn conversations where context matters.

    Args:
        request: The message processing request
        conversation_history: List of previous messages as dicts with 'role' and 'content'

    Returns:
        ProcessMessageResponse with the generated reply and metadata

    Raises:
        AgentProcessingError: If processing fails
    """
    start_time = time.time()

    try:
        agent = get_agent()

        initial_state: AgentState = {
            "sender_id": request.sender_id,
            "recipient_id": request.recipient_id,
            "current_message": request.message_text,
            "intent": None,
            "confidence": 0.0,
            "messages": conversation_history,
            "response": None,
            "error": None,
        }

        result = await agent.ainvoke(initial_state)

        processing_time = (time.time() - start_time) * 1000

        logger.info(
            f"Processed message with context for {request.sender_id} "
            f"(intent: {result.get('intent')}, history_len: {len(conversation_history)}, "
            f"time: {processing_time:.2f}ms)"
        )

        return ProcessMessageResponse(
            response_text=result.get("response") or "Unable to generate response",
            intent=result.get("intent") or MessageIntent.UNKNOWN,
            confidence=result.get("confidence", 0.0),
            processing_time_ms=processing_time,
        )

    except Exception as e:
        logger.error(f"Agent processing with context failed for {request.sender_id}: {e}")
        raise AgentProcessingError(f"Failed to process message: {str(e)}") from e
