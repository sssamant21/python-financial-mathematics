"""Reference checks for Section 8.3."""
import math
from section_8_03 import (
    finite, product_derivative, quotient_derivative, revenue, marginal_revenue,
    average_cost, average_cost_derivative, coverage_ratio,
    coverage_ratio_derivative, discounted_value, discounted_value_derivative,
    centered_difference)

def close(a, b, rel_tol=1e-8, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, function, *args):
    try:
        function(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    for x in (-3, -1, 0, 1, 2, 5):
        actual = product_derivative(lambda z:z*z, lambda z:2*z,
                                    lambda z:3*z+1, lambda z:3, x)
        close(actual, 9*x*x+2*x)
    for x in (-4, -1, 0, 1, 2, 5):
        actual = quotient_derivative(lambda z:z*z+1, lambda z:2*z,
                                     lambda z:z+2, lambda z:1, x)
        close(actual, (x*x+4*x-1)/(x+2)**2)
    rejects(ValueError, quotient_derivative, lambda x:1, lambda x:0,
            lambda x:x-2, lambda x:1, 2)
    for q in (10, 100, 200, 350):
        close(marginal_revenue(q), 120-0.6*q)
        close(centered_difference(revenue, q), marginal_revenue(q))
        close(average_cost_derivative(q), 0.1-500/(q*q))
        close(centered_difference(average_cost, q), average_cost_derivative(q))
    close(marginal_revenue(100), 60)
    close(average_cost_derivative(100), 0.05)
    for t in (0, 1, 3, 10):
        close(coverage_ratio_derivative(t), 100/(50+3*t)**2)
        close(centered_difference(coverage_ratio, t), coverage_ratio_derivative(t))
        value = lambda x: discounted_value(x, 0.05, lambda z:100+2*z, lambda z:2)
        slope = discounted_value_derivative(t, 0.05, lambda z:100+2*z, lambda z:2)
        if t > 0:
            close(centered_difference(value, t), slope)
    close(coverage_ratio_derivative(0), 0.04)
    rejects(ValueError, average_cost, 0)
    rejects(ValueError, average_cost_derivative, -1)
    rejects(ValueError, revenue, -1)
    rejects(ValueError, centered_difference, lambda x:x*x, 1, 0)
    rejects(ValueError, discounted_value_derivative, -1, 0.05, lambda t:1, lambda t:0)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.3 reference checks")

if __name__ == "__main__":
    run()
