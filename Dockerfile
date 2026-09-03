# syntax=docker/dockerfile:1

# ---------- stage 1: build ----------
# pip, compilers and build wheels live here and never reach the final image.
FROM python:3.12-slim AS builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
# Copied before the source so this layer caches until dependencies change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- stage 2: runtime ----------
FROM python:3.12-slim AS runtime

# Never run as root. Kubernetes can enforce this, but the image should not rely on it.
RUN useradd --create-home --uid 1001 appuser

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY app/ ./app/

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
