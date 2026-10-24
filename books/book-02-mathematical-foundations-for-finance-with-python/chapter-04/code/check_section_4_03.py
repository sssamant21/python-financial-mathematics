"""Reference checks for Section 4.3."""
import math
from section_4_03 import (finite_positive, log_product, log_quotient,
                          log_power, log_return, cumulative_log_return,
                          simple_return_from_log)

def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), (
        actual, expected)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")

def run():
    close(log_product(4, 5), math.log(20))
    close(log_quotient(20, 2), math.log(10))
    close(log_power(5, 3), math.log(125))
    close(log_product(1.1, 1.05), math.log(1.1*1.05))
    close(log_return(100, 110), math.log(1.1))
    close(log_return(110, 105), math.log(105/110))
    close(cumulative_log_return([100, 110, 105]), math.log(1.05))
    close(simple_return_from_log(cumulative_log_return([100, 110, 105])), 0.05)
    close(log_return(100, 100), 0)
    close(log_return(100, 100*(1+1e-12)), math.log1p(1e-12))
    close(simple_return_from_log(math.log1p(1e-12)), 1e-12)
    for prices in ([100, 110], [100, 110, 105], [20, 30, 15, 40]):
        close(cumulative_log_return(prices), log_return(prices[0], prices[-1]))
    assert not math.isclose(math.log(2+3), math.log(2)+math.log(3),
                            rel_tol=1e-12, abs_tol=1e-12)
    rejects(ValueError, finite_positive, 0, "x")
    rejects(ValueError, finite_positive, -2, "x")
    rejects(ValueError, finite_positive, float("inf"), "x")
    rejects(ValueError, finite_positive, float("nan"), "x")
    rejects(TypeError, finite_positive, True, "x")
    rejects(ValueError, log_return, 100, 0)
    rejects(ValueError, cumulative_log_return, [100])
    rejects(ValueError, cumulative_log_return, [100, -1])
    rejects(TypeError, log_power, 2, True)
    print("PASS: Section 4.3 reference checks")

if __name__ == "__main__":
    run()
