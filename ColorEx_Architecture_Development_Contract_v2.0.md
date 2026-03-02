# ColorEx Architecture & Development Contract

**Project:** ColorEx\
**Owner:** Louis Ronald\
**Language:** Python\
**Target:** PyPI-distributed package\
**Version:** 2.0.0 (Modernization Specification)\
**Generated On:** 2026-03-02 15:38 UTC

------------------------------------------------------------------------

## 1. Project Purpose

ColorEx is a lightweight Python library for rendering tabular numeric
data into clean, interpretable 2D heatmaps.

Goals: - Maintain simplicity - Avoid AI features - Modernize
architecture - Package for PyPI - Improve extensibility and developer
experience

------------------------------------------------------------------------

## 2. Design Philosophy

1.  Minimal API surface\
2.  Strong typing\
3.  Deterministic rendering\
4.  No unnecessary dependencies\
5.  HTML-first visualization\
6.  Pandas-friendly\
7.  Clear separation of concerns

------------------------------------------------------------------------

## 3. Target Package Structure

    colorex/
    │
    ├── __init__.py
    ├── heatmap.py
    ├── theme.py
    ├── normalization.py
    ├── renderer/
    │   ├── __init__.py
    │   ├── html_renderer.py
    │   ├── image_renderer.py
    │   └── base.py
    │
    ├── cli.py
    ├── utils.py
    └── exceptions.py

    tests/
    docs/
    pyproject.toml
    README.md
    CHANGELOG.md
    LICENSE

------------------------------------------------------------------------

## 4. Packaging Requirements

### 4.1 Build System

-   Use `pyproject.toml`
-   Backend: `setuptools` or `hatchling`
-   Python ≥ 3.9

### 4.2 Metadata

-   Name: `colorex`
-   License: MIT
-   Semantic Versioning (SemVer)
-   Classifiers:
    -   Visualization
    -   Data Processing
    -   Python 3

### 4.3 CLI Entry

    colorex render input.csv --out output.html

------------------------------------------------------------------------

## 5. Public API Specification

### Core Object

``` python
from colorex import Heatmap

hm = Heatmap(data)
hm.to_html("output.html")
hm.show()
```

### Constructor Signature

``` python
Heatmap(
    data,
    theme=None,
    normalize="linear",
    show_values=False,
    title=None,
    subtitle=None,
)
```

### Accepted Data

-   pandas.DataFrame
-   2D list of numeric values
-   CSV file path

------------------------------------------------------------------------

## 6. Data Handling Rules

### Missing Values

-   Default: convert to None and render as neutral gray
-   Optional: raise error

### Normalization Modes

-   linear
-   log
-   quantile

Implemented using strategy pattern.

------------------------------------------------------------------------

## 7. Theme System

``` python
from dataclasses import dataclass

@dataclass
class Theme:
    primary: str
    secondary: str
    neutral: str = "#f0f0f0"
```

Built-in Themes: - BlueRed - GreenYellow - MonoDark - MonoLight

------------------------------------------------------------------------

## 8. Rendering Layer

### Base Renderer

``` python
class BaseRenderer:
    def render(self, heatmap):
        pass
```

### HTML Renderer Requirements

-   Modern HTML5
-   Embedded CSS
-   Hover tooltip per tile
-   Optional legend bar
-   Responsive layout
-   Deterministic output

### Image Renderer

-   PNG output
-   Use Pillow or matplotlib backend
-   No GUI dependencies

------------------------------------------------------------------------

## 9. CLI Specification

Example:

    colorex render input.csv \
      --out output.html \
      --theme blue-red \
      --normalize linear \
      --show-values

Must: - Handle errors gracefully - Exit with non-zero code on failure

------------------------------------------------------------------------

## 10. Performance Constraints

-   Handle 500x500 grid efficiently
-   Avoid O(n²) string concatenation
-   Use list joins for HTML generation

------------------------------------------------------------------------

## 11. Testing Requirements

-   Use pytest
-   Minimum 80% coverage
-   Test normalization, interpolation, missing handling, HTML structure,
    CLI parsing

------------------------------------------------------------------------

## 12. Documentation Requirements

README must include: 1. Quickstart 2. DataFrame example 3. CSV example
4. CLI usage 5. Theme customization 6. API reference

------------------------------------------------------------------------

## 13. CI Requirements

GitHub Actions: - Install dependencies - Run ruff - Run black check -
Run pytest - Build wheel

------------------------------------------------------------------------

## 14. Versioning Plan

### v0.1.0

-   Modern core API
-   HTML renderer
-   DataFrame support
-   PyPI release

### v0.2.0

-   CLI
-   Themes
-   Legend + tooltips
-   Image export

### v1.0.0

-   Performance optimizations
-   Stable public API
-   Complete documentation

------------------------------------------------------------------------

## 15. Non-Goals

-   No AI integration
-   No database connectors
-   No streaming dashboards
-   No heavy JS frameworks

------------------------------------------------------------------------

## 16. Definition of Done

-   `pip install colorex` works
-   Quickstart runs in \<60 seconds
-   CLI renders valid HTML
-   Tests pass in CI
-   Package versioned and tagged

------------------------------------------------------------------------

## 17. Ownership & Governance

-   Louis Ronald retains project ownership
-   MIT License
-   Public GitHub repository
-   Accept pull requests after v1.0
