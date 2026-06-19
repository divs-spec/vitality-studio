import os
import subprocess
import tempfile
import uuid
import shlex
from typing import Tuple
from .remote_orchestrator import run_remote_container


def run_in_container(language: str, code: str, timeout: int = 10, cpus: float = 0.5, memory: str = "128m") -> Tuple[str, str, int]:
    """
    Run the provided code in a fresh ephemeral container.

    If `REMOTE_DOCKER_HOST` environment variable is set the code will be
    executed via the remote orchestrator (python docker SDK). Otherwise
    this falls back to invoking the local `docker` CLI using `docker run`.
    """
    # If a remote docker host is configured, use remote orchestrator
    remote_host = os.environ.get("REMOTE_DOCKER_HOST")
    if remote_host:
        return run_remote_container(language, code, timeout=timeout, cpus=cpus, memory=memory)

    # Fallback: use local docker CLI invocation
    mapping = {
        "python": ("python:3.12-slim", "python /tmp/code.py"),
        "javascript": ("node:18-slim", "node /tmp/code.js"),
    }
    if language not in mapping:
        raise ValueError("unsupported language")

    image, cmd = mapping[language]

    # create temp dir to hold code
    tmpdir = tempfile.mkdtemp(prefix="vitality-run-")
    fname = "code.py" if language == "python" else "code.js"
    path = os.path.join(tmpdir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    container_name = f"vitality-run-{uuid.uuid4().hex[:8]}"

    docker_cmd = (
        f"docker run --rm --name {container_name} "
        f"--cpus=" + str(cpus) + " "
        f"--memory=" + memory + " "
        f"--network=none "
        f"-v {shlex.quote(path)}:/tmp/{fname}:ro "
        f"{image} sh -c {shlex.quote(cmd)}"
    )

    try:
        proc = subprocess.run(docker_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        stdout = proc.stdout.decode('utf-8', errors='replace')
        stderr = proc.stderr.decode('utf-8', errors='replace')
        return stdout, stderr, proc.returncode
    finally:
        # best-effort cleanup
        try:
            if os.path.exists(path):
                os.remove(path)
            os.rmdir(tmpdir)
        except Exception:
            pass
