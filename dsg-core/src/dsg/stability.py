from __future__ import annotations

from typing import Any, Dict


class StabilityAnalyzer:
    def compute_stability(self, current: Dict[str, Any], proposed: Dict[str, Any]) -> float:
        try:
            current_value = float(current.get("value", 1.0))
            proposed_value = float(proposed.get("value", 1.0))
            drift = abs(proposed_value - current_value) / (abs(current_value) + 1e-9)
            return round(1 / (1 + drift), 4)
        except Exception:
            return 0.0
