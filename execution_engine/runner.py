from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from .orchestrator import run_in_container
from .metrics import incr, snapshot


app = FastAPI(title="Execution Runner")


class ExecPayload(BaseModel):
    language: str
    code: str


@app.post("/execute")
async def execute(payload: ExecPayload):
    # Run inside an ephemeral container using orchestrator
    start = datetime.utcnow()
    try:
        stdout, stderr, exit_code = run_in_container(payload.language, payload.code, timeout=15, cpus=0.5, memory="128m")
    except Exception as e:
        incr("executions_total")
        incr("executions_failure")
        return {"stdout": "", "stderr": str(e), "exit_code": 1, "runtime_seconds": 0.0, "timestamp": datetime.utcnow().isoformat() + "Z"}
    end = datetime.utcnow()
    incr("executions_total")
    if exit_code == 0:
        incr("executions_success")
    else:
        incr("executions_failure")
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "runtime_seconds": (end - start).total_seconds(),
        "timestamp": end.isoformat() + "Z",
    }


@app.get("/metrics")
async def metrics():
    return snapshot()


@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
