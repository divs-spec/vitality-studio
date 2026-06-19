from .base import BaseProvider


class OllamaProvider(BaseProvider):
    async def generate(self, prompt: str, **kwargs):
        return {"provider": "ollama", "response": f"Ollama echo: {prompt}"}
