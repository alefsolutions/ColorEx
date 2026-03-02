"""Top-level package for ColorEx."""

from .heatmap import Heatmap
from .theme import Theme, get_builtin_theme

__all__ = ["Heatmap", "Theme", "get_builtin_theme"]
__version__ = "0.2.0"