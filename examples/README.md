# Examples

Run these from the project root.

## Example 1

Deterministic 50x50 CSV dataset rendered to HTML (+ PNG when Pillow is available).

```bash
python examples/example1/run.py
```

Outputs:
- `examples/example1/dataset_50x50.csv`
- `examples/example1/heatmap_50x50.html`
- `examples/example1/heatmap_50x50.png` (if Pillow installed)

## Example 2

In-memory 20x20 data with missing values and custom theme.

```bash
python examples/example2/run.py
```

Outputs:
- `examples/example2/heatmap_in_memory.html`
- `examples/example2/heatmap_in_memory.png` (if Pillow installed)

## Example 3

CLI-driven render from CSV.

```bash
python examples/example3/run.py
```

Outputs:
- `examples/example3/dataset_cli.csv`
- `examples/example3/heatmap_cli.html`