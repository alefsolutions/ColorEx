<img src="assets/github-banner.png" alt="GitHub Banner" width="100%" />

# ColorEx

ColorEx is a lightweight Python library for rendering tabular numeric data into deterministic 2D heatmaps.

## Quickstart

```bash
pip install colorex
```

```python
from colorex import Heatmap

hm = Heatmap(
    [[1, 5, 2], [3, 9, 4], [6, 7, 8]],
    title="Quickstart",
    subtitle="Linear normalization",
)
hm.to_html("output.html")
```

## DataFrame Example

```python
import pandas as pd
from colorex import Heatmap

# Requires: pip install "colorex[pandas]"
df = pd.DataFrame(
    [[10, 20, 30], [40, None, 60], [70, 80, 90]],
    columns=["A", "B", "C"],
    index=["r1", "r2", "r3"],
)

hm = Heatmap(df, normalize="quantile", title="DataFrame Heatmap")
hm.to_html("df_heatmap.html")
```

## CSV Example

```python
from colorex import Heatmap

hm = Heatmap(
    "input.csv",
    normalize="log",
    show_values=True,
    title="CSV Heatmap",
)
hm.to_html("csv_heatmap.html")
hm.to_image("csv_heatmap.png")
```

## CLI Usage

```bash
colorex render input.csv --out output.html --theme blue-red --normalize linear --show-values
```

PNG output:

```bash
colorex render input.csv --out output.png --theme mono-dark --normalize quantile
```

## Theme Customization

Built-in themes:
- `blue-red`
- `green-yellow`
- `mono-dark`
- `mono-light`

Use a built-in theme:

```python
from colorex import Heatmap

hm = Heatmap([[1, 2], [3, 4]], theme="green-yellow")
```

Use a custom theme:

```python
from colorex import Heatmap, Theme

custom = Theme(primary="#1D4ED8", secondary="#F59E0B", neutral="#E5E7EB")
hm = Heatmap([[1, None], [3, 4]], theme=custom)
```

## API Reference

### `Heatmap`

```python
Heatmap(
    data,
    theme=None,
    normalize="linear",
    show_values=False,
    title=None,
    subtitle=None,
)
```

Accepted `data`:
- `pandas.DataFrame`
- 2D list of numeric values (`None` allowed)
- CSV file path

Behavior:
- Missing values default to `None` and render using theme `neutral`.
- Optional strict mode: `Heatmap(..., strict_missing=True)` raises on missing values.
- Normalization modes: `linear`, `log`, `quantile`.

Methods:
- `to_html(path, legend=True) -> str`
- `to_image(path) -> None` (requires Pillow)
- `show() -> None` (opens image with system viewer; requires Pillow)

## Current Limitations

- No native Tkinter interactive window renderer in the current `colorex` package.
- HTML output is renderer-defined; there is no external template/plugin system yet.
- `show()` is an image preview path (via Pillow), not an interactive heatmap UI.
- PNG export depends on optional Pillow installation.
- DataFrame support requires optional pandas installation (`colorex[pandas]`).
- The current renderer focuses on cell color/value visualization and does not yet expose advanced chart features (for example: clustering, annotations, or dashboard embedding components).

## Development

Install dev dependencies:

```bash
pip install -e ".[dev,pandas,image]"
pytest
```

## Examples

Runnable examples are in `examples/`:

- `python examples/example1/run.py` (50x50 CSV dataset)
- `python examples/example2/run.py` (in-memory data with missing values)
- `python examples/example3/run.py` (CLI-driven rendering)

## License

Apache License 2.0. See [LICENSE.md](LICENSE.md).
