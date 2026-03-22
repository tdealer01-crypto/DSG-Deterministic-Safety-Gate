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


class AuditEventRequest(BaseModel):
    epoch: str
    sequence: int
    region_id: str
    state_hash: str
    entropy: float = 0.0
    gate_result: DecisionType
    z3_proof_hash: str | None = None
    signature: str | None = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AuditDeterminismResult(BaseModel):
    sequence: int
    region_count: int
    unique_state_hashes: int
    max_entropy: float
    deterministic: bool
    gate_action: str
