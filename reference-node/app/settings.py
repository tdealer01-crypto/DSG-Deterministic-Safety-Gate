from __future__ import annotations

import json
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("DSG_APP_NAME", "DSG Reference Node")
    app_version: str = os.getenv("DSG_APP_VERSION", "0.5.0")
    database_url: str = os.getenv("DSG_DATABASE_URL", "sqlite:///./data/dsg.db")
    api_key: str | None = os.getenv("DSG_API_KEY")
    policy_file: str = os.getenv("DSG_POLICY_FILE", "./policies/default-policy.json")
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

    def load_policy_file(self) -> dict[str, Any]:
        path = Path(self.policy_file)
        if not path.exists():
            return {
                "block_actions": list(self.block_actions),
                "stabilize_actions": list(self.stabilize_actions),
            }
        text = path.read_text(encoding="utf-8")
        if path.suffix in {".yaml", ".yml"}:
            data: dict[str, Any] = {}
            current_list_key: str | None = None
            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.endswith(":"):
                    current_list_key = line[:-1].strip()
                    data[current_list_key] = []
                    continue
                if line.startswith("-") and current_list_key:
                    data[current_list_key].append(line[1:].strip())
            return data
        return json.loads(text)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
