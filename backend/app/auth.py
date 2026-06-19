import os
import json
import uuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

PWD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# allow overriding the users file path for tests/dev
USERS_FILE = os.environ.get("VITALITY_USERS_FILE") or os.path.join(os.getcwd(), "backend", "app", "users.json")
SECRET = os.environ.get("VITALITY_SECRET", "dev-secret")


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(d):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)


def create_user(email, password):
    users = load_users()
    if email in users:
        raise Exception("User exists")
    user_id = str(uuid.uuid4())
    users[email] = {
        "id": user_id,
        "email": email,
        "pw": PWD_CONTEXT.hash(password),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    save_users(users)
    return users[email]


def authenticate_user(email, password):
    users = load_users()
    u = users.get(email)
    if not u:
        return None
    if not PWD_CONTEXT.verify(password, u["pw"]):
        return None
    payload = {"sub": u["id"], "exp": int((datetime.utcnow() + timedelta(hours=6)).timestamp())}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token


def verify_token(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data.get("sub")
    except Exception:
        return None
