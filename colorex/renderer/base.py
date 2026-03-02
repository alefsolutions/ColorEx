"""Base renderer contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, heatmap: object):
        """Render a heatmap object into a specific target format."""