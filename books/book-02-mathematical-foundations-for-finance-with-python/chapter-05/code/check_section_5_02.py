"""Reference checks for Section 5.2."""
import math
from section_5_02 import arithmetic_term, arithmetic_sum, geometric_term, geometric_sum, future_value_end_deposits, count, finite

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, function, *args):
    try:
        function(*args)
    except error:
        return
    raise AssertionError("Expected " + error.__name__)

def run():
    close(arithmetic_term(7, 3, 4), 19)
    close(arithmetic_sum(5, 2, 10), 140)
    close(arithmetic_sum(100, 10, 4), 460)
    close(arithmetic_sum(10, -2, 0), 0)
    close(arithmetic_sum(10, 0, 5), 50)
    close(geometric_term(100, 1.05, 4), 100 * 1.05**4)
    close(geometric_sum(3, 2, 4), 45)
    close(geometric_sum(3, -2, 4), -15)
    close(geometric_sum(3, 0, 4), 3)
    close(geometric_sum(3, 1, 4), 12)
    close(geometric_sum(3, 2, 0), 0)
    close(future_value_end_deposits(100, 0.1, 3), 331)
    close(future_value_end_deposits(100, 0, 3), 300)
    close(future_value_end_deposits(100, -0.1, 3), 271)
    close(future_value_end_deposits(100, 0.05, 0), 0)
    for n in range(1, 8):
        close(arithmetic_sum(5, 2, n), sum(arithmetic_term(5, 2, k) for k in range(n)))
        close(geometric_sum(2, 1.2, n), sum(geometric_term(2, 1.2, k) for k in range(n)))
    rejects(ValueError, future_value_end_deposits, 100, -1, 2)
    rejects(ValueError, arithmetic_term, 1, 1, -1)
    rejects(TypeError, count, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 5.2 reference checks")

if __name__ == "__main__":
    run()
