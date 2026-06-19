from typing import List, Dict
from .providers.openai import OpenAIProvider
from .providers.ollama import OllamaProvider
from .providers.hf_inference import HFInferenceProvider


def default_providers() -> List[Dict]:
    return [
        {"name": "openai", "instance": OpenAIProvider(), "tier": 1},
        {"name": "ollama", "instance": OllamaProvider(), "tier": 2},
        {"name": "hf_inference", "instance": HFInferenceProvider(), "tier": 3},
    ]
