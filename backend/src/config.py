"""Application configuration."""
import json
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_dm_automation"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS - accepts JSON string or comma-separated list
    cors_origins: list[str] = ["http://localhost:3000"]

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Instagram
    instagram_verify_token: str = ""
    instagram_app_secret: str = ""
    instagram_access_token: str = ""
    instagram_page_id: str = ""

    # AI Agent / LLM Configuration
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4.1-mini"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 500

    # Shopify E-commerce Configuration
    shopify_store_url: str = ""  # e.g., "mystore.myshopify.com"
    shopify_api_key: str = ""  # Shopify API key
    shopify_access_token: str = ""  # Admin API access token (shpat_xxx)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from JSON string or comma-separated list."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Try JSON first
            if v.startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Fall back to comma-separated
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return ["http://localhost:3000"]


settings = Settings()
