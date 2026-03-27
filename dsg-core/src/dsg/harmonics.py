from __future__ import annotations

from typing import Iterable, Tuple


class HarmonicEngine:
    def __init__(self, floor: float = 0.05) -> None:
        self.floor = floor

    def compute_center(self, signals: Iterable[float]) -> float:
        values = [max(float(v), self.floor) for v in signals]
        if not values:
            return 0.0
        return len(values) / sum(1.0 / v for v in values)

    def evaluate_phase(
        self,
        signals: Iterable[float],
        unity_t: float = 0.05,
        tuning_t: float = 0.2,
    ) -> Tuple[str, float, float]:
        values = [float(v) for v in signals]
        if not values:
            return "CHAOS", 1.0, 0.0

        center = self.compute_center(values)
        entropy = sum(abs(v - center) for v in values) / len(values)

        if entropy < unity_t:
            return "UNITY", entropy, center
        if entropy < tuning_t:
            return "TUNING", entropy, center
        return "CHAOS", entropy, center
