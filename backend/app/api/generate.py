from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from ..ai.router import ModelRouter

router = APIRouter()


class GeneratePayload(BaseModel):
    prompt: str
    messages: Optional[List[Dict]] = None
    preferred: Optional[str] = None


@router.post("/")
async def generate(payload: GeneratePayload):
    try:
        router_svc = ModelRouter()
        res = await router_svc.generate(payload.prompt, messages=payload.messages, preferred=payload.preferred)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
