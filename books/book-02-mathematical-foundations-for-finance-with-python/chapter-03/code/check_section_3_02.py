"""Reference checks for Section 3.2."""
from fractions import Fraction as F
from section_3_02 import (rational, coordinates, break_even, slope_between,
                          render_ascii)


def rejects(exception, fn, *args):
    try:
        fn(*args)
    except exception:
        return
    raise AssertionError(f"Expected {exception.__name__}")


def run():
    rows = coordinates(25, 15, 40, 6)
    assert len(rows) == 7
    assert rows[0] == (0, 0, 40, -40)
    assert rows[4] == (4, 100, 100, 0)
    assert rows[6] == (6, 150, 130, 20)
    assert all(revenue-cost == profit for _, revenue, cost, profit in rows)
    assert all(rows[i+1][1]-rows[i][1] == 25 for i in range(6))
    assert all(rows[i+1][2]-rows[i][2] == 15 for i in range(6))
    assert all(rows[i+1][3]-rows[i][3] == 10 for i in range(6))
    assert break_even(25, 15, 40) == ("unique", F(4))
    assert break_even(10, 10, 0) == ("all", None)
    assert break_even(10, 10, 40) == ("none", None)
    assert break_even(5, 10, 40) == ("outside_domain", F(-8))
    assert break_even(10, 15, 0) == ("unique", F(0))
    assert slope_between((0, -40), (4, 0)) == 10
    assert slope_between((0, 40), (4, 100)) == 15
    assert "4 | 100 | 100 | 0" in render_ascii(25, 15, 40, 6)
    rejects(ValueError, coordinates, 25, 15, 40, "5/2")
    rejects(ValueError, coordinates, 25, 15, 40, -1)
    rejects(ValueError, coordinates, -1, 15, 40, 4)
    rejects(ValueError, slope_between, (2, 3), (2, 7))
    rejects(TypeError, rational, 0.1)
    rejects(TypeError, rational, True)
    print("PASS: Section 3.2 reference checks")


if __name__ == "__main__":
    run()
