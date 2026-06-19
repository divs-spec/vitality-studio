import os
import docker
from typing import Tuple


def run_remote_container(language: str, code: str, timeout: int = 10, cpus: float = 0.5, memory: str = "128m") -> Tuple[str, str, int]:
    """
    Run code on a remote Docker host specified by REMOTE_DOCKER_HOST (e.g. tcp://host:2375).
    Uses the python `docker` SDK. This function runs a short-lived container with
    network disabled and returns stdout, stderr and exit code.
    Note: this method passes the code as a command argument (python -c / node -e),
    which is suitable for short snippets.
    """
    remote = os.environ.get("REMOTE_DOCKER_HOST")
    if not remote:
        # fallback to local docker environment
        client = docker.from_env()
    else:
        # use remote base_url
        client = docker.DockerClient(base_url=remote)

    mapping = {
        "python": ("python:3.12-slim", ["python", "-c", code]),
        "javascript": ("node:18-slim", ["node", "-e", code]),
    }
    if language not in mapping:
        raise ValueError("unsupported language")

    image, cmd = mapping[language]
    # pull image if not present
    try:
        client.images.pull(image)
    except Exception:
        pass

    try:
        container = client.containers.run(
            image,
            cmd,
            detach=True,
            network_disabled=True,
            mem_limit=memory,
            cpu_quota=int(cpus * 100000),
            remove=True,
        )
        result = container.wait(timeout=timeout)
        logs = container.logs(stdout=True, stderr=True)
        # docker-py returns logs as bytes
        stdout = logs.decode("utf-8", errors="replace")
        exit_code = result.get("StatusCode", 1)
        return stdout, "", exit_code
    except Exception as e:
        return "", str(e), 1
