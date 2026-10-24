"""Reference checks for Section 2.8."""
from fractions import Fraction
from section_2_08 import (q, equation, scale, residual, normalized_residual,
                          solve_one, cash_flow_balance)


def run():
    row = equation(2, 3, 13)
    assert residual(row, 2, 3) == 0
    for factor in ("1/1000000", "-7", "1000000000"):
        scaled = scale(row, factor)
        for point in ((2, 3), (0, 0), (4, 5)):
            assert residual(scaled, *point) == q(factor)*residual(row, *point)
            assert normalized_residual(scaled, *point) == normalized_residual(row, *point)
    assert normalized_residual(row, 0, 0) == 1
    assert normalized_residual(equation(0, 0, 0), 3, 5) == 0
    assert solve_one(4, 20) == ("unique", Fraction(5))
    assert solve_one(0, 0) == ("all", None)
    assert solve_one(0, 1) == ("none", None)
    assert cash_flow_balance(12, 100, 50, 1150) == 0
    assert cash_flow_balance(12, 100, 50, 1200) == -50
    for invalid in (0, "0"):
        try:
            scale(row, invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("zero scale accepted")
    for invalid in (0.5, True):
        try:
            q(invalid)
        except TypeError:
            pass
        else:
            raise AssertionError("inexact or boolean input accepted")
    print("PASS: Section 2.8 reference checks")


if __name__ == "__main__":
    run()
