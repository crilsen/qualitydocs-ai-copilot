"""Backend settings. No secrets logged. Full document content never logged."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Provider selection: auto | anthropic | openai | gemini | compat | local
    llm_provider: str = "auto"

    # Anthropic Claude
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20240620"

    # OpenAI (GPT / Codex models)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Google Gemini (GEMINI_API_KEY or GOOGLE_API_KEY)
    gemini_api_key: str = ""
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # OpenAI-compatible endpoint (OpenCode gateway, OpenRouter, Ollama, vLLM, ...)
    compat_base_url: str = ""
    compat_api_key: str = ""
    compat_model: str = ""

    database_url: str = "sqlite:///./app.db"
    max_upload_mb: int = 15
    allowed_extensions: str = ".pdf,.docx"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
