"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_dm_automation"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
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

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
