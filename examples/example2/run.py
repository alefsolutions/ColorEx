from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from colorex import Heatmap, Theme

BASE_DIR = Path(__file__).resolve().parent
HTML_OUTPUT = BASE_DIR / "heatmap_in_memory.html"
PNG_OUTPUT = BASE_DIR / "heatmap_in_memory.png"


def build_data(rows: int = 20, cols: int = 20) -> list[list[float | None]]:
    data: list[list[float | None]] = []
    for r in range(rows):
        row: list[float | None] = []
        for c in range(cols):
            val = (r * 1.7) + (c * 2.3)
            if (r + c) % 11 == 0:
                row.append(None)
            else:
                row.append(round(val, 2))
        data.append(row)
    return data


def main() -> int:
    theme = Theme(primary="#1D4ED8", secondary="#F59E0B", neutral="#E5E7EB")
    heatmap = Heatmap(
        build_data(),
        theme=theme,
        normalize="quantile",
        show_values=False,
        title="Example 2: In-Memory Data",
        subtitle="Quantile normalization with missing values",
    )

    heatmap.to_html(HTML_OUTPUT)
    try:
        heatmap.to_image(PNG_OUTPUT)
        print(f"Wrote {HTML_OUTPUT} and {PNG_OUTPUT}")
    except Exception:
        print(f"Wrote {HTML_OUTPUT} (PNG skipped: install pillow for image export)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
