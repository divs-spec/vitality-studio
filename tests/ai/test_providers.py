import os
import sys
import unittest
import asyncio

sys.path.insert(0, os.path.abspath(os.getcwd()))

from backend.app.ai.providers.openai import OpenAIProvider
from backend.app.ai.providers.ollama import OllamaProvider
from backend.app.ai.providers.hf_inference import HFInferenceProvider


class ProvidersTest(unittest.TestCase):
    def test_providers_generate(self):
        async def run_all():
            p1 = OpenAIProvider()
            p2 = OllamaProvider()
            p3 = HFInferenceProvider()
            r1 = await p1.generate("hello")
            r2 = await p2.generate("hello")
            r3 = await p3.generate("hello")
            return r1, r2, r3

        r1, r2, r3 = asyncio.run(run_all())
        self.assertEqual(r1.get("provider"), "openai")
        self.assertEqual(r2.get("provider"), "ollama")
        self.assertEqual(r3.get("provider"), "hf_inference")


if __name__ == "__main__":
    unittest.main()
