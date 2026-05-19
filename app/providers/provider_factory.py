import os
from dotenv import load_dotenv
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider

load_dotenv()


def get_provider():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "openai":
        return OpenAIProvider()

    return OllamaProvider()
