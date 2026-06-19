from typing import List, Dict


def compact_conversation(messages: List[Dict], max_messages: int = 10) -> str:
    # naive compaction: keep last `max_messages` messages and join text
    recent = messages[-max_messages:]
    parts = []
    for m in recent:
        role = m.get("role", "user")
        text = m.get("text", "")
        parts.append(f"[{role}] {text}")
    return "\n".join(parts)
