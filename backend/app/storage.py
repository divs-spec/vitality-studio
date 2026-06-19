import os
import json
import uuid
from datetime import datetime

BASE = os.environ.get("VITALITY_STORAGE_BASE") or os.path.join(os.getcwd(), "storage", "users")


def ensure_user_dir(user_id: str) -> str:
    path = os.path.join(BASE, user_id)
    os.makedirs(path, exist_ok=True)
    return path


def save_chat(user_id: str, chat_obj: dict) -> str:
    path = ensure_user_dir(user_id)
    chat_id = chat_obj.get("chat_id") or f"chat_{uuid.uuid4().hex[:8]}"
    filename = os.path.join(path, f"{chat_id}.json")
    meta = dict(chat_obj)
    meta.setdefault("chat_id", chat_id)
    meta.setdefault("created_at", datetime.utcnow().isoformat() + "Z")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    return chat_id


def list_chats(user_id: str):
    path = ensure_user_dir(user_id)
    files = []
    for fname in os.listdir(path):
        if fname.endswith(".json"):
            files.append(fname)
    return files


def load_chat(user_id: str, chat_id: str):
    path = ensure_user_dir(user_id)
    filename = os.path.join(path, f"{chat_id}.json")
    if not os.path.exists(filename):
        raise FileNotFoundError(chat_id)
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_chat(user_id: str, chat_id: str) -> bool:
    path = ensure_user_dir(user_id)
    filename = os.path.join(path, f"{chat_id}.json")
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False


def append_message(user_id: str, chat_id: str, message: dict):
    data = load_chat(user_id, chat_id)
    msgs = data.get("messages") or []
    msgs.append(message)
    data["messages"] = msgs
    path = ensure_user_dir(user_id)
    filename = os.path.join(path, f"{chat_id}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return True
