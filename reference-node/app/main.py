from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="DSG Reference Node", version="0.1.0")


class ExecutionRequest(BaseModel):
    agent_id: str
    action: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str | None = None


@app.get("/")
def root() -> dict:
    return {
        "status": "DSG Node Online",
        "service": "reference-node",
        "version": "0.1.0",
    }


@app.post("/execute")
def execute(req: ExecutionRequest) -> dict:
    dangerous_actions = {"danger", "delete_all", "exfiltrate"}

    if req.action in dangerous_actions:
        decision = "BLOCK"
        stability_score = 0.10
        reason = "Action violates default safety policy"
    elif req.action in {"elevate", "override", "high_risk"}:
        decision = "STABILIZE"
        stability_score = 0.55
        reason = "Action requires stabilization before execution"
    else:
        decision = "ALLOW"
        stability_score = 0.95
        reason = "Execution satisfies default policy"

    return {
        "decision": decision,
        "stability_score": stability_score,
        "reason": reason,
        "agent_id": req.agent_id,
        "action": req.action,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }
