"""Core Heatmap API."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .exceptions import DataValidationError
from .normalization import create_normalizer
from .theme import Theme, get_builtin_theme
from .utils import coerce_to_grid, flatten_numeric, lerp_color


@dataclass(frozen=True)
class Tile:
    row: int
    col: int
    value: float | None
    normalized: float | None
    color: str


class Heatmap:
    """Public Heatmap object.

    Signature intentionally follows the architecture contract.
    """

    def __init__(
        self,
        data: Any,
        theme: Theme | str | None = None,
        normalize: str = "linear",
        show_values: bool = False,
        title: str | None = None,
        subtitle: str | None = None,
        *,
        strict_missing: bool = False,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.show_values = bool(show_values)
        self.normalize_mode = normalize
        self.strict_missing = strict_missing

        if theme is None:
            self.theme = get_builtin_theme("blue-red")
        elif isinstance(theme, Theme):
            self.theme = theme
        elif isinstance(theme, str):
            self.theme = get_builtin_theme(theme)
        else:
            raise TypeError("theme must be Theme, str, or None")

        grid, x_labels, y_labels = coerce_to_grid(data)
        self.grid = self._validate_numeric_grid(grid)
        self.x_labels = x_labels
        self.y_labels = y_labels

        self._normalizer = create_normalizer(normalize)
        numeric = flatten_numeric(self.grid)
        if not numeric:
            raise DataValidationError("Heatmap requires at least one numeric value")
        self._normalizer.fit(numeric)

        self.tiles = self._build_tiles()

    def _validate_numeric_grid(self, grid: list[list[object]]) -> list[list[float | None]]:
        validated: list[list[float | None]] = []
        for row in grid:
            out_row: list[float | None] = []
            for item in row:
                if item is None:
                    if self.strict_missing:
                        raise DataValidationError("Missing values detected with strict_missing=True")
                    out_row.append(None)
                elif isinstance(item, (int, float)):
                    out_row.append(float(item))
                else:
                    raise DataValidationError(
                        f"Non-numeric value detected: {item!r}. Input must be numeric or missing."
                    )
            validated.append(out_row)
        return validated

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.grid), len(self.grid[0])

    def _build_tiles(self) -> list[list[Tile]]:
        rows, cols = self.shape
        tiles: list[list[Tile]] = []
        for r in range(rows):
            tile_row: list[Tile] = []
            for c in range(cols):
                value = self.grid[r][c]
                if value is None:
                    tile_row.append(
                        Tile(
                            row=r,
                            col=c,
                            value=None,
                            normalized=None,
                            color=self.theme.neutral,
                        )
                    )
                    continue
                normalized = self._normalizer.transform(value)
                color = lerp_color(self.theme.secondary, self.theme.primary, normalized)
                tile_row.append(
                    Tile(
                        row=r,
                        col=c,
                        value=value,
                        normalized=normalized,
                        color=color,
                    )
                )
            tiles.append(tile_row)
        return tiles

    def to_html(self, output_path: str | Path, *, legend: bool = True) -> str:
        from .renderer.html_renderer import HtmlRenderer

        renderer = HtmlRenderer(show_legend=legend)
        html = renderer.render(self)
        Path(output_path).write_text(html, encoding="utf-8")
        return html

    def to_image(self, output_path: str | Path) -> None:
        from .renderer.image_renderer import ImageRenderer

        renderer = ImageRenderer()
        renderer.render_to_file(self, output_path)

    def show(self) -> None:
        """Display the heatmap as an image using Pillow's default viewer."""
        from .renderer.image_renderer import ImageRenderer

        renderer = ImageRenderer()
        renderer.show(self)