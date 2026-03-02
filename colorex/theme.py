"""Theme definitions and helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    """Color palette for heatmap rendering."""

    primary: str
    secondary: str
    neutral: str = "#f0f0f0"


_BUILTIN_THEMES = {
    "blue-red": Theme(primary="#08306B", secondary="#CB181D", neutral="#F2F2F2"),
    "green-yellow": Theme(primary="#238B45", secondary="#D4B106", neutral="#F2F2F2"),
    "mono-dark": Theme(primary="#0F172A", secondary="#6B7280", neutral="#D1D5DB"),
    "mono-light": Theme(primary="#374151", secondary="#E5E7EB", neutral="#F3F4F6"),
}


def get_builtin_theme(name: str) -> Theme:
    """Return a built-in theme by name."""
    key = name.strip().lower()
    if key not in _BUILTIN_THEMES:
        valid = ", ".join(sorted(_BUILTIN_THEMES))
        raise ValueError(f"Unknown theme '{name}'. Valid themes: {valid}")
    return _BUILTIN_THEMES[key]


def available_themes() -> list[str]:
    """Return available built-in theme names."""
    return sorted(_BUILTIN_THEMES.keys())