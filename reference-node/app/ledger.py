from __future__ import annotations

import json
from typing import Dict, List

from .database import get_connection
from .models import ExecutionDecision, ExecutionRequest


def record_execution(req: ExecutionRequest, decision: ExecutionDecision) -> Dict:
    payload_json = json.dumps(req.payload)
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO ledger (
                agent_id,
                action,
                payload_json,
                decision,
                stability_score,
                reason,
                evaluated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                req.agent_id,
                req.action,
                payload_json,
                decision.decision,
                decision.stability_score,
                decision.reason,
                decision.evaluated_at,
            ),
        )
        conn.commit()
        entry_id = cursor.lastrowid

    return {
        "id": entry_id,
        "agent_id": req.agent_id,
        "action": req.action,
        "payload": req.payload,
        "decision": decision.decision,
        "stability_score": decision.stability_score,
        "reason": decision.reason,
        "evaluated_at": decision.evaluated_at,
    }


def list_entries() -> List[Dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, agent_id, action, payload_json, decision, stability_score, reason, evaluated_at
            FROM ledger
            ORDER BY id DESC
            """
        ).fetchall()

    items: List[Dict] = []
    for row in rows:
        items.append(
            {
                "id": row["id"],
                "agent_id": row["agent_id"],
                "action": row["action"],
                "payload": json.loads(row["payload_json"]),
                "decision": row["decision"],
                "stability_score": row["stability_score"],
                "reason": row["reason"],
                "evaluated_at": row["evaluated_at"],
            }
        )
    return items


def metrics() -> Dict:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) AS count FROM ledger").fetchone()["count"]
        allow = conn.execute("SELECT COUNT(*) AS count FROM ledger WHERE decision = 'ALLOW'").fetchone()["count"]
        stabilize = conn.execute("SELECT COUNT(*) AS count FROM ledger WHERE decision = 'STABILIZE'").fetchone()["count"]
        block = conn.execute("SELECT COUNT(*) AS count FROM ledger WHERE decision = 'BLOCK'").fetchone()["count"]

    return {
        "total_executions": total,
        "allow_count": allow,
        "stabilize_count": stabilize,
        "block_count": block,
    }
