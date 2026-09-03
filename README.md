# hello-devops

Python (FastAPI) reference app for practising a full CI/CD path:
build -> unit test -> coverage -> static analysis -> image scan -> registry -> Kubernetes.

## Local

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements-dev.txt
    pytest
    uvicorn app.main:app --reload

## Endpoints

| Path | Purpose |
|---|---|
| `/` | Greeting. Optional `?name=` |
| `/healthz` | Liveness - is the process serving |
| `/readyz` | Readiness - should this pod take traffic |

## Container

    docker build -t hello-devops:local .
    docker run --rm -p 8000:8000 hello-devops:local

Multistage build: dependencies compile in a builder stage, only the venv and
application code reach the runtime image. Runs as non-root uid 1001.
