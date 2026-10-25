"""Reference checks for Section 7.9 capstone."""
import math
from section_7_09 import (
    finite, removable_raw, removable_extension, threshold_fee,
    vertical_sample, annuity_accumulation, annuity_sum_reference,
    bond_residual, bisection)

def close(a, b, rel_tol=1e-9, abs_tol=1e-9):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(error, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    # A: removable singularity and continuous extension
    rejects(ValueError, removable_raw, 3)
    close(removable_extension(3), 6)
    for x in (0, 2, 2.9, 3.1, 4):
        close(removable_raw(x), removable_extension(x))
    # B: exact threshold contract
    assert threshold_fee(999.99) == 5
    assert threshold_fee(1000) == 10
    assert threshold_fee(1000.01) == 10
    rejects(ValueError, threshold_fee, -1)
    # C: asymptote sampling
    rejects(ValueError, vertical_sample, 2)
    previous = 0
    for d in (0.1, 0.01, 0.001):
        left, right = vertical_sample(2-d), vertical_sample(2+d)
        assert left < 0 < right
        assert abs(left) > previous
        previous = abs(left)
        close(abs(left), abs(right), rel_tol=1e-10)
    # D: independent finite-sum identity
    for n in (0, 1, 2, 12, 30):
        for rate in (-0.1, 0, 1e-10, 0.02, 0.1):
            close(annuity_accumulation(rate, n),
                  annuity_sum_reference(rate, n))
    assert annuity_accumulation(0, 12) == 12
    rejects(ValueError, annuity_accumulation, -1, 12)
    rejects(TypeError, annuity_accumulation, 0, True)
    # E: yield and audit record
    assert bond_residual(0) > 0 and bond_residual(0.1) < 0
    close(bond_residual(0.05), 0)
    result = bisection(bond_residual, 0, 0.1)
    close(result.estimate, 0.05)
    assert result.left <= 0.05 <= result.right
    assert result.iterations > 0
    assert result.right-result.left <= 2e-10
    close(result.residual, bond_residual(result.estimate))
    rejects(ValueError, bisection, bond_residual, 0.2, 0.3)
    rejects(ValueError, bisection, bond_residual, 0, 0.1, tolerance=0)
    rejects(RuntimeError, bisection, lambda x: x*x-2, 1, 2,
            tolerance=1e-20, max_iterations=1)
    rejects(ValueError, bond_residual, -1)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 7.9 capstone reference checks (A1-A8)")

if __name__ == "__main__":
    run()
