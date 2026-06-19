from time import time
from typing import Dict

_metrics: Dict[str, int] = {
    "executions_total": 0,
    "executions_success": 0,
    "executions_failure": 0,
}


def incr(name: str, amt: int = 1):
    if name not in _metrics:
        _metrics[name] = 0
    _metrics[name] += amt


def snapshot():
    return {**_metrics, "timestamp": int(time())}
