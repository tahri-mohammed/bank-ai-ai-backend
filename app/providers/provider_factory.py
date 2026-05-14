import os
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider


def get_provider():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "openai":
        return OpenAIProvider()

    return OllamaProvider()
