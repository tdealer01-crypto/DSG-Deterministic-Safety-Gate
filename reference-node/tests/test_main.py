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


def test_policy_validation() -> None:
    from app.policy_validation import validate_policy

    errors = validate_policy({"block_actions": ["danger"], "stabilize_actions": ["elevate"]})
    assert errors == []
