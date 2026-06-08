from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.core.logger import logger


def get_llm():
    """Get the LLM provider based on the settings."""
    provider = settings.LLM_PROVIDER.lower()
    logger.info(f"Using LLM provider: {provider}")

    if provider == "openai":
        return ChatOpenAI(
            model=settings.OPENAI_LLM_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY,
        )

    if provider == "ollama":
        return ChatOllama(
            model=settings.OLLAMA_LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")
