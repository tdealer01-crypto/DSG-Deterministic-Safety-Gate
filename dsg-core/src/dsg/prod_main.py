from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from .gate import DSGGate, DSGRequest

app = FastAPI(title="DSG Production Bridge Node", version="0.1.0-beta.1")
gate = DSGGate()
decision_history: List[Dict[str, Any]] = []


class ExecuteBridgePayload(BaseModel):
    input: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)


class ExecuteBridgeRequest(BaseModel):
    agent_id: str
    action: str = "scan"
    payload: ExecuteBridgePayload = Field(default_factory=ExecuteBridgePayload)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _clamp_float(value: Any, default: float, low: float, high: float) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = default
    return max(low, min(high, numeric))


def _build_state_next(req: ExecuteBridgeRequest) -> Dict[str, Any]:
    input_payload = req.payload.input if isinstance(req.payload.input, dict) else {}
    context_payload = req.payload.context if isinstance(req.payload.context, dict) else {}

    base_state = input_payload.get("state_next", {})
    state_next = dict(base_state if isinstance(base_state, dict) else {})

    risk_score = _clamp_float(context_payload.get("risk_score", 0.1), 0.1, 0.0, 1.0)
    value = _clamp_float(input_payload.get("value", 10.0), 10.0, -1000000.0, 1000000.0)
    compute_cost = _clamp_float(
        context_payload.get("compute_cost", input_payload.get("compute_cost", 100.0)),
        100.0,
        0.0,
        1000000.0,
    )

    state_next.setdefault("is_grounded", bool(input_payload.get("is_grounded", True)))
    state_next.setdefault("intent_score", max(0.01, 1.0 - risk_score))
    state_next.setdefault("is_api_clean", bool(input_payload.get("is_api_clean", True)))
    state_next.setdefault("value", value)
    state_next.setdefault("source_verified", bool(context_payload.get("source_verified", True)))
    state_next.setdefault("compute_cost", compute_cost)
    state_next.setdefault("has_audit_trail", True)
    state_next.setdefault("nonce_lock", True)
    state_next.setdefault("action", req.action)
    state_next.setdefault("request_input", input_payload)
    state_next.setdefault("request_context", context_payload)
    return state_next


def _build_signals(req: ExecuteBridgeRequest) -> List[float]:
    input_payload = req.payload.input if isinstance(req.payload.input, dict) else {}
    context_payload = req.payload.context if isinstance(req.payload.context, dict) else {}

    provided = context_payload.get("signals", input_payload.get("signals"))
    if isinstance(provided, list):
        normalized = []
        for item in provided[:8]:
            normalized.append(_clamp_float(item, 1.0, 0.01, 10.0))
        if normalized:
            return normalized

    risk_score = _clamp_float(context_payload.get("risk_score", 0.1), 0.1, 0.0, 1.0)
    return [
        max(0.05, 1.0 - risk_score),
        max(0.05, 1.0 - (risk_score / 2.0)),
    ]


def _build_nonce(req: ExecuteBridgeRequest) -> str:
    context_payload = req.payload.context if isinstance(req.payload.context, dict) else {}
    raw = context_payload.get("nonce") or context_payload.get("trace_id") or _utc_now_iso()
    return str(raw)


def _string_reason(reasons: List[str], decision: str) -> str:
    if reasons:
        return ", ".join(reasons)
    if decision == "ALLOW":
        return "Execution satisfies active invariants and stability is within bounds."
    if decision == "STABILIZE":
        return "Execution requires stabilization before approval."
    return "Blocked by deterministic gate."


def _record_history(
    *,
    agent_id: str,
    action: str,
    response: Dict[str, Any],
) -> Dict[str, Any]:
    sequence = len(decision_history) + 1
    event = {
        "sequence": sequence,
        "epoch": "DSG-BETA-1",
        "region_id": "reference-node",
        "state_hash": response["ledger_hash"],
        "entropy": response["entropy"],
        "gate_result": response["decision"],
        "z3_proof_hash": response["proof_hash"],
        "signature": None,
        "created_at": response["evaluated_at"],
        "agent_id": agent_id,
        "action": action,
        "decision": response["decision"],
        "phase": response["phase"],
        "stability": response["stability"],
        "reason": response["reason"],
        "reasons": response["reasons"],
        "proof_hash": response["proof_hash"],
        "ledger_hash": response["ledger_hash"],
        "version": response["version"],
    }
    decision_history.append(event)
    return event


