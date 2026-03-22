from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .settings import get_settings

try:
    import psycopg
except Exception:  # pragma: no cover
    psycopg = None


def get_connection() -> Any:
    settings = get_settings()
    if settings.is_sqlite:
        db_path = settings.sqlite_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    if settings.is_postgres:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL support")
        conn = psycopg.connect(settings.database_url)
        conn.row_factory = psycopg.rows.dict_row
        return conn
    raise ValueError("Unsupported database URL")


def init_db() -> None:
    settings = get_settings()
    if settings.is_sqlite:
        with get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    stability_score REAL NOT NULL,
                    reason TEXT NOT NULL,
                    evaluated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    epoch TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    region_id TEXT NOT NULL,
                    state_hash TEXT NOT NULL,
                    entropy REAL NOT NULL,
                    gate_result TEXT NOT NULL,
                    z3_proof_hash TEXT,
                    signature TEXT,
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()
    elif settings.is_postgres:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ledger (
                        id SERIAL PRIMARY KEY,
                        agent_id TEXT NOT NULL,
                        action TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        decision TEXT NOT NULL,
                        stability_score DOUBLE PRECISION NOT NULL,
                        reason TEXT NOT NULL,
                        evaluated_at TEXT NOT NULL
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS audit_events (
                        id SERIAL PRIMARY KEY,
                        epoch TEXT NOT NULL,
                        sequence BIGINT NOT NULL,
                        region_id TEXT NOT NULL,
                        state_hash TEXT NOT NULL,
                        entropy DOUBLE PRECISION NOT NULL,
                        gate_result TEXT NOT NULL,
                        z3_proof_hash TEXT,
                        signature TEXT,
                        metadata_json TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
            conn.commit()
