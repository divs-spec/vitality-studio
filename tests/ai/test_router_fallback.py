import os
import sys
import unittest
import asyncio

sys.path.insert(0, os.path.abspath(os.getcwd()))

from backend.app.ai.router import ModelRouter
from backend.app.ai.providers.base import BaseProvider


class FailProvider(BaseProvider):
    def __init__(self, name="fail"):
        self.name = name

    async def generate(self, prompt: str, **kwargs):
        raise RuntimeError("simulated failure")


class OkProvider(BaseProvider):
    def __init__(self, name="ok"):
        self.name = name

    async def generate(self, prompt: str, **kwargs):
        return {"provider": self.name, "response": f"ok:{prompt}"}


class RouterFallbackTest(unittest.TestCase):
    def test_router_fallback(self):
        async def run():
            p_fail = {"name": "fail", "instance": FailProvider("fail"), "tier": 1}
            p_ok = {"name": "ok", "instance": OkProvider("ok"), "tier": 2}
            router = ModelRouter(providers=[p_fail, p_ok])
            res = await router.generate("hello world", preferred="fail")
            return res

        res = asyncio.run(run())
        # fallback should return the ok provider's response
        self.assertEqual(res.get("provider"), "ok")
        events = res.get("switching_events") or []
        self.assertTrue(any("fail" in e.get("from") for e in events))


if __name__ == "__main__":
    unittest.main()
