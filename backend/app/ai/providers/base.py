from typing import Any, Dict


class BaseProvider:
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError()
