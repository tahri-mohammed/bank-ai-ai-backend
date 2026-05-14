import requests
from app.providers.base_provider import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "qwen2.5-coder:1.5b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "")
