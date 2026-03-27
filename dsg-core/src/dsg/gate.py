from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

from pydantic import BaseModel

from .harmonics import HarmonicEngine
from .ledger import AppendOnlyLedger
from .stability import StabilityAnalyzer


class DSGRequest(BaseModel):
    version: str = "1.0.0"
    agent: str
    state_next: Dict[str, Any]
    signals: List[float]
    nonce: str


class DSGResponse(BaseModel):
    decision: str
    phase: str
    stability: float
    entropy: float
    proof_hash: str
    reasons: List[str]
    ledger_hash: str
    version: str


class DSGGate:
    SUPPORTED_VERSIONS = ["1.0.0"]

    def __init__(self, db_client=None) -> None:
        self.harmonics = HarmonicEngine()
        self.stability = StabilityAnalyzer()
        self.ledger = AppendOnlyLedger()
        self.db = db_client
        self.anchor = {"value": 10.0}

    def process_request(self, req: DSGRequest) -> DSGResponse:
        if req.version not in self.SUPPORTED_VERSIONS:
            ledger_hash = self.ledger.append(
                {"a": req.agent, "v": req.version, "incident": "unsupported_version"}
            )
            return self._build_resp(
                "BLOCK", "CHAOS", 0.0, 1.0, ["unsupported_version"], lh=ledger_hash, ver=req.version
            )

        nonce_key = f"nonce:{req.agent}:{req.nonce}"
        if self.db:
            if self.db.get(nonce_key):
                ledger_hash = self.ledger.append(
                    {"a": req.agent, "n": req.nonce, "incident": "replay_detected"}
                )
                return self._build_resp(
                    "BLOCK", "CHAOS", 0.0, 1.0, ["replay_detected"], lh=ledger_hash, ver=req.version
                )
            self.db.setex(nonce_key, 3600, "1")

        reasons = self.verify_makk8(req.state_next)
        phase, entropy, _ = self.harmonics.evaluate_phase(req.signals)
        stability = self.stability.compute_stability(self.anchor, req.state_next)

        decision = "ALLOW"
        if reasons or phase == "CHAOS" or stability < 0.3:
            decision = "BLOCK"
        elif phase == "TUNING" or stability < 0.7:
            decision = "STABILIZE"

        proof_hash = self._generate_proof(req, decision, entropy)
        ledger_hash = self.ledger.append({"a": req.agent, "d": decision, "p": proof_hash})
        return self._build_resp(
            decision, phase, stability, entropy, reasons, proof_hash, ledger_hash, ver=req.version
        )

    def verify_makk8(self, state_next: Dict[str, Any]) -> List[str]:
        rules = {
            "RIGHT_VIEW": state_next.get("is_grounded") is True,
            "RIGHT_INTENT": state_next.get("intent_score", 0) > 0,
            "RIGHT_SPEECH": state_next.get("is_api_clean") is True,
            "RIGHT_CONDUCT": state_next.get("value", 0) >= 0,
            "RIGHT_LIVELIHOOD": state_next.get("source_verified") is True,
            "RIGHT_EFFORT": state_next.get("compute_cost", 0) < 1000,
            "RIGHT_MINDFULNESS": state_next.get("has_audit_trail") is True,
            "RIGHT_SAMADHI": state_next.get("nonce_lock") is True,
        }
        return [name for name, passed in rules.items() if not passed]

    def _generate_proof(self, req: DSGRequest, decision: str, entropy: float) -> str:
        bundle = {
            "v": req.version,
            "a": req.agent,
            "n": req.nonce,
            "g": req.signals,
            "d": decision,
            "e": round(entropy, 4),
            "s": req.state_next,
        }
        return hashlib.sha256(json.dumps(bundle, sort_keys=True).encode()).hexdigest()

    def _build_resp(
        self,
        decision: str,
        phase: str,
        stability: float,
        entropy: float,
        reasons: List[str],
        proof_hash: str = "ERROR",
        ledger_hash: str = "0",
        ver: str = "1.0.0",
    ) -> DSGResponse:
        return DSGResponse(
            decision=decision,
            phase=phase,
            stability=round(stability, 4),
            entropy=round(entropy, 4),
            proof_hash=proof_hash,
            reasons=reasons,
            ledger_hash=ledger_hash,
            version=ver,
        )
