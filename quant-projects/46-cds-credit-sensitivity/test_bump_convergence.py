"""Synthetic quote-bump convergence diagnostics for simplified multi-tenor CDS CS01.

Educational finite-difference checks, not ISDA or market validation.
"""
import unittest

from multi_tenor_cs01 import bucket_cs01, calibrate, legs


TENORS = (1, 3, 5)
QUOTES = (60, 100, 140)


def repriced(quotes):
    """Independently recalibrate all tenors and reprice a fixed coupon."""
    hazards = calibrate(TENORS, quotes)
    annuity, protection = legs(5, TENORS, hazards)
    return 1_000_000 * (protection - .01 * annuity)


class BumpConvergenceTests(unittest.TestCase):
    def test_bucket_derivatives_stabilize_as_bump_shrinks(self):
        # Compare central derivatives against a small-bump reference.
        reference = bucket_cs01(TENORS, QUOTES, bump_bp=.01)
        medium = bucket_cs01(TENORS, QUOTES, bump_bp=.1)
        large = bucket_cs01(TENORS, QUOTES, bump_bp=1.)
        for i in range(3):
            target = reference["buckets"][i]["cs01"]
            medium_error = abs(medium["buckets"][i]["cs01"] - target)
            large_error = abs(large["buckets"][i]["cs01"] - target)
            self.assertLessEqual(medium_error, large_error + .001)
            self.assertLess(medium_error, max(.1, .005 * abs(target)))

    def test_parallel_derivative_stabilizes_with_bump(self):
        reference = bucket_cs01(TENORS, QUOTES, bump_bp=.01)["parallel_sum"]
        medium = bucket_cs01(TENORS, QUOTES, bump_bp=.1)["parallel_sum"]
        large = bucket_cs01(TENORS, QUOTES, bump_bp=1.)["parallel_sum"]
        self.assertLessEqual(abs(medium - reference), abs(large - reference) + .001)
        self.assertLess(abs(medium - reference), max(.1, .005 * abs(reference)))

    def test_parallel_quote_repricing_matches_bucket_sum_at_small_bump(self):
        bump = .1
        estimate = bucket_cs01(TENORS, QUOTES, bump_bp=bump)["parallel_sum"]
        plus = repriced(tuple(q + bump for q in QUOTES))
        minus = repriced(tuple(q - bump for q in QUOTES))
        independent = (plus - minus) / (2 * bump)
        self.assertAlmostEqual(estimate, independent, delta=.1)

    def test_zero_quote_uses_forward_difference(self):
        result = bucket_cs01((1,), (0,), maturity=1, coupon_bp=0, bump_bp=.01)
        self.assertEqual(result["buckets"][0]["method"], "forward")
        self.assertGreater(result["buckets"][0]["cs01"], 0)

    def test_invalid_tiny_bump_rejected(self):
        with self.assertRaises(ValueError):
            bucket_cs01(TENORS, QUOTES, bump_bp=.0001)


if __name__ == "__main__":
    unittest.main()
