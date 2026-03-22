from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Dict, List

from .database import get_connection
from .models import AuditDeterminismResult, AuditEventRequest


def record_audit_event(event: AuditEventRequest) -> Dict:
    created_at = datetime.now(timezone.utc).isoformat()
    metadata_json = json.dumps(event.metadata)

    with get_connection() as conn:
        if hasattr(conn, "execute"):
            cursor = conn.execute(
                """
                INSERT INTO audit_events (
                    epoch, sequence, region_id, state_hash, entropy, gate_result,
                    z3_proof_hash, signature, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.epoch,
                    event.sequence,
                    event.region_id,
                    event.state_hash,
                    event.entropy,
                    event.gate_result,
                    event.z3_proof_hash,
                    event.signature,
                    metadata_json,
                    created_at,
                ),
            )
            conn.commit()
            entry_id = cursor.lastrowid
        else:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO audit_events (
                        epoch, sequence, region_id, state_hash, entropy, gate_result,
                        z3_proof_hash, signature, metadata_json, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        event.epoch,
                        event.sequence,
                        event.region_id,
                        event.state_hash,
                        event.entropy,
                        event.gate_result,
                        event.z3_proof_hash,
                        event.signature,
                        metadata_json,
                        created_at,
                    ),
                )
                entry_id = cur.fetchone()[0]
            conn.commit()

    return {
        "id": entry_id,
        "epoch": event.epoch,
        "sequence": event.sequence,
        "region_id": event.region_id,
        "state_hash": event.state_hash,
        "entropy": event.entropy,
        "gate_result": event.gate_result,
        "z3_proof_hash": event.z3_proof_hash,
        "signature": event.signature,
        "metadata": event.metadata,
        "created_at": created_at,
    }


def list_audit_events(limit: int = 50) -> List[Dict]:
    with get_connection() as conn:
        if hasattr(conn, "execute"):
            rows = conn.execute(
                """
                SELECT id, epoch, sequence, region_id, state_hash, entropy, gate_result,
                       z3_proof_hash, signature, metadata_json, created_at
                FROM audit_events
                ORDER BY sequence DESC, id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, epoch, sequence, region_id, state_hash, entropy, gate_result,
                           z3_proof_hash, signature, metadata_json, created_at
                    FROM audit_events
                    ORDER BY sequence DESC, id DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                rows = cur.fetchall()

    items: List[Dict] = []
    for row in rows:
        items.append(
            {
                "id": row["id"],
                "epoch": row["epoch"],
                "sequence": row["sequence"],
                "region_id": row["region_id"],
                "state_hash": row["state_hash"],
                "entropy": row["entropy"],
                "gate_result": row["gate_result"],
                "z3_proof_hash": row["z3_proof_hash"],
                "signature": row["signature"],
                "metadata": json.loads(row["metadata_json"]),
                "created_at": row["created_at"],
            }
        )
    return items


def get_determinism(sequence: int) -> AuditDeterminismResult:
    with get_connection() as conn:
        if hasattr(conn, "execute"):
            rows = conn.execute(
                """
                SELECT region_id, state_hash, entropy
                FROM audit_events
                WHERE sequence = ?
                """,
                (sequence,),
            ).fetchall()
        else:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT region_id, state_hash, entropy
                    FROM audit_events
                    WHERE sequence = %s
                    """,
                    (sequence,),
                )
                rows = cur.fetchall()

    hashes = {row["state_hash"] for row in rows}
    max_entropy = max((float(row["entropy"]) for row in rows), default=0.0)
    deterministic = len(hashes) <= 1 and max_entropy < 1.0
    gate_action = "ALLOW" if deterministic else "FREEZE"

    return AuditDeterminismResult(
        sequence=sequence,
        region_count=len(rows),
        unique_state_hashes=len(hashes),
        max_entropy=max_entropy,
        deterministic=deterministic,
        gate_action=gate_action,
    )
