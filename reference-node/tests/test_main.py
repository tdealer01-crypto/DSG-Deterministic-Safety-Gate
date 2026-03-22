from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DSG Node Online"


def test_execute_allow() -> None:
    response = client.post(
        "/execute",
        json={"agent_id": "agt_test", "action": "scan", "payload": {}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "ALLOW"


def test_execute_block() -> None:
    response = client.post(
        "/execute",
        json={"agent_id": "agt_test", "action": "danger", "payload": {}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "BLOCK"
