from colorex.normalization import create_normalizer


def test_linear_normalization_bounds():
    norm = create_normalizer("linear")
    norm.fit([0.0, 50.0, 100.0])
    assert norm.transform(0.0) == 0.0
    assert norm.transform(100.0) == 1.0


def test_log_normalization_monotonic():
    norm = create_normalizer("log")
    norm.fit([1.0, 10.0, 100.0])
    a = norm.transform(1.0)
    b = norm.transform(10.0)
    c = norm.transform(100.0)
    assert 0.0 <= a < b < c <= 1.0


def test_quantile_normalization():
    norm = create_normalizer("quantile")
    norm.fit([1.0, 2.0, 3.0, 4.0])
    mid = norm.transform(3.0)
    assert 0.0 <= mid <= 1.0