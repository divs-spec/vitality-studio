FROM docker:24.0.5-cli
WORKDIR /app
COPY . /app
# Use the official Docker CLI image as base (contains docker client).
# Install Python and pip so the runner and orchestrator can run.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends python3 python3-venv python3-pip ca-certificates \
	&& python3 -m pip install --no-cache-dir fastapi uvicorn pydantic docker \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*
EXPOSE 9000
CMD ["uvicorn", "execution_engine.runner:app", "--host", "0.0.0.0", "--port", "9000"]
