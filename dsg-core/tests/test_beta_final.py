import fakeredis
import pytest

from dsg.gate import DSGGate, DSGRequest


@pytest.fixture
def gate():
    return DSGGate(db_client=fakeredis.FakeStrictRedis())


def get_happy(val=10.0):
    return {
        "value": val,
        "is_grounded": True,
        "intent_score": 1,
        "is_api_clean": True,
        "source_verified": True,
        "compute_cost": 100,
        "has_audit_trail": True,
        "nonce_lock": True,
    }


def test_01_allow(gate):
    req = DSGRequest(agent="A1", state_next=get_happy(), signals=[0.9, 0.9, 0.9], nonce="n1")
    assert gate.process_request(req).decision == "ALLOW"


def test_02_stabilize(gate):
    req = DSGRequest(agent="A1", state_next=get_happy(15.0), signals=[0.7, 0.7, 0.7], nonce="n2")
    assert gate.process_request(req).decision == "STABILIZE"


def test_03_block(gate):
    req = DSGRequest(agent="A1", state_next={"value": -1}, signals=[1], nonce="n3")
    assert gate.process_request(req).decision == "BLOCK"


def test_04_replay(gate):
    req = DSGRequest(agent="A1", state_next=get_happy(), signals=[1], nonce="n4")
    gate.process_request(req)
    assert "replay_detected" in gate.process_request(req).reasons


def test_05_tamper(gate):
    req = DSGRequest(agent="A1", state_next=get_happy(), signals=[1], nonce="n5")
    gate.process_request(req)
    gate.ledger.chain[0]["data"]["d"] = "ALLOW_INJECTED"
    assert gate.ledger.verify_chain() is False


def test_06_version_mismatch(gate):
    req = DSGRequest(version="2.0.0", agent="A1", state_next=get_happy(), signals=[1], nonce="n6")
    res = gate.process_request(req)
    assert res.version == "2.0.0"
    assert gate.ledger.chain[-1]["data"]["incident"] == "unsupported_version"


def test_07_chaos(gate):
    req = DSGRequest(agent="A1", state_next=get_happy(), signals=[0.1, 0.9, 0.4], nonce="n7")
    assert gate.process_request(req).phase == "CHAOS"


def test_08_empty_signals(gate):
    req = DSGRequest(agent="A1", state_next=get_happy(), signals=[], nonce="n8")
    assert gate.process_request(req).decision == "BLOCK"


def test_09_resource_limit(gate):
    sn = get_happy()
    sn["compute_cost"] = 2000
    req = DSGRequest(agent="A1", state_next=sn, signals=[1], nonce="n9")
    assert "RIGHT_EFFORT" in gate.process_request(req).reasons


def test_10_malformed(gate):
    with pytest.raises(Exception):
        DSGRequest(agent="A1", state_next="fail", signals=[1], nonce="n10")


def test_11_max_drift(gate):
    req = DSGRequest(agent="A1", state_next=get_happy(200.0), signals=[1], nonce="n11")
    assert gate.process_request(req).decision == "BLOCK"


def test_12_multi_violation(gate):
    req = DSGRequest(agent="A1", state_next={"value": -5, "nonce_lock": False}, signals=[1], nonce="n12")
    assert len(gate.process_request(req).reasons) >= 2
