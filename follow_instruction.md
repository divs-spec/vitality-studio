# Vitality Studio — Run & Test Instructions

This file contains step-by-step commands to run the backend, frontend, unit tests, integration tests, Docker Compose stack, and health checks. Run commands from the project root (the folder that contains `backend/`, `frontend/`, `docker/`, `execution_engine/`, `tests/`).

Prerequisites
- Python 3.12+ and `pip` (project uses virtualenv recommended)
- Node.js 18+ and `npm` (for frontend)
- Docker & Docker Compose (for containers and integration tests)
- On Windows, run PowerShell with administrative privileges when installing Docker

Environment variables (optional)
- `VITALITY_STORAGE_BASE` — override storage base directory
- `VITALITY_EXECUTOR_URL` — override executor URL (backend uses this for `/execute` proxy)
- `REMOTE_DOCKER_HOST` — if set, orchestrator uses a remote Docker API endpoint (e.g. `tcp://host:2375`)

1) Setup Python virtual environment and install dependencies

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Unix/macOS:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Run unit tests

Run all unit tests (fast):
```bash
python -m unittest discover -s tests -v
```

Notes:
- Unit tests exercise backend modules and many use mocks; they do NOT require Docker.

3) Run backend locally (development)

Start the FastAPI backend with uvicorn (from project root, venv active):
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check (backend):
```bash
curl http://localhost:8000/health
```
Expected output (JSON):
```json
{"status":"ok"}
```

Metrics endpoint (JSON snapshot):
```bash
curl http://localhost:8000/metrics
```
Example output includes counts and timestamp (JSON).

4) Run frontend (development)

Open a separate terminal, then:
```bash
cd frontend
npm install
npm run dev
```

The dev server listens on port 5173 by default. Open http://localhost:5173

To run Electron (after building frontend):
```bash
cd frontend
npm run build
npm run start
```

5) Run execution service locally (dev)

The execution service provides an HTTP API to run code (in containers). To run locally (development):
```bash
# from the project root
uvicorn execution_engine.runner:app --reload --host 0.0.0.0 --port 9000
```

Health check (executor):
```bash
curl http://localhost:9000/health
```
Expected output:
```json
{"status":"ok"}
```

Metrics endpoint (executor):
```bash
curl http://localhost:9000/metrics
```
Example output includes `executions_total`, `executions_success`, `executions_failure`, and a timestamp.

6) Run full local stack with Docker Compose

This will build backend and execution images, run the frontend dev container (node), and a Prometheus stub.

```powershell
# from project root
docker compose -f docker/docker-compose.yml up --build
```

After compose starts:
- Backend: http://localhost:8000
- Frontend dev: http://localhost:5173
- Execution service: http://localhost:9000
- Prometheus UI: http://localhost:9090

Health checks (example):
```bash
curl http://localhost:8000/health     # backend
curl http://localhost:9000/health     # execution
```

Expected responses:
```json
{"status":"ok"}
```

7) Build backend Docker image only

If Docker is available locally you can build the backend image manually:
```powershell
# from project root
docker build -t vitality-backend:local ./backend
```

Run backend image:
```powershell
docker run -d --rm -p 8000:8000 --name vitality-backend-test vitality-backend:local
# verify
curl http://localhost:8000/health
# stop
docker stop vitality-backend-test
```

8) Integration test (executes code inside container)

The integration test runs a short Python snippet using the orchestrator and requires Docker. It will be skipped if Docker is not available.

Run:
```powershell
$env:PYTHONPATH = "$(pwd)"
.\.venv\Scripts\Activate.ps1
python -m unittest tests.integration.test_execute_integration -v
```

On systems without Docker, the test will report `skipped`.

9) Environment notes & remote orchestrator

- To run orchestrator against a remote Docker host (instead of mounting host socket), set:
```bash
export REMOTE_DOCKER_HOST=tcp://remote-host:2375
```
or on PowerShell:
```powershell
$env:REMOTE_DOCKER_HOST = "tcp://remote-host:2375"
```

The orchestrator will prefer `REMOTE_DOCKER_HOST` when present. Use a secured remote Docker API (TLS & auth) for production.

10) CI (GitHub Actions)

The repo includes `.github/workflows/ci.yml` which runs unit tests and builds Docker images. Integration tests that require Docker are not run by default in the unit job.

11) Troubleshooting storage directory

- The per-user JSON files live under `storage/users/<user_id>/`. This folder is created when a chat is saved or when `ensure_user_dir()` is called. If you don't see `storage/users/u1`, create a chat for `u1` via the API or run the quick script below.

Quickly create a sample chat for `u1`:
```powershell
python - <<'PY'
from backend.app.storage import save_chat
print(save_chat('u1', {'title':'sample chat'}))
PY
```

12) Security reminders

- Mounting `/var/run/docker.sock` into containers (as done in local `docker-compose.yml`) grants privileged control over the Docker host — acceptable for local dev but insecure for untrusted code.
- Prefer remote, audited worker clusters, Kubernetes Jobs, or VM-based sandboxes for production execution.

13) Quick checklist to verify everything is healthy

1. Start backend (uvicorn) and verify `/health` returns `{"status":"ok"}`.
2. Start execution service and verify its `/health` and `/metrics` endpoints.
3. Start frontend dev server and open `http://localhost:5173`.
4. (Optional) Start compose: `docker compose -f docker/docker-compose.yml up --build` and verify services on ports 8000/9000/5173/9090.

If you want, I can also add a PowerShell script `scripts/dev_up.ps1` that performs these steps automatically and waits for health checks. Tell me if you'd like that and I'll add it.