from __future__ import annotations

from fastapi import Header, HTTPException, status

from .settings import get_settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    valid_keys = settings.api_keys
    if not valid_keys:
        return
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
