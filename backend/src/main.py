"""FastAPI application entry point."""
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# Log startup
logger.info("Starting AI DM Automation API...")

try:
    from src.auth.router import router as auth_router
    from src.config import settings
    from src.conversations.router import router as conversations_router
    from src.instagram.router import router as instagram_router
    logger.info("All imports successful")
    logger.info(f"CORS origins configured: {settings.cors_origins}")
except Exception as e:
    logger.error(f"Failed to import modules: {e}")
    raise

app = FastAPI(
    title="AI DM Automation API",
    description="AI-powered DM Automation SaaS for e-commerce businesses",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(conversations_router)
app.include_router(instagram_router)

logger.info("FastAPI app configured successfully")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/health/db")
async def db_health_check() -> dict[str, str]:
    """Database health check endpoint."""
    from sqlalchemy import text
    from src.database import async_session_maker

    try:
        async with async_session_maker() as session:
            result = await session.execute(text("SELECT 1"))
            result.scalar()

            # Check if users table exists
            table_check = await session.execute(
                text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
            )
            users_exists = table_check.scalar()

            return {
                "status": "healthy",
                "database": "connected",
                "users_table": "exists" if users_exists else "missing"
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "unhealthy", "database": "error", "error": str(e)}


@app.on_event("startup")
async def startup_event() -> None:
    """Log when the application starts."""
    logger.info("Application startup complete - ready to serve requests")
