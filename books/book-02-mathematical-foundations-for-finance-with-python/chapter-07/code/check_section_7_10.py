"""Reference checks for Section 7.10."""
import math
from section_7_10 import (
    finite, discrete_future_value, continuous_future_value,
    continuous_present_value, effective_from_continuous,
    continuous_from_effective, log_return, annuity_factor,
    bond_residual, bisection)

def close(a, b, rel_tol=1e-10, abs_tol=1e-9):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    close(discrete_future_value(2500, 0.06, 1, 3), 2500*(1.06)**3)
    close(continuous_future_value(2500, 0.06, 3), 2500*math.exp(0.18))
    close(continuous_present_value(10000, 0.03, 4), 10000*math.exp(-0.12))
    close(effective_from_continuous(0.05), math.exp(0.05)-1)
    close(continuous_from_effective(0.08), math.log(1.08))
    close(log_return(100, 103), math.log(1.03))
    close(continuous_future_value(1, -0.01, 2), math.exp(-0.02))
    close(math.expm1(-0.007), math.exp(-0.007)-1)
    for n in (0, 1, 5, 10):
        for r in (-0.1, 0, 1e-10, 0.05):
            close(annuity_factor(r, n), math.fsum((1+r)**k for k in range(n)))
    close(annuity_factor(0, 10), 10)
    close(bond_residual(0.06), 0)
    assert bond_residual(0) > 0 and bond_residual(0.2) < 0
    root, bracket, iterations = bisection(bond_residual, 0, 0.2)
    close(root, 0.06)
    assert bracket[0] <= 0.06 <= bracket[1]
    assert iterations > 0 and bracket[1]-bracket[0] <= 2e-10
    rejects(ValueError, discrete_future_value, 100, 0.05, 0, 1)
    rejects(ValueError, discrete_future_value, 100, -2, 1, 1)
    rejects(ValueError, continuous_present_value, 100, 0.05, -1)
    rejects(ValueError, continuous_from_effective, -1)
    rejects(ValueError, log_return, 0, 100)
    rejects(ValueError, annuity_factor, -1, 10)
    rejects(ValueError, bisection, bond_residual, 0.2, 0.3)
    rejects(RuntimeError, bisection, lambda x: x*x-2, 1, 2,
            tolerance=1e-20, max_iterations=1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 7.10 chapter review reference checks")

if __name__ == "__main__":
    run()
