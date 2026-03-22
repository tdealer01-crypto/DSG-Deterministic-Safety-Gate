from __future__ import annotations

from datetime import datetime, timezone

from .models import ExecutionDecision, ExecutionRequest

DANGEROUS_ACTIONS = {"danger", "delete_all", "exfiltrate"}
STABILIZE_ACTIONS = {"elevate", "override", "high_risk"}


def evaluate_execution(req: ExecutionRequest) -> ExecutionDecision:
    if req.action in DANGEROUS_ACTIONS:
        decision = "BLOCK"
        stability_score = 0.10
        reason = "Action violates default safety policy"
    elif req.action in STABILIZE_ACTIONS:
        decision = "STABILIZE"
        stability_score = 0.55
        reason = "Action requires stabilization before execution"
    else:
        decision = "ALLOW"
        stability_score = 0.95
        reason = "Execution satisfies default policy"

    return ExecutionDecision(
        decision=decision,
        stability_score=stability_score,
        reason=reason,
        agent_id=req.agent_id,
        action=req.action,
        evaluated_at=datetime.now(timezone.utc).isoformat(),
    )
