"""LangGraph graph construction for the AI Agent with tool support."""

import logging
from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.ai_agent.nodes import (
    call_tools,
    classify_intent,
    generate_response,
    handle_error,
)
from src.ai_agent.schemas import AgentState, MessageIntent

logger = logging.getLogger(__name__)


def should_use_tools(
    state: AgentState,
) -> Literal["call_tools", "generate_response", "handle_error"]:
    """
    Determine routing based on intent and error state.

    Routes to tools for PRODUCT_INQUIRY and ORDER_STATUS intents,
    directly to response generation for other intents.

    Args:
        state: Current agent state

    Returns:
        Next node name based on intent and error state
    """
    if state.get("error"):
        return "handle_error"

    intent = state.get("intent")

    # These intents require tool calls for e-commerce data
    if intent in (MessageIntent.PRODUCT_INQUIRY, MessageIntent.ORDER_STATUS):
        return "call_tools"

    return "generate_response"


def should_continue_after_tools(
    state: AgentState,
) -> Literal["generate_response", "handle_error"]:
    """
    Determine what to do after tools execute.

    Args:
        state: Current agent state

    Returns:
        Next node name based on error state
    """
    if state.get("error"):
        return "handle_error"
    return "generate_response"


def build_agent_graph() -> StateGraph:
    """
    Build the LangGraph agent with tool support for e-commerce operations.

    Graph structure:
        START -> classify_intent -> [conditional]
                                        |
                                        v (PRODUCT_INQUIRY, ORDER_STATUS)
                                   call_tools -> generate_response -> END
                                        |
                                        v (GREETING, GENERAL_QUESTION, UNKNOWN)
                                   generate_response -> END
                                        |
                                        v (error)
                                   handle_error -> END

    Returns:
        Constructed StateGraph (not yet compiled)
    """
    # Create the graph with our state schema
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("call_tools", call_tools)
    graph.add_node("generate_response", generate_response)
    graph.add_node("handle_error", handle_error)

    # Define edges
    graph.add_edge(START, "classify_intent")

    # Conditional routing after classification
    graph.add_conditional_edges(
        "classify_intent",
        should_use_tools,
        {
            "call_tools": "call_tools",
            "generate_response": "generate_response",
            "handle_error": "handle_error",
        },
    )

    # After tools, go to response generation
    graph.add_conditional_edges(
        "call_tools",
        should_continue_after_tools,
        {
            "generate_response": "generate_response",
            "handle_error": "handle_error",
        },
    )

    graph.add_edge("generate_response", END)
    graph.add_edge("handle_error", END)

    return graph


# Module-level compiled graph (singleton pattern)
_compiled_graph: CompiledStateGraph | None = None


def get_agent() -> CompiledStateGraph:
    """
    Get the compiled agent graph (singleton pattern).

    The graph is compiled once at first access and reused for performance.

    Returns:
        Compiled StateGraph ready for invocation
    """
    global _compiled_graph
    if _compiled_graph is None:
        logger.info("Compiling AI agent graph with tool support...")
        _compiled_graph = build_agent_graph().compile()
        logger.info("AI agent graph compiled successfully")
    return _compiled_graph


def reset_agent() -> None:
    """
    Reset the compiled agent graph.

    Useful for testing or when configuration changes require a fresh graph.
    """
    global _compiled_graph
    _compiled_graph = None
    logger.info("AI agent graph reset")
