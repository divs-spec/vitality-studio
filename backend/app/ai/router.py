import asyncio
from typing import List, Dict, Any, Optional
from .registry import default_providers
from .context import compact_conversation


class ModelRouter:
    def __init__(self, providers: Optional[List[Dict]] = None):
        self.providers = providers or default_providers()

    def _ordered_providers(self, preferred: Optional[str] = None) -> List[Dict]:
        # sort by tier ascending (1 = best)
        ordered = sorted(self.providers, key=lambda p: p.get("tier", 999))
        if preferred:
            # move preferred to front if present
            for i, p in enumerate(ordered):
                if p.get("name") == preferred:
                    ordered.insert(0, ordered.pop(i))
                    break
        return ordered

    async def generate(self, prompt: str, messages: Optional[List[Dict]] = None, preferred: Optional[str] = None) -> Dict[str, Any]:
        ordered = self._ordered_providers(preferred)
        switching_events = []
        for p in ordered:
            name = p.get("name")
            inst = p.get("instance")
            try:
                # If messages exist, compact and prepend
                if messages:
                    prompt = compact_conversation(messages) + "\n" + prompt
                resp = await inst.generate(prompt)
                return {"provider": name, "response": resp, "switching_events": switching_events}
            except Exception as e:
                switching_events.append({"from": name, "error": str(e)})
                # try next provider
                continue
        # if all failed
        raise RuntimeError("All providers failed")
