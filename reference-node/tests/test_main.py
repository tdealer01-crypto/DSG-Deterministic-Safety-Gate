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


def test_audit_ingest_and_determinism() -> None:
    response1 = client.post(
        "/audit/event",
        json={
            "epoch": "GEN5-EPOCH-001",
            "sequence": 42,
            "region_id": "asia-southeast1",
            "state_hash": "hash-a",
            "entropy": 0.2,
            "gate_result": "ALLOW",
            "metadata": {},
        },
    )
    assert response1.status_code == 200

    response2 = client.post(
        "/audit/event",
        json={
            "epoch": "GEN5-EPOCH-001",
            "sequence": 42,
            "region_id": "us-central1",
            "state_hash": "hash-a",
            "entropy": 0.4,
            "gate_result": "ALLOW",
            "metadata": {},
        },
    )
    assert response2.status_code == 200

    determinism = client.get("/audit/determinism/42")
    assert determinism.status_code == 200
    data = determinism.json()
    assert data["deterministic"] is True
    assert data["gate_action"] == "ALLOW"
