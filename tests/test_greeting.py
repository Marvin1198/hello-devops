import pytest
from fastapi.testclient import TestClient

from app.greeting import build_greeting, is_healthy
from app.main import app

client = TestClient(app)


# --- unit tests: pure logic, no web layer ---

def test_default_greeting():
    assert build_greeting() == "Hello, World!"


def test_named_greeting():
    assert build_greeting("Marvin") == "Hello, Marvin!"


def test_whitespace_name_falls_back():
    assert build_greeting("   ") == "Hello, World!"


def test_name_is_trimmed():
    assert build_greeting("  Marvin  ") == "Hello, Marvin!"


def test_overlong_name_rejected():
    with pytest.raises(ValueError):
        build_greeting("x" * 51)


def test_health_reports_dependency_state():
    assert is_healthy(True) is True
    assert is_healthy(False) is False


# --- integration tests: through the API ---

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, World!"


def test_root_endpoint_with_name():
    response = client.get("/?name=RBC")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, RBC!"


def test_root_endpoint_rejects_overlong_name():
    response = client.get("/?name=" + "x" * 51)
    assert response.status_code == 400


def test_healthz():
    assert client.get("/healthz").status_code == 200


def test_readyz():
    assert client.get("/readyz").status_code == 200
