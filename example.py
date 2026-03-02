from __future__ import annotations

import csv
import random
from pathlib import Path

from colorex import Heatmap

DATASET_PATH = Path("example_50x50.csv")
HTML_OUTPUT = Path("example_50x50.html")
PNG_OUTPUT = Path("example_50x50.png")
GRID_SIZE = 50
SEED = 20260303


def generate_dataset(path: Path, size: int, seed: int) -> None:
    rng = random.Random(seed)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        for r in range(size):
            row = []
            for c in range(size):
                # Smooth-ish gradient + small noise for more interesting heatmaps.
                base = ((r + 1) * (c + 1)) / size
                jitter = rng.uniform(-3.0, 3.0)
                row.append(round(base + jitter, 3))
            writer.writerow(row)


def main() -> int:
    if not DATASET_PATH.exists():
        generate_dataset(DATASET_PATH, GRID_SIZE, SEED)

    hm = Heatmap(
        str(DATASET_PATH),
        theme="blue-red",
        normalize="linear",
        show_values=False,
        title="ColorEx Example: 50x50 Dataset",
        subtitle="Generated deterministic sample data",
    )

    hm.to_html(HTML_OUTPUT)

    try:
        hm.to_image(PNG_OUTPUT)
        print(f"Wrote {HTML_OUTPUT} and {PNG_OUTPUT}")
    except Exception:
        print(f"Wrote {HTML_OUTPUT} (PNG skipped: install pillow for image export)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())