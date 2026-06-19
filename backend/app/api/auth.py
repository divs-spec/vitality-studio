from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..auth import create_user, authenticate_user

router = APIRouter()


class RegisterPayload(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(payload: RegisterPayload):
    try:
        user = create_user(payload.email, payload.password)
        return {"user_id": user["id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class LoginPayload(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(payload: LoginPayload):
    token = authenticate_user(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}
