from __future__ import annotations

from datetime import datetime, timezone

from .models import ExecutionDecision, ExecutionRequest
from .settings import get_settings


def evaluate_execution(req: ExecutionRequest) -> ExecutionDecision:
    settings = get_settings()
    policy = settings.load_policy_file()
    block_actions = set(policy.get("block_actions", list(settings.block_actions)))
    stabilize_actions = set(policy.get("stabilize_actions", list(settings.stabilize_actions)))

    if req.action in block_actions:
        decision = "BLOCK"
        stability_score = 0.10
        reason = "Action violates configured safety policy"
    elif req.action in stabilize_actions:
        decision = "STABILIZE"
        stability_score = 0.55
        reason = "Action requires stabilization before execution"
    else:
        decision = "ALLOW"
        stability_score = 0.95
        reason = "Execution satisfies configured policy"

    return ExecutionDecision(
        decision=decision,
        stability_score=stability_score,
        reason=reason,
        agent_id=req.agent_id,
        action=req.action,
        evaluated_at=datetime.now(timezone.utc).isoformat(),
    )
