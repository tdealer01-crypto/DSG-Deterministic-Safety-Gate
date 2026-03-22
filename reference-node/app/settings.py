from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("DSG_APP_NAME", "DSG Reference Node")
    app_version: str = os.getenv("DSG_APP_VERSION", "0.3.0")
    database_url: str = os.getenv("DSG_DATABASE_URL", "sqlite:///./data/dsg.db")
    block_actions: tuple[str, ...] = tuple(
        action.strip()
        for action in os.getenv("DSG_BLOCK_ACTIONS", "danger,delete_all,exfiltrate").split(",")
        if action.strip()
    )
    stabilize_actions: tuple[str, ...] = tuple(
        action.strip()
        for action in os.getenv("DSG_STABILIZE_ACTIONS", "elevate,override,high_risk").split(",")
        if action.strip()
    )

    @property
    def sqlite_path(self) -> Path:
        prefix = "sqlite:///"
        if self.database_url.startswith(prefix):
            return Path(self.database_url[len(prefix) :])
        raise ValueError("Only sqlite:/// URLs are currently supported")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
