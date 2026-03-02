![ColorEx](res/header.png)

# ColorEx

ColorEx is a Python heat map library centered around the `CX_HeatMap` engine in `colorexlib/colorex.py`.

## Current Features

- 2D heat maps from numeric grid data.
- CSV input support via `CSVReader`.
- Output to:
  - HTML file (`HTMLWriter`, Cheetah template rendering).
  - Tkinter GUI window (`GUIOutputWriter`) with interactive tile selection and popup values.
- Bi-color interpolation between theme `primary` and `secondary`.
- Tile grouping (`TileGroup`, `TileGroups`) with:
  - custom labels
  - optional fixed colors per group
  - fallback alpha-based group coloring
- Optional numeric value formatting with `DataFormatter`.
- Axis titles and labels.
- Row/column header-aware rendering.
- Theme and stylesheet customization using `Theme` and `StyleSheet`.

## Requirements

- Python 3.7+
- `Cheetah3` (for HTML generation)
- `tkinter` (for GUI output; usually bundled with Python)

## Installation

```bash
pip install colorexlib
```

## Public API (Current)

### Main engine

```python
from colorexlib.colorex import CX_HeatMap
```

### `CX_HeatMap(options)` required options

- `source`: one of
  - CSV filepath `str` ending in `.csv`
  - `DataGrid` instance
- `title`: `str`
- `subtitle`: `str`

### `CX_HeatMap(options)` optional options

- `theme`: `Theme` instance (default: `Theme()`)
- `stylesheet`: `StyleSheet` instance (default: `StyleSheet()`)
- `xaxis_title`: `str` (default: `""`)
- `yaxis_title`: `str` (default: `""`)
- `xaxis_labels`: `list` or `None`
- `yaxis_labels`: `list` or `None`
- `rowcol_headers`: `bool` (default: `True`)
- `data_formatter`: `DataFormatter` or `None`
- `grouping`: `TileGroups` or `None`

### Output methods

- `to_html(html_filename: str)`
  - supported when `source` is a CSV filepath
- `to_gui()`
  - supported when `source` is CSV filepath or `DataGrid`

## Minimal Working Example (CSV -> HTML)

```python
from colorexlib.colorex import CX_HeatMap
from colorexlib.common.styling import Theme

options = {
    "source": "first_example/attendance.csv",
    "title": "Student Attendance",
    "subtitle": "Attendance by month",
    "theme": Theme(
        primaryColor="#d45500",
        secondaryColor="#ffccaa",
        onPrimaryColor="#ffccaa",
        onSecondaryColor="#000000",
    ),
}

heatmap = CX_HeatMap(options)
heatmap.to_html("attendance.html")
```

## Minimal Working Example (CSV -> GUI)

```python
from colorexlib.colorex import CX_HeatMap
from colorexlib.common.styling import Theme

options = {
    "source": "first_example/attendance.csv",
    "title": "Student Attendance",
    "subtitle": "Attendance by month",
    "theme": Theme(),
}

heatmap = CX_HeatMap(options)
heatmap.to_gui()
```

## Core Modules

- `colorexlib/colorex.py`: `CX_HeatMap`
- `colorexlib/common/datastructures.py`: `Data`, `DataGrid`, `Tile`, `HeatMap`, `TileGroup`, `TileGroups`
- `colorexlib/common/styling.py`: `Themes`, `Theme`, `StyleSheet`
- `colorexlib/common/formating.py`: `DataFormatter`
- `colorexlib/readers/CSVReader.py`: CSV input reader
- `colorexlib/writers/HTMLWriter.py`: HTML output writer
- `colorexlib/writers/GUIOutputWriter.py`: Tkinter GUI writer

## Notes About Repository State

- The current runnable class is `CX_HeatMap`.
- HTML output uses an internal template string in `HTMLWriter`; there is no template filename argument in `to_html`.
- Existing files in `examples/` and `first_example/` still show older API usage and do not match the current `CX_HeatMap` interface.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE.md](LICENSE.md).
