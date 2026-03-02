import pytest

from colorex import Heatmap


def test_heatmap_accepts_2d_list():
    hm = Heatmap([[1, 2], [3, 4]], title="A")
    assert hm.shape == (2, 2)
    assert hm.title == "A"


def test_heatmap_accepts_csv_path(tmp_path):
    path = tmp_path / "sample.csv"
    path.write_text("1,2\n3,4\n", encoding="utf-8")
    hm = Heatmap(str(path))
    assert hm.shape == (2, 2)


@pytest.mark.skipif(
    __import__("importlib").util.find_spec("pandas") is None,
    reason="pandas not installed",
)
def test_heatmap_accepts_dataframe():
    import pandas as pd

    df = pd.DataFrame([[1, 2], [3, 4]], columns=["a", "b"], index=["x", "y"])
    hm = Heatmap(df)
    assert hm.shape == (2, 2)
    assert hm.x_labels == ["a", "b"]
    assert hm.y_labels == ["x", "y"]