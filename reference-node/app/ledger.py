from __future__ import annotations

from typing import Dict, List

from .models import ExecutionDecision, ExecutionRequest

_LEDGER: List[Dict] = []


def record_execution(req: ExecutionRequest, decision: ExecutionDecision) -> Dict:
    entry = {
        "agent_id": req.agent_id,
        "action": req.action,
        "payload": req.payload,
        "decision": decision.decision,
        "stability_score": decision.stability_score,
        "reason": decision.reason,
        "evaluated_at": decision.evaluated_at,
    }
    _LEDGER.append(entry)
    return entry


def list_entries() -> List[Dict]:
    return list(_LEDGER)
