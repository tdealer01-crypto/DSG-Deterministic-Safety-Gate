from __future__ import annotations

from typing import Any, Dict, Literal

from pydantic import BaseModel, Field

DecisionType = Literal["ALLOW", "STABILIZE", "BLOCK"]


class ExecutionRequest(BaseModel):
    agent_id: str
    action: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str | None = None


class ExecutionDecision(BaseModel):
    decision: DecisionType
    stability_score: float
    reason: str
    agent_id: str
    action: str
    evaluated_at: str
