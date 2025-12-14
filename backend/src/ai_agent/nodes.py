"""LangGraph node functions for the AI Agent."""

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.ai_agent.prompts import (
    EXTRACT_ORDER_ID_PROMPT,
    EXTRACT_PRODUCT_QUERY_PROMPT,
    FALLBACK_RESPONSE,
    INTENT_CLASSIFICATION_PROMPT,
    RESPONSE_GENERATION_PROMPT,
    TOOL_RESPONSE_GENERATION_PROMPT,
)
from src.ai_agent.schemas import AgentState, MessageIntent
from src.config import settings
from src.ecommerce.tools import check_order_status, get_product_info

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


async def call_tools(state: AgentState) -> dict[str, list[str] | str | None]:
    """
    Call the appropriate e-commerce tool based on the classified intent.

    This node extracts the relevant information from the user's message
    and invokes the corresponding tool to retrieve product or order data.

    Args:
        state: Current agent state with intent already classified

    Returns:
        Updated state fields with tool_results
    """
    intent = state.get("intent")
    message = state["current_message"]

    try:
        llm = get_llm()

        if intent == MessageIntent.PRODUCT_INQUIRY:
            # Extract product search term from message
            prompt = EXTRACT_PRODUCT_QUERY_PROMPT.format(message=message)
            response = await llm.ainvoke([SystemMessage(content=prompt)])
            search_term = response.content.strip() if isinstance(response.content, str) else str(response.content).strip()

            logger.info(f"Calling get_product_info with search term: {search_term}")
            result = await get_product_info.ainvoke(search_term)

            return {
                "tool_results": [result],
                "error": None,
            }

        elif intent == MessageIntent.ORDER_STATUS:
            # Extract order ID from message
            prompt = EXTRACT_ORDER_ID_PROMPT.format(message=message)
            response = await llm.ainvoke([SystemMessage(content=prompt)])
            order_id = response.content.strip() if isinstance(response.content, str) else str(response.content).strip()

            if order_id.lower() == "unknown":
                return {
                    "tool_results": [
                        "I couldn't find an order number in your message. "
                        "Could you please provide your order number? "
                        "It should be in your confirmation email (e.g., #1001)."
                    ],
                    "error": None,
                }

            logger.info(f"Calling check_order_status with order ID: {order_id}")
            result = await check_order_status.ainvoke(order_id)

            return {
                "tool_results": [result],
                "error": None,
            }

        else:
            # No tool call needed for this intent
            logger.warning(f"call_tools invoked with unexpected intent: {intent}")
            return {
                "tool_results": [],
                "error": None,
            }

    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return {
            "tool_results": [
                "I encountered an issue while looking up that information. "
                "Please try again or a team member will assist you."
            ],
            "error": f"Tool error: {str(e)}",
        }


async def generate_response(state: AgentState) -> dict[str, str | list[dict[str, str]] | None]:
    """
    Generate a response based on the classified intent and any tool results.

    This node uses the LLM to create an appropriate response for the user.
    If tool results are available, they are incorporated into the response.

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

        # Check if we have tool results to incorporate
        tool_results = state.get("tool_results", [])
        if tool_results:
            # Use tool-aware prompt when we have tool results
            tool_results_text = "\n\n".join(tool_results)
            prompt = TOOL_RESPONSE_GENERATION_PROMPT.format(
                intent=intent_value,
                message=state["current_message"],
                tool_results=tool_results_text,
                history=history,
            )
            logger.info(f"Generating response with tool results for sender {state['sender_id']}")
        else:
            # Use standard prompt when no tool results
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
