from typing import Dict
from time import time

_metrics: Dict[str, int] = {
    "requests_total": 0,
    "generate_requests": 0,
    "execute_requests": 0,
}


def incr(name: str, amt: int = 1):
    if name not in _metrics:
        _metrics[name] = 0
    _metrics[name] += amt


def snapshot():
    # return metrics in simple JSON form; can be adapted to Prometheus exposition
    return {**_metrics, "timestamp": int(time())}
