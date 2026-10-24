"""Reference checks for Section 5.1."""
import math
from section_5_01 import (
    finite, count, time_grid, payment_for_period,
    balance_path, present_value_end_payments)

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-10), (
        actual, expected)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")

def run():
    grid = time_grid(12, 1/12)
    assert len(grid) == 13
    close(grid[0], 0)
    close(grid[9], 0.75)
    close(grid[-1], 1)
    assert len(time_grid(24, 1/12)) == 25
    assert len(time_grid(0, 1/12)) == 1
    close(payment_for_period((100, 200, 300), 1), 100)
    close(payment_for_period((100, 200, 300), 3), 300)
    end = balance_path(1000, 0.01, (100, 100))
    begin = balance_path(1000, 0.01, (100, 100), timing="begin")
    assert len(end) == 3
    close(end[0], 1000)
    close(end[1], 1110)
    close(end[2], 1221.1)
    close(begin[1], 1111)
    close(begin[2], 1223.11)
    close(balance_path(1000, 0, (100, -50))[-1], 1050)
    close(balance_path(1000, 0.01, ())[-1], 1000)
    close(present_value_end_payments((500,), 0.05), 500/1.05)
    close(present_value_end_payments((100, 100), 0), 200)
    rejects(ValueError, time_grid, 12, 0)
    rejects(ValueError, time_grid, -1, 1/12)
    rejects(TypeError, count, True)
    rejects(ValueError, balance_path, 1000, -1, (100,))
    rejects(IndexError, payment_for_period, (100,), 2)
    rejects(ValueError, payment_for_period, (100,), 0)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 5.1 reference checks")

if __name__ == "__main__":
    run()
