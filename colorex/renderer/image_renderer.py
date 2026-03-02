"""PNG image renderer for Heatmap."""

from __future__ import annotations

from pathlib import Path

from ..exceptions import RenderError
from .base import BaseRenderer

try:
    from PIL import Image, ImageDraw
except Exception as exc:  # pragma: no cover - dependency may be absent
    Image = None
    ImageDraw = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


class ImageRenderer(BaseRenderer):
    def __init__(self, tile_size: int = 12, border: int = 1) -> None:
        self.tile_size = tile_size
        self.border = border

    def render(self, heatmap: object):
        if Image is None or ImageDraw is None:
            raise RenderError(
                "Pillow is required for image rendering. Install with: pip install pillow"
            ) from _IMPORT_ERROR

        rows, cols = heatmap.shape
        width = cols * self.tile_size
        height = rows * self.tile_size
        image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(image)

        for r in range(rows):
            for c in range(cols):
                tile = heatmap.tiles[r][c]
                x1 = c * self.tile_size
                y1 = r * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                draw.rectangle((x1, y1, x2, y2), fill=tile.color, outline="#ffffff")

        return image

    def render_to_file(self, heatmap: object, output_path: str | Path) -> None:
        image = self.render(heatmap)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG")

    def show(self, heatmap: object) -> None:
        image = self.render(heatmap)
        image.show()