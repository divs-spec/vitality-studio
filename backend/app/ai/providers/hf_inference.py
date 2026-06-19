from .base import BaseProvider


class HFInferenceProvider(BaseProvider):
    async def generate(self, prompt: str, **kwargs):
        return {"provider": "hf_inference", "response": f"HF echo: {prompt}"}
