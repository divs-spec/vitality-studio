from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    async def generate(self, prompt: str, **kwargs):
        # Minimal stub for local testing — replace with real API calls.
        return {"provider": "openai", "response": f"Echo: {prompt}"}
