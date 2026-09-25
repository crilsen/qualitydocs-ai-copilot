"""Backend settings. No secrets logged. Full document content never logged."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20240620"
    llm_provider: str = "auto"  # auto | anthropic | local
    database_url: str = "sqlite:///./app.db"
    max_upload_mb: int = 15
    allowed_extensions: str = ".pdf,.docx"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
