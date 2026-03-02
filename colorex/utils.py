"""Utility functions for data coercion and color interpolation."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable

from .exceptions import DataValidationError

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pd = None


def is_dataframe(value: object) -> bool:
    return pd is not None and isinstance(value, pd.DataFrame)


def load_csv(path: str | Path) -> list[list[object]]:
    p = Path(path)
    if not p.exists():
        raise DataValidationError(f"CSV file not found: {p}")
    rows: list[list[object]] = []
    with p.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            rows.append([parse_cell(item) for item in row])
    return rows


def parse_cell(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return float(value)
    text = str(value).strip()
    if text == "":
        return None
    try:
        numeric = float(text)
    except ValueError:
        return text
    if math.isnan(numeric):
        return None
    return numeric


def coerce_to_grid(data: object) -> tuple[list[list[object]], list[str] | None, list[str] | None]:
    if isinstance(data, (str, Path)):
        return load_csv(str(data)), None, None

    if is_dataframe(data):
        df = data  # type: ignore[assignment]
        values = [[parse_cell(v) for v in row] for row in df.to_numpy().tolist()]
        x_labels = [str(c) for c in df.columns.tolist()]
        y_labels = [str(i) for i in df.index.tolist()]
        return values, x_labels, y_labels

    if isinstance(data, list):
        if not data:
            raise DataValidationError("Input data list cannot be empty")
        if not all(isinstance(row, list) for row in data):
            raise DataValidationError("Input must be a 2D list")
        width = len(data[0])
        if width == 0:
            raise DataValidationError("Input data contains an empty row")
        if not all(len(row) == width for row in data):
            raise DataValidationError("All rows must have the same length")
        return [[parse_cell(v) for v in row] for row in data], None, None

    raise DataValidationError(
        "Unsupported input type. Expected pandas.DataFrame, 2D list, or CSV path"
    )


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    value = color.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Invalid hex color: {color}")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def lerp_color(start: str, end: str, t: float) -> str:
    t = max(0.0, min(1.0, t))
    sr, sg, sb = hex_to_rgb(start)
    er, eg, eb = hex_to_rgb(end)
    rgb = (
        int(sr + (er - sr) * t),
        int(sg + (eg - sg) * t),
        int(sb + (eb - sb) * t),
    )
    return rgb_to_hex(rgb)


def flatten_numeric(grid: Iterable[Iterable[object]]) -> list[float]:
    values: list[float] = []
    for row in grid:
        for value in row:
            if isinstance(value, (int, float)):
                values.append(float(value))
    return values