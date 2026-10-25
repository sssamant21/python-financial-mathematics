"""Reference checks for Section 6.1."""
import math
from section_6_01 import (
    finite, net_cash_flow, accumulation_factor, future_value, iterative_value)

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-10), (
        actual, expected)

def rejects(error, function, *args):
    try:
        function(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(net_cash_flow(()), 0)
    close(accumulation_factor(()), 1)
    close(net_cash_flow((100, -40, 60)), 120)
    close(accumulation_factor((0.02, -0.01, 0.03)), 1.040094)
    close(future_value(1000, (), ()), 1000)
    close(future_value(1000, (0.02, -0.01, 0.03), (0, 0, 0)),
          1040.094)
    close(future_value(1000, (0.02, -0.01), (100, -50)), 1058.8)
    close(iterative_value(1000, (0.02, -0.01), (100, -50)), 1058.8)
    for n in range(8):
        rates = tuple(0.01 * ((k % 3) - 1) for k in range(n))
        flows = tuple((k % 2) * 25 - 10 for k in range(n))
        close(future_value(500, rates, flows),
              iterative_value(500, rates, flows))
    rejects(ValueError, future_value, 100, (0.01,), ())
    rejects(ValueError, accumulation_factor, (-1,))
    rejects(ValueError, future_value, 100, (-1,), (0,))
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("inf"), "x")
    print("PASS: Section 6.1 reference checks")

if __name__ == "__main__":
    run()
