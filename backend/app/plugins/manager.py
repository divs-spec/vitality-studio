import os
import json
from typing import Dict, List

PLUGINS_DIR = os.environ.get("VITALITY_PLUGINS_DIR") or os.path.join(os.getcwd(), "plugins")


class PluginManager:
    def __init__(self, plugins_dir: str = None):
        self.plugins_dir = plugins_dir or PLUGINS_DIR
        os.makedirs(self.plugins_dir, exist_ok=True)
        self._registry: Dict[str, Dict] = {}

    def discover(self) -> List[str]:
        items = []
        for name in os.listdir(self.plugins_dir):
            p = os.path.join(self.plugins_dir, name)
            if os.path.isdir(p):
                items.append(name)
        return items

    def load_metadata(self, plugin_name: str) -> Dict:
        meta_file = os.path.join(self.plugins_dir, plugin_name, "plugin.json")
        if not os.path.exists(meta_file):
            raise FileNotFoundError(meta_file)
        with open(meta_file, "r", encoding="utf-8") as f:
            m = json.load(f)
        self._registry[plugin_name] = m
        return m

    def list_plugins(self) -> Dict[str, Dict]:
        # lazy load metadata
        for name in self.discover():
            if name not in self._registry:
                try:
                    self.load_metadata(name)
                except Exception:
                    self._registry[name] = {"error": "invalid plugin"}
        return self._registry
