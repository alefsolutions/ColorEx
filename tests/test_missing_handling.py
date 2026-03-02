import pytest

from colorex import Heatmap
from colorex.exceptions import DataValidationError


def test_missing_values_default_to_neutral():
    hm = Heatmap([[1, None], [2, 3]])
    assert hm.tiles[0][1].value is None
    assert hm.tiles[0][1].color == hm.theme.neutral


def test_missing_values_strict_mode_raises():
    with pytest.raises(DataValidationError):
        Heatmap([[1, None], [2, 3]], strict_missing=True)


def test_rejects_non_numeric_cells():
    with pytest.raises(DataValidationError):
        Heatmap([[1, "abc"], [2, 3]])