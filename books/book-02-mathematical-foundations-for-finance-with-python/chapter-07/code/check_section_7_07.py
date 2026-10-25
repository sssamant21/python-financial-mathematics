"""Reference checks for Section 7.7."""
import math
from section_7_07 import finite, bisection, project_profit, bond_yield_residual

def close(a, b, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=abs_tol), (a, b)

def rejects(error, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    root, bracket, count = bisection(lambda x: x*x-2, 1, 2)
    close(root, math.sqrt(2))
    assert bracket[0] <= math.sqrt(2) <= bracket[1]
    assert count > 0 and bracket[1]-bracket[0] <= 2e-10
    root, bracket, count = bisection(lambda x: x-1, 1, 3)
    assert (root, bracket, count) == (1, (1, 1), 0)
    root, bracket, count = bisection(lambda x: x-3, 1, 3)
    assert (root, bracket, count) == (3, (3, 3), 0)
    root, bracket, count = bisection(lambda x: x-1.5, 1, 2)
    close(root, 1.5)
    close(project_profit(125), 0)
    close(project_profit(100), -200)
    close(project_profit(200), 600)
    root, bracket, count = bisection(project_profit, 100, 200)
    close(root, 125)
    residual = lambda y: bond_yield_residual(y, (50, 1050), 1000)
    close(residual(0.05), 0)
    assert residual(0) > 0 and residual(0.1) < 0
    root, bracket, count = bisection(residual, 0, 0.1)
    close(root, 0.05)
    rejects(ValueError, bisection, lambda x: x*x+1, -1, 1)
    rejects(ValueError, bisection, lambda x: x, 2, 1)
    rejects(ValueError, bisection, lambda x: x, -1, 1, tolerance=0)
    rejects(ValueError, bisection, lambda x: x, -1, 1, max_iterations=0)
    rejects(RuntimeError, bisection, lambda x: x*x-2, 1, 2, tolerance=1e-20, max_iterations=1)
    rejects(ValueError, bond_yield_residual, -1, (50, 1050), 1000)
    rejects(ValueError, bond_yield_residual, 0.05, (), 1000)
    rejects(ValueError, bond_yield_residual, 0.05, (50, -10), 1000)
    rejects(ValueError, bond_yield_residual, 0.05, (50, 1050), 0)
    rejects(ValueError, project_profit, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 7.7 reference checks")

if __name__ == "__main__":
    run()
