"""Reference checks for Section 4.6."""
import math
from section_4_06 import (finite, period_log_return, cumulative_log_return,
    cumulative_simple_return, price_path_log_return, portfolio_simple_return,
    portfolio_log_return)

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-11), (
        actual, expected)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    changes = (0.10, -0.05, 0.08)
    close(cumulative_simple_return(changes), 0.1286)
    close(cumulative_log_return(changes), math.log(1.1286))
    close(period_log_return(0), 0)
    close(cumulative_log_return(()), 0)
    close(cumulative_simple_return(()), 0)
    close(cumulative_simple_return((-0.2, 0.2)), -0.04)
    close(cumulative_simple_return((-0.2, 0.25)), 0)
    close(price_path_log_return((100, 110, 105)), math.log(1.05))
    close(portfolio_simple_return((0.2, -0.1), (0.5, 0.5)), 0.05)
    close(portfolio_log_return((0.2, -0.1), (0.5, 0.5)), math.log1p(0.05))
    assert not math.isclose(
        portfolio_log_return((0.2, -0.1), (0.5, 0.5)),
        0.5*math.log1p(0.2)+0.5*math.log1p(-0.1),
        rel_tol=1e-12, abs_tol=1e-12)
    close(period_log_return(1e-12), math.log1p(1e-12))
    close(cumulative_simple_return((1e-12, 1e-12)), (1+1e-12)**2-1)
    rejects(ValueError, period_log_return, -1)
    rejects(ValueError, period_log_return, -1.2)
    rejects(ValueError, price_path_log_return, (100,))
    rejects(ValueError, price_path_log_return, (100, 0))
    rejects(ValueError, portfolio_simple_return, (0.1,), (0.4,))
    rejects(ValueError, portfolio_simple_return, (0.1, 0.2), (1,))
    rejects(ValueError, portfolio_simple_return, (-1,), (1,))
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("inf"), "x")
    print("PASS: Section 4.6 reference checks")

if __name__ == "__main__":
    run()