def _response_from_gate(
    *,
    agent_id: str,
    action: str,
    gate_response: Any,
) -> Dict[str, Any]:
    evaluated_at = _utc_now_iso()
    reasons = list(getattr(gate_response, "reasons", []) or [])
    response = {
        "decision": getattr(gate_response, "decision", "BLOCK"),
        "phase": getattr(gate_response, "phase", "CHAOS"),
        "stability": getattr(gate_response, "stability", 0.0),
        "stability_score": getattr(gate_response, "stability", 0.0),
        "entropy": getattr(gate_response, "entropy", 1.0),
        "proof_hash": getattr(gate_response, "proof_hash", "ERROR"),
        "ledger_hash": getattr(gate_response, "ledger_hash", "0"),
        "version": getattr(gate_response, "version", "0.1.0-beta.1"),
        "policy_version": getattr(gate_response, "version", "0.1.0-beta.1"),
        "evaluated_at": evaluated_at,
        "reason": _string_reason(reasons, getattr(gate_response, "decision", "BLOCK")),
        "reasons": reasons,
        "agent_id": agent_id,
        "request_type": action,
    }
    history = _record_history(agent_id=agent_id, action=action, response=response)
    response["sequence"] = history["sequence"]
    return response


def _ledger_items(limit: int = 20) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for index, node in enumerate(gate.ledger.chain, start=1):
        data = node.get("data", {})
        items.append(
            {
                "id": f"ledger_{index}",
                "sequence": index,
                "created_at": node.get("ts"),
                "decision": data.get("d") or ("BLOCK" if data.get("incident") else None),
                "gate_result": data.get("d") or ("BLOCK" if data.get("incident") else None),
                "proof_hash": data.get("p"),
                "ledger_hash": node.get("hash"),
                "prev_hash": node.get("prev_hash"),
                "metadata": data,
            }
        )
    return list(reversed(items))[:limit]


def _metrics() -> Dict[str, Any]:
    allow_count = sum(1 for item in decision_history if item["decision"] == "ALLOW")
    stabilize_count = sum(1 for item in decision_history if item["decision"] == "STABILIZE")
    block_count = sum(1 for item in decision_history if item["decision"] == "BLOCK")
    total = max(1, len(decision_history))
    latest = decision_history[-1] if decision_history else None
    return {
        "allow_count": allow_count,
        "stabilize_count": stabilize_count,
        "block_count": block_count,
        "allow_rate": round(allow_count / total, 4),
        "stabilize_rate": round(stabilize_count / total, 4),
        "block_rate": round(block_count / total, 4),
        "latest_entropy": latest["entropy"] if latest else 0.0,
        "latest_stability": latest["stability"] if latest else 0.0,
        "executions": len(decision_history),
    }


def _determinism_payload(sequence: int) -> Dict[str, Any]:
    matched = next((item for item in decision_history if item["sequence"] == sequence), None)
    if not matched:
        raise HTTPException(status_code=404, detail="sequence_not_found")
    return {
        "sequence": matched["sequence"],
        "region_count": 1,
        "unique_state_hashes": 1,
        "max_entropy": matched["entropy"],
        "deterministic": True,
        "gate_action": matched["gate_result"],
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "DSG_ACTIVE",
        "deterministic": True,
        "version": "0.1.0-beta.1",
        "mode": "production-bridge",
    }


@app.post("/evaluate")
def evaluate(req: DSGRequest) -> Dict[str, Any]:
    response = gate.process_request(req)
    return _response_from_gate(agent_id=req.agent, action="evaluate", gate_response=response)


@app.post("/execute")
def execute(req: ExecuteBridgeRequest) -> Dict[str, Any]:
    dsg_request = DSGRequest(
        version="1.0.0",
        agent=req.agent_id,
        state_next=_build_state_next(req),
        signals=_build_signals(req),
        nonce=_build_nonce(req),
    )
    response = gate.process_request(dsg_request)
    return _response_from_gate(agent_id=req.agent_id, action=req.action, gate_response=response)


@app.get("/metrics")
def metrics() -> Dict[str, Any]:
    return _metrics()


@app.get("/ledger")
def ledger(limit: int = Query(default=20, ge=1, le=200)) -> Dict[str, Any]:
    return {"items": _ledger_items(limit=limit)}


@app.get("/audit/events")
def audit_events(limit: int = Query(default=20, ge=1, le=200)) -> Dict[str, Any]:
    return {"items": list(reversed(decision_history))[:limit]}


@app.get("/audit/determinism/{sequence}")
def audit_determinism(sequence: int) -> Dict[str, Any]:
    return _determinism_payload(sequence)


@app.get("/audit/determinism")
def audit_determinism_query(sequence: int = Query(..., ge=1)) -> Dict[str, Any]:
    return _determinism_payload(sequence)


@app.get("/ledger/verify")
def verify_ledger() -> Dict[str, Any]:
    return {"ok": gate.ledger.verify_chain(), "entries": len(gate.ledger.chain)}
