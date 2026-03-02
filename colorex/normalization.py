"""Normalization strategies for heatmap data."""

from __future__ import annotations

import bisect
import math
from abc import ABC, abstractmethod

from .exceptions import NormalizationError


class BaseNormalizer(ABC):
    """Strategy interface for normalization."""

    @abstractmethod
    def fit(self, values: list[float]) -> None:
        """Learn global bounds/statistics from numeric values."""

    @abstractmethod
    def transform(self, value: float) -> float:
        """Normalize a single value to range [0.0, 1.0]."""


class LinearNormalizer(BaseNormalizer):
    def __init__(self) -> None:
        self._min = 0.0
        self._max = 1.0

    def fit(self, values: list[float]) -> None:
        if not values:
            raise NormalizationError("Cannot normalize empty numeric input")
        self._min = min(values)
        self._max = max(values)

    def transform(self, value: float) -> float:
        if self._max == self._min:
            return 0.5
        return (value - self._min) / (self._max - self._min)


class LogNormalizer(BaseNormalizer):
    def __init__(self) -> None:
        self._min_log = 0.0
        self._max_log = 1.0
        self._offset = 0.0

    def fit(self, values: list[float]) -> None:
        if not values:
            raise NormalizationError("Cannot normalize empty numeric input")
        min_val = min(values)
        self._offset = 1.0 - min_val if min_val <= 0 else 0.0
        logs = [math.log(v + self._offset) for v in values]
        self._min_log = min(logs)
        self._max_log = max(logs)

    def transform(self, value: float) -> float:
        if self._max_log == self._min_log:
            return 0.5
        log_value = math.log(value + self._offset)
        return (log_value - self._min_log) / (self._max_log - self._min_log)


class QuantileNormalizer(BaseNormalizer):
    def __init__(self) -> None:
        self._sorted: list[float] = []

    def fit(self, values: list[float]) -> None:
        if not values:
            raise NormalizationError("Cannot normalize empty numeric input")
        self._sorted = sorted(values)

    def transform(self, value: float) -> float:
        if not self._sorted:
            raise NormalizationError("QuantileNormalizer must be fit before use")
        n = len(self._sorted)
        if n == 1:
            return 0.5
        idx = bisect.bisect_left(self._sorted, value)
        return idx / (n - 1)


def create_normalizer(mode: str) -> BaseNormalizer:
    key = mode.strip().lower()
    if key == "linear":
        return LinearNormalizer()
    if key == "log":
        return LogNormalizer()
    if key == "quantile":
        return QuantileNormalizer()
    raise NormalizationError("Unknown normalization mode: " + mode)