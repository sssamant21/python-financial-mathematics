"""Selected independent rank-screen references for Section 13.6."""
import math
from section_13_06 import solve_qr

def run():
    factors = ("F1", "F2")
    instruments = ("A", "B")
    tolerance = 2.0 ** -20
    # Diagonal matrices isolate the normalized pivot threshold exactly.
    for scale in (1.0, -1.0, 2.0 ** 100, 2.0 ** -100):
        for delta in (0.0, tolerance / 2, tolerance):
            try:
                solve_qr(factors, instruments, ((scale, 0), (0, scale * delta)),
                         factors, (scale, scale * delta), tolerance)
            except ValueError as exc:
                assert "rank-deficient" in str(exc)
            else:
                raise AssertionError("normalized pivot at/below threshold accepted")
        for delta in (2 * tolerance, 4 * tolerance):
            result = solve_qr(factors, instruments,
                              ((scale, 0), (0, scale * delta)),
                              ("F2", "F1"), (scale * delta, scale), tolerance)
            for value in result["positions"].values():
                assert math.isclose(value, 1.0, rel_tol=1e-12, abs_tol=1e-12)
    # Independent exact rational minimizer: x=7/3, y=10/3.
    # Reordering columns must reorder labels, preserving achieved exposures.
    for names, rows in (
        (("A", "B"), ((1, 0), (0, 1), (1, 1))),
        (("B", "A"), ((0, 1), (1, 0), (1, 1))),
    ):
        result = solve_qr(("F1", "F2", "F3"), names, rows,
                          ("F3", "F1", "F2"), (6, 2, 3))
        assert math.isclose(result["positions"]["A"], 7 / 3, abs_tol=1e-12)
        assert math.isclose(result["positions"]["B"], 10 / 3, abs_tol=1e-12)
        for label, expected in zip(("F1", "F2", "F3"), (7 / 3, 10 / 3, 17 / 3)):
            assert math.isclose(result["achieved"][label], expected, abs_tol=1e-12)
        assert math.isclose(result["objective_half_squared_l2"], 1 / 6, abs_tol=1e-12)
    print("PASS: Section 13.6 selected rank-screen and column-order references")

if __name__ == "__main__":
    run()
