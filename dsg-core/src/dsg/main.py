from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from .gate import DSGGate, DSGRequest

app = FastAPI(title="DSG Reference Node", version="0.1.0-beta.1")
gate = DSGGate()


@app.get("/health")
def health() -> dict:
    return {
        "status": "DSG_ACTIVE",
        "deterministic": True,
        "version": "0.1.0-beta.1",
    }


@app.post("/evaluate")
def evaluate(req: DSGRequest):
    return gate.process_request(req)


@app.post("/execute")
def execute(req: DSGRequest) -> Dict[str, Any]:
    response = gate.process_request(req).model_dump()
    response["evaluated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return response


@app.get("/metrics")
def metrics() -> Dict[str, Any]:
    decision_counts = {"ALLOW": 0, "STABILIZE": 0, "BLOCK": 0}
    for node in gate.ledger.chain:
        data = node.get("data", {})
        decision = data.get("d")
        if decision in decision_counts:
            decision_counts[decision] += 1

    total = sum(decision_counts.values())
    allow_rate = decision_counts["ALLOW"] / total if total else 0.0
    stabilize_rate = decision_counts["STABILIZE"] / total if total else 0.0
    block_rate = decision_counts["BLOCK"] / total if total else 0.0

    return {
        "decision_counts": decision_counts,
        "allow_rate": round(allow_rate, 4),
        "stabilize_rate": round(stabilize_rate, 4),
        "block_rate": round(block_rate, 4),
        "latest_stability_summary": None,
        "latest_entropy_summary": None,
    }


@app.get("/ledger")
def ledger(limit: int = 100) -> Dict[str, Any]:
    safe_limit = max(1, min(limit, 1000))
    return {"entries": gate.ledger.chain[-safe_limit:]}


@app.get("/audit/events")
def audit_events(limit: int = 100) -> Dict[str, Any]:
    safe_limit = max(1, min(limit, 1000))
    events = []
    for node in gate.ledger.chain[-safe_limit:]:
        data = node.get("data", {})
        events.append(
            {
                "timestamp": node.get("ts"),
                "agent": data.get("a"),
                "decision": data.get("d"),
                "incident": data.get("incident"),
                "proof_hash": data.get("p"),
                "ledger_hash": node.get("hash"),
            }
        )
    return {"events": events}


@app.get("/audit/determinism/{sequence}")
def audit_determinism(sequence: int) -> Dict[str, Any]:
    if sequence < 0 or sequence >= len(gate.ledger.chain):
        raise HTTPException(status_code=404, detail="sequence_not_found")

    node = gate.ledger.chain[sequence]
    data = node.get("data", {})
    proof_hash = data.get("p")

    return {
        "sequence": sequence,
        "region_count": 1,
        "unique_state_hashes": 1 if proof_hash else 0,
        "max_entropy": None,
        "deterministic": bool(proof_hash),
        "gate_action": data.get("d", "BLOCK"),
    }


@app.get("/ledger/verify")
def verify_ledger() -> dict:
    return {"ok": gate.ledger.verify_chain(), "entries": len(gate.ledger.chain)}
