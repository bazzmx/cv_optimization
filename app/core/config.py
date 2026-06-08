from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.
    LLM settings and Chroma vector store settings are defined in a .env. Otherwise, we assume that there is
    a local Ollama server running with a Gemma model.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    LLM_PROVIDER: str = "ollama"

    OPENAI_API_KEY: str | None = None
    OPENAI_LLM_MODEL: str = "gpt-4o-mini"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_LLM_MODEL: str = "gemma4:e2b-mlx"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False
    LOG_BACKTRACE: bool = True

    CHROMA_PATH: str | None = None

    @property
    def chroma_path(self) -> str:
        if self.CHROMA_PATH:
            return self.CHROMA_PATH

        return str(Path.cwd() / "chroma_db")


settings = Settings()
