# Project Constitution: AI DM Automation SaaS

## 1. Core Mission

Our mission is to build a market-leading, AI-powered DM Automation SaaS for e-commerce businesses. The tool will integrate with Instagram, TikTok, and WhatsApp to provide intelligent, automated sales and support conversations.

## 2. Tech Stack

- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** FastAPI (Python 3.11), LangGraph
- **Database:** PostgreSQL (via Supabase)
- **Cache:** Redis (via Upstash)
- **Deployment:** Railway (Backend), Vercel (Frontend)
- **Local Development:** Docker Compose

## 3. Architectural Principles

1.  **Monorepo:** The entire project (frontend and backend) lives in a single repository to provide complete context.
2.  **Domain-Driven Design:** The codebase is organized by business domains (e.g., `instagram`, `ai_agent`, `ecommerce`), not by file types. Each domain is self-contained.
3.  **Separation of Concerns:** A strict separation is maintained between the API layer (routers), business logic (services), and data layer (models).
4.  **Test-Driven Development (TDD):** All new features must be accompanied by comprehensive unit and integration tests. YOU MUST write tests before or alongside the implementation.

## 4. Core Principles & Coding Standards

- **Strong Typing:** All code, both Python and TypeScript, MUST be strongly typed. No `any` types are permitted.
- **No Secrets in Code:** API keys, database URLs, and other secrets MUST be loaded from environment variables. Never commit them to the repository.
- **Clear Commit Messages:** Follow the Conventional Commits specification (e.g., `feat:`, `fix:`, `docs:`).
- **Asynchronous Backend:** All I/O operations in the backend (database calls, API requests) MUST be `async`.
- **Immutable Frontend State:** Frontend state should be treated as immutable. Use state management libraries correctly to handle updates.

## 5. Development Commands

- `docker-compose up --build`: Start all services for local development.
- `cd frontend && npm run dev`: Start the frontend development server.
- `cd backend && uvicorn src.main:app --reload`: Start the backend development server.
