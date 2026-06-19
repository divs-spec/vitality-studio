from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import httpx

router = APIRouter()


class ExecutePayload(BaseModel):
    language: str
    code: str


@router.post("/")
async def execute(payload: ExecutePayload):
    executor_url = os.environ.get("VITALITY_EXECUTOR_URL", "http://execution:9000/execute")
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(executor_url, json=payload.dict(), timeout=30.0)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Execution service error: {e}")
