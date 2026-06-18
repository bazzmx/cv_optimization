import pytest
from unittest.mock import patch
from app.infra.llm.provider import get_llm


@patch("app.infra.llm.provider.ChatOpenAI")
def test_get_llm_openai(mock_openai, monkeypatch):

    monkeypatch.setattr(
        "app.core.config.settings.LLM_PROVIDER",
        "openai",
    )

    get_llm()

    mock_openai.assert_called_once()


@patch("app.infra.llm.provider.ChatOllama")
def test_get_llm_ollama(mock_ollama, monkeypatch):

    monkeypatch.setattr(
        "app.core.config.settings.LLM_PROVIDER",
        "ollama",
    )

    get_llm()

    mock_ollama.assert_called_once()


def test_get_llm_invalid_provider(monkeypatch):

    monkeypatch.setattr(
        "app.core.config.settings.LLM_PROVIDER",
        "foo",
    )

    with pytest.raises(ValueError):
        get_llm()
