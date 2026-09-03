import os

from fastapi import FastAPI, HTTPException

from app.greeting import build_greeting, is_healthy

APP_ENV = os.getenv("APP_ENV", "local")
APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="hello-devops", version=APP_VERSION)


@app.get("/")
def root(name: str | None = None):
    try:
        message = build_greeting(name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"message": message, "env": APP_ENV, "version": APP_VERSION}


@app.get("/healthz")
def healthz():
    """Liveness: is the process able to serve at all?"""
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    """Readiness: should this pod receive traffic right now?"""
    if not is_healthy():
        raise HTTPException(status_code=503, detail="not ready")
    return {"status": "ready"}
