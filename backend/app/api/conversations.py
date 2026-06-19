from fastapi import APIRouter, HTTPException
from .. import storage

router = APIRouter()


@router.post("/")
async def create_chat(payload: dict):
    try:
        chat_id = storage.save_chat("anon", payload)
        return {"chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_chats():
    return {"chats": storage.list_chats("anon")}
