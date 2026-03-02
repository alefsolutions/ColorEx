from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset_cli.csv"
HTML_OUTPUT = BASE_DIR / "heatmap_cli.html"


def generate_dataset(path: Path) -> None:
    rows = [
        [10, 15, 20, 40, 60],
        [8, 12, 22, 44, 66],
        [6, 20, 28, 42, 68],
        [4, 18, 26, 48, 72],
        [2, 16, 24, 50, 80],
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def main() -> int:
    if not DATASET_PATH.exists():
        generate_dataset(DATASET_PATH)

    cmd = [
        sys.executable,
        "-m",
        "colorex.cli",
        "render",
        str(DATASET_PATH),
        "--out",
        str(HTML_OUTPUT),
        "--theme",
        "mono-dark",
        "--normalize",
        "log",
        "--show-values",
        "--title",
        "Example 3: CLI Render",
        "--subtitle",
        "Rendered through the colorex CLI",
    ]

    completed = subprocess.run(cmd, check=False)
    if completed.returncode != 0:
        return completed.returncode

    print(f"Wrote {HTML_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())