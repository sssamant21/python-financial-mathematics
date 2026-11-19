"""Independent finite-shock checks for the multi-tenor bucket approximation.

All curves and quotes are synthetic. Standard-library unittest only.
"""
import unittest
from multi_tenor_cs01 import bucket_cs01, calibrate, legs


def independent_pv(tenors, quotes, maturity=5, coupon_bp=100,
                   notional=1_000_000, recovery=.4, rate=.02, frequency=4):
    """Rebootstrap a complete curve without calling bucket_cs01."""
    hazard = calibrate(tenors, quotes, recovery, rate, frequency)
    annuity, protection = legs(maturity, tenors, hazard, recovery, rate, frequency)
    return notional * (protection - coupon_bp / 10000 * annuity)


class ParallelReconciliationTests(unittest.TestCase):
    def test_parallel_central_derivative_matches_bucket_sum(self):
        tenors = (1, 3, 5)
        quotes = (60, 100, 140)
        bump = .1
        result = bucket_cs01(tenors, quotes, bump_bp=bump)
        plus = independent_pv(tenors, tuple(q + bump for q in quotes))
        minus = independent_pv(tenors, tuple(q - bump for q in quotes))
        parallel_derivative = (plus - minus) / (2 * bump)
        # Central differences differ by O(bump**2) in a nonlinear model.
        self.assertAlmostEqual(result["parallel_sum"], parallel_derivative, delta=.1)

    def test_bucket_sum_is_not_claimed_as_exact_large_shock_pnl(self):
        tenors = (1, 3, 5)
        quotes = (60, 100, 140)
        result = bucket_cs01(tenors, quotes, bump_bp=.1)
        base = independent_pv(tenors, quotes)
        shock = 5.
        shifted = independent_pv(tenors, tuple(q + shock for q in quotes))
        predicted = shock * result["parallel_sum"]
        # First-order approximation should be reasonably close, not identical.
        self.assertLess(abs((shifted - base) - predicted), max(1., .05 * abs(shifted - base)))

    def test_parallel_derivative_scales_with_notional(self):
        tenors, quotes = (1, 3, 5), (60, 100, 140)
        a = bucket_cs01(tenors, quotes, notional=100_000, bump_bp=.1)
        b = bucket_cs01(tenors, quotes, notional=1_000_000, bump_bp=.1)
        self.assertAlmostEqual(b["parallel_sum"], 10 * a["parallel_sum"], delta=1e-5)

    def test_negative_parallel_shock_rejected_if_curve_infeasible(self):
        with self.assertRaises(ValueError):
            calibrate((1, 3), (1000, 0))


if __name__ == "__main__":
    unittest.main()
