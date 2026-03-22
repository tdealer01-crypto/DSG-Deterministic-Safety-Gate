from __future__ import annotations

from typing import Any, Dict

import requests


class DSGClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        return headers

    def health(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        return response.json()

    def metrics(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/metrics", headers=self._headers(), timeout=10)
        response.raise_for_status()
        return response.json()

    def ledger(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/ledger", headers=self._headers(), timeout=10)
        response.raise_for_status()
        return response.json()

    def execute(self, agent_id: str, action: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/execute",
            headers=self._headers(),
            json={
                "agent_id": agent_id,
                "action": action,
                "payload": payload or {},
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
