"""HTML renderer for Heatmap."""

from __future__ import annotations

from html import escape

from .base import BaseRenderer


class HtmlRenderer(BaseRenderer):
    def __init__(self, show_legend: bool = True) -> None:
        self.show_legend = show_legend

    def render(self, heatmap: object) -> str:
        rows, cols = heatmap.shape
        parts: list[str] = []

        parts.append("<!doctype html>")
        parts.append('<html lang="en">')
        parts.append("<head>")
        parts.append('<meta charset="utf-8">')
        parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
        parts.append("<title>ColorEx Heatmap</title>")
        parts.append("<style>")
        parts.append(self._styles())
        parts.append("</style>")
        parts.append("</head>")
        parts.append("<body>")
        parts.append('<div class="cx-wrap">')

        if heatmap.title:
            parts.append(f'<h1 class="cx-title">{escape(str(heatmap.title))}</h1>')
        if heatmap.subtitle:
            parts.append(f'<p class="cx-subtitle">{escape(str(heatmap.subtitle))}</p>')

        parts.append('<div class="cx-grid" role="grid">')
        for r in range(rows):
            parts.append('<div class="cx-row" role="row">')
            for c in range(cols):
                tile = heatmap.tiles[r][c]
                label = "missing" if tile.value is None else f"{tile.value:g}"
                text = "" if (not heatmap.show_values or tile.value is None) else f"{tile.value:g}"
                parts.append(
                    "".join(
                        [
                            '<div class="cx-tile" ',
                            f'role="gridcell" style="background:{tile.color}" ',
                            f'title="row {r+1}, col {c+1}: {escape(label)}">',
                            f"{escape(text)}",
                            "</div>",
                        ]
                    )
                )
            parts.append("</div>")
        parts.append("</div>")

        if self.show_legend:
            parts.append(self._legend_html(heatmap))

        parts.append("</div>")
        parts.append("</body>")
        parts.append("</html>")
        return "\n".join(parts)

    def _legend_html(self, heatmap: object) -> str:
        return "".join(
            [
                '<div class="cx-legend" aria-label="Legend">',
                f'<span class="cx-legend-label">Low ({escape(heatmap.normalize_mode)})</span>',
                f'<div class="cx-legend-bar" style="background:linear-gradient(90deg, {heatmap.theme.secondary}, {heatmap.theme.primary});"></div>',
                '<span class="cx-legend-label">High</span>',
                "</div>",
            ]
        )

    def _styles(self) -> str:
        return "\n".join(
            [
                ":root { color-scheme: light; }",
                "* { box-sizing: border-box; }",
                "body { margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif; background: #f8fafc; color: #0f172a; }",
                ".cx-wrap { max-width: 1200px; margin: 0 auto; padding: 24px; }",
                ".cx-title { margin: 0 0 8px; font-size: 1.5rem; }",
                ".cx-subtitle { margin: 0 0 20px; color: #475569; }",
                ".cx-grid { display: inline-block; border: 1px solid #d0d7de; background: white; overflow: auto; max-width: 100%; }",
                ".cx-row { display: flex; }",
                ".cx-tile { width: 24px; height: 24px; border: 1px solid rgba(15,23,42,0.08); display: flex; align-items: center; justify-content: center; font-size: 10px; color: rgba(0,0,0,0.75); }",
                ".cx-tile:hover { outline: 2px solid #111827; outline-offset: -2px; }",
                ".cx-legend { display: flex; align-items: center; gap: 12px; margin-top: 16px; }",
                ".cx-legend-label { font-size: 0.875rem; color: #334155; }",
                ".cx-legend-bar { width: 240px; max-width: 50vw; height: 12px; border-radius: 999px; border: 1px solid rgba(15,23,42,0.12); }",
                "@media (max-width: 640px) { .cx-tile { width: 18px; height: 18px; font-size: 8px; } }",
            ]
        )