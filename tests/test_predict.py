
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.backends.mock import (
    MockBackend,
    ModelInferenceError,
)

client = TestClient(app)


def test_mock_backend():
    backend = MockBackend()

    result = backend.predict("hello")

    assert result == "Mock prediction: hello"


def test_mock_backend_failure():
    backend = MockBackend(should_fail=True)

    with pytest.raises(ModelInferenceError):
        backend.predict("hello")


def test_predict_api():
    response = client.post(
        "/predict",
        json={"text": "Hello AI Infra"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["model"] == "mock"
    assert data["result"] == (
        "Mock prediction: Hello AI Infra"
    )


def test_predict_empty_input():
    response = client.post(
        "/predict",
        json={"text": ""},
    )

    assert response.status_code == 422


def test_predict_model_failure(monkeypatch):
    failing_backend = MockBackend(should_fail=True)

    monkeypatch.setattr(
        "app.main.backend",
        failing_backend,
    )

    response = client.post(
        "/predict",
        json={"text": "hello"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Model inference unavailable"
    )
