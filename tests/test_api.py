
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_echo():
    response = client.post(
        "/echo",
        json={"text": "Hello AI Infra"},
    )

    assert response.status_code == 200
    assert response.json()["length"] == 14


def test_empty_input():
    response = client.post(
        "/echo",
        json={"text": ""},
    )

    assert response.status_code == 422

