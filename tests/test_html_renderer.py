from pathlib import Path

from colorex import Heatmap


def test_html_contains_expected_structure(tmp_path: Path):
    hm = Heatmap([[1, 2], [3, None]], show_values=True, title="T")
    out = tmp_path / "out.html"
    html = hm.to_html(out)

    assert out.exists()
    assert "<!doctype html>" in html
    assert "cx-grid" in html
    assert "cx-tile" in html
    assert "title=\"row 1, col 1:" in html
    assert "cx-legend" in html


def test_html_legend_toggle(tmp_path: Path):
    hm = Heatmap([[1, 2], [3, 4]])
    html = hm.to_html(tmp_path / "out2.html", legend=False)
    assert '<div class="cx-legend"' not in html
