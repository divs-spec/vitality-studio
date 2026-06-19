from fastapi import FastAPI
from .api.conversations import router as conv_router
from .api.auth import router as auth_router
from .api.generate import router as gen_router
from .api.execute import router as exec_router
from .metrics import incr, snapshot

app = FastAPI(title="Vitality Studio API")

app.include_router(auth_router, prefix="/auth")
app.include_router(conv_router, prefix="/conversations")
app.include_router(gen_router, prefix="/generate")
app.include_router(exec_router, prefix="/execute")


@app.get("/metrics")
async def metrics():
    return snapshot()



@app.get("/health")
async def health():
    return {"status": "ok"}
