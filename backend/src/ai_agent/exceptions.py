"""Custom exceptions for the AI Agent domain."""


class AIAgentError(Exception):
    """Base exception for AI Agent-related errors."""

    pass


class IntentClassificationError(AIAgentError):
    """Raised when intent classification fails."""

    pass


class ResponseGenerationError(AIAgentError):
    """Raised when response generation fails."""

    pass


class AgentProcessingError(AIAgentError):
    """Raised when the overall agent processing fails."""

    pass


class LLMConnectionError(AIAgentError):
    """Raised when connection to the LLM fails."""

    pass
