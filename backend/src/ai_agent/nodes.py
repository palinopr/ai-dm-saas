"""LangGraph node functions for the AI Agent."""

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.ai_agent.prompts import (
    FALLBACK_RESPONSE,
    INTENT_CLASSIFICATION_PROMPT,
    RESPONSE_GENERATION_PROMPT,
)
from src.ai_agent.schemas import AgentState, MessageIntent
from src.config import settings

logger = logging.getLogger(__name__)


def get_llm() -> ChatOpenAI:
    """
    Create and configure the LLM instance.

    Returns:
        Configured ChatOpenAI instance
    """
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_api_base,
        temperature=settings.openai_temperature,
        max_tokens=settings.openai_max_tokens,
    )


async def classify_intent(state: AgentState) -> dict[str, MessageIntent | float | str | None]:
    """
    Classify the intent of the current message.

    This node uses the LLM to determine what the user wants based on their message.

    Args:
        state: Current agent state

    Returns:
        Updated state fields with intent and confidence
    """
    try:
        llm = get_llm()
        prompt = INTENT_CLASSIFICATION_PROMPT.format(message=state["current_message"])

        response = await llm.ainvoke([SystemMessage(content=prompt)])

        # Parse JSON response from LLM
        content = response.content
        if isinstance(content, str):
            # Clean up response if needed (remove markdown code blocks if present)
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            result = json.loads(content)
            intent = MessageIntent(result["intent"])
            confidence = float(result["confidence"])

            logger.info(
                f"Classified intent for sender {state['sender_id']}: "
                f"{intent.value} (confidence: {confidence:.2f})"
            )

            return {
                "intent": intent,
                "confidence": confidence,
                "error": None,
            }

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse intent classification response: {e}")
        return {
            "intent": MessageIntent.UNKNOWN,
            "confidence": 0.0,
            "error": f"Classification parse error: {str(e)}",
        }
    except ValueError as e:
        logger.error(f"Invalid intent value: {e}")
        return {
            "intent": MessageIntent.UNKNOWN,
            "confidence": 0.0,
            "error": f"Invalid intent: {str(e)}",
        }
    except Exception as e:
        logger.error(f"Intent classification failed: {e}")
        return {
            "intent": MessageIntent.UNKNOWN,
            "confidence": 0.0,
            "error": f"Classification error: {str(e)}",
        }


async def generate_response(state: AgentState) -> dict[str, str | list[dict[str, str]] | None]:
    """
    Generate a response based on the classified intent.

    This node uses the LLM to create an appropriate response for the user.

    Args:
        state: Current agent state with intent already classified

    Returns:
        Updated state fields with response and updated messages
    """
    try:
        llm = get_llm()

        # Format conversation history
        history_messages = state.get("messages", [])
        if history_messages:
            history = "\n".join(
                [f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" for msg in history_messages[-5:]]
            )
        else:
            history = "No previous messages"

        intent_value = state["intent"].value if state["intent"] else "unknown"
        prompt = RESPONSE_GENERATION_PROMPT.format(
            intent=intent_value,
            message=state["current_message"],
            history=history,
        )

        response = await llm.ainvoke([SystemMessage(content=prompt)])

        response_text = response.content if isinstance(response.content, str) else str(response.content)

        # Update messages with the new exchange
        updated_messages = list(state.get("messages", []))
        updated_messages.append({"role": "user", "content": state["current_message"]})
        updated_messages.append({"role": "assistant", "content": response_text})

        logger.info(f"Generated response for sender {state['sender_id']} (intent: {intent_value})")

        return {
            "response": response_text,
            "messages": updated_messages,
            "error": None,
        }

    except Exception as e:
        logger.error(f"Response generation failed: {e}")
        return {
            "response": FALLBACK_RESPONSE,
            "error": f"Generation error: {str(e)}",
        }


async def handle_error(state: AgentState) -> dict[str, str]:
    """
    Handle errors that occurred during processing.

    Provides a graceful fallback response when something goes wrong.

    Args:
        state: Current agent state with error information

    Returns:
        Updated state with fallback response
    """
    error_msg = state.get("error", "Unknown error")
    logger.error(f"Error in agent pipeline for sender {state['sender_id']}: {error_msg}")

    return {
        "response": FALLBACK_RESPONSE,
    }
