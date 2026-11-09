import pytest
from forward_diagnostics import forward_table, compare_forwards

CURVE = ((1, .035), (3, .04), (5, .043), (10, .047))

def test_first_forward_equals_first_spot():
    for method in ("rate_linear", "log_discount"):
        assert forward_table(CURVE, method)[0][2] == pytest.approx(.035)

def test_reconstruct_discount_factors():
    for method in ("rate_linear", "log_discount"):
        product = 1.0
        for year, df, forward in forward_table(CURVE, method):
            product /= (1 + forward)
            assert product == pytest.approx(df)

def test_knot_discount_agreement():
    a, b = (forward_table(CURVE, m) for m in ("rate_linear", "log_discount"))
    for year, _ in CURVE:
        assert a[year - 1][1] == pytest.approx(b[year - 1][1])

def test_between_knot_difference():
    assert compare_forwards(CURVE)["max_abs_forward_gap_bps"] > 0

def test_flat_curve_forward():
    curve = ((1, .04), (3, .04), (5, .04))
    for method in ("rate_linear", "log_discount"):
        assert [r[2] for r in forward_table(curve, method)] == pytest.approx([.04] * 5)

def test_shock_does_not_change_base():
    before = compare_forwards(CURVE)
    after = compare_forwards(CURVE, (100, 0, 0, -100))
    assert before["base"] == after["base"]
    assert after["shocked"] != after["base"]

def test_negative_forward_reported():
    curve = ((1, .20), (2, .01))
    assert forward_table(curve, "log_discount")[1][2] < 0

def test_invalid_method():
    with pytest.raises(ValueError): forward_table(CURVE, "cubic")

def test_invalid_shock():
    with pytest.raises(ValueError): compare_forwards(CURVE, (100,))

def test_noninteger_terminal_tenor():
    with pytest.raises(ValueError): forward_table(((1, .03), (2.5, .04)))

def test_input_immutable():
    before = tuple(CURVE)
    compare_forwards(CURVE, (1, 2, 3, 4))
    assert CURVE == before
