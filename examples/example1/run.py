from __future__ import annotations

import csv
import random
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from colorex import Heatmap

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset_50x50.csv"
HTML_OUTPUT = BASE_DIR / "heatmap_50x50.html"
PNG_OUTPUT = BASE_DIR / "heatmap_50x50.png"
GRID_SIZE = 50
SEED = 20260303


def generate_dataset(path: Path, size: int, seed: int) -> None:
    rng = random.Random(seed)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        for r in range(size):
            row = []
            for c in range(size):
                base = ((r + 1) * (c + 1)) / size
                jitter = rng.uniform(-3.0, 3.0)
                row.append(round(base + jitter, 3))
            writer.writerow(row)


def main() -> int:
    if not DATASET_PATH.exists():
        generate_dataset(DATASET_PATH, GRID_SIZE, SEED)

    heatmap = Heatmap(
        str(DATASET_PATH),
        theme="blue-red",
        normalize="linear",
        show_values=False,
        title="Example 1: 50x50 CSV Dataset",
        subtitle="Deterministic generated sample",
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
