# Backend Constitution: FastAPI & Python

## 1. Key Files & Structure

- **`main.py`**: The FastAPI app entry point. Minimal logic here.
- **`routers/`**: API route handlers. Each file corresponds to a domain.
- **`services/`**: Business logic. This is where the core work happens.
- **`models/`**: SQLAlchemy database models.
- **`schemas.py`**: Pydantic models for request/response validation.
- **`dependencies.py`**: Reusable FastAPI dependencies.

## 2. Core Patterns & Standards

- **Dependency Injection:** Use FastAPI's dependency injection system for database sessions, authentication, and other shared resources.
- **Pydantic Everywhere:** All API requests and responses MUST be validated with Pydantic models defined in `schemas.py`.
- **Async/Await:** All database queries, external API calls, and other I/O-bound operations MUST use `async` and `await`.
- **Service Layer:** Business logic MUST reside in the `services/` layer. Router functions should be thin and only handle HTTP-related tasks.
- **Explicit Imports:** Use explicit imports to avoid naming conflicts (e.g., `from src.auth import service as auth_service`).
