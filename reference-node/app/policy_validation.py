from __future__ import annotations

from typing import Any

REQUIRED_KEYS = {"block_actions", "stabilize_actions"}


def validate_policy(policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_KEYS - set(policy.keys())
    if missing:
        errors.append(f"Missing required keys: {', '.join(sorted(missing))}")

    for key in ("block_actions", "stabilize_actions"):
        if key in policy and not isinstance(policy[key], list):
            errors.append(f"{key} must be a list")
        elif key in policy:
            for idx, item in enumerate(policy[key]):
                if not isinstance(item, str) or not item.strip():
                    errors.append(f"{key}[{idx}] must be a non-empty string")
    return errors
