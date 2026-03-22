from __future__ import annotations

import sqlite3

from .settings import get_settings


def get_connection() -> sqlite3.Connection:
    settings = get_settings()
    db_path = settings.sqlite_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
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
        conn.commit()
