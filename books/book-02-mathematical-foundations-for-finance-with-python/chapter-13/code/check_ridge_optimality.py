"""Independent exact-objective references for the fixed Section 13.8 model."""
from fractions import Fraction as F
import math
from section_13_08 import solve_redundant_hedges

def objective(x, y, lam):
    # A has identical columns (1,2), target is (3,6).
    rate = F(3) - x - y
    credit = F(6) - 2*x - 2*y
    return (rate*rate + credit*credit + lam*(x*x+y*y))/2

def close(actual, expected):
    assert math.isclose(actual, float(expected), rel_tol=2e-12, abs_tol=2e-14)

def run():
    limits = {"RATE": 0.4, "CREDIT": 1.1}
    for lam in (F(1,2), F(2), F(20), F(1,2**20)):
        # Solve the independent 2x2 normal equations by determinants:
        # (5+lambda)x+5y=15, 5x+(5+lambda)y=15.
        diagonal = 5 + lam
        determinant = diagonal*diagonal - 25
        optimum = (15*diagonal - 75)/determinant
        result = solve_redundant_hedges(float(lam), limits)
        for x in result["positions"].values():
            close(x, optimum)
        rate, credit = 3-2*optimum, 6-4*optimum
        data = (rate*rate+credit*credit)/2
        penalty = lam*optimum*optimum
        close(result["data_objective"], data)
        close(result["penalty_objective"], penalty)
        close(result["total_objective"], objective(optimum,optimum,lam))
        close(result["residual_target_minus_achieved"]["RATE"], rate)
        close(result["residual_target_minus_achieved"]["CREDIT"], credit)
        for dx, dy in ((F(1),F(0)), (F(1),F(-1)), (F(-1,4),F(1,2))):
            excess = objective(optimum+dx,optimum+dy,lam)-objective(optimum,optimum,lam)
            # Exact positive quadratic excess independently establishes these comparisons.
            assert excess == F(5,2)*(dx+dy)**2 + lam*(dx*dx+dy*dy)/2
            assert excess > 0
            assert result["total_objective"] < float(objective(optimum+dx,optimum+dy,lam))
    # Positive-strength sequence tends to the minimum-norm exact hedge (1.5,1.5).
    previous_error = math.inf
    for exponent in (0, 4, 8, 12, 16, 20):
        lam = F(1, 2**exponent)
        result = solve_redundant_hedges(float(lam), limits)
        error = 1.5 - result["positions"]["BOND_A"]
        assert 0 < error < previous_error
        close(error, F(3,2)*lam/(10+lam))
        previous_error = error
    try:
        solve_redundant_hedges(0, limits)
    except ValueError:
        pass
    else:
        raise AssertionError("zero strength is outside the helper contract")
    print("PASS: Section 13.8 exact objectives and selected positive-strength limit")

if __name__ == "__main__":
    run()
