"""Additional synthetic numerical boundary and coupon-frequency checks."""
import math
import unittest
from accrued_default import accrued_legs


class NumericalEdgeCases(unittest.TestCase):
    def test_exact_zero_combined_rate(self):
        h, r, t = 0.04, -0.04, 5
        x = accrued_legs(hazard=h, rate=r, years=t)
        self.assertAlmostEqual(x["protection_leg"], 1_000_000 * 0.6 * h * t, places=7)
        self.assertAlmostEqual(x["accrual_annuity_per_notional"], h * t / 8, places=12)
        self.assertTrue(math.isfinite(x["par_spread_bp"]))

    def test_near_zero_combined_rate_continuity(self):
        base = accrued_legs(hazard=0.04, rate=-0.04)
        for shift in (-1e-10, 1e-10, -1e-6, 1e-6):
            with self.subTest(shift=shift):
                actual = accrued_legs(hazard=0.04, rate=-0.04 + shift)
                self.assertTrue(math.isfinite(actual["par_spread"]))
                self.assertAlmostEqual(actual["par_spread"], base["par_spread"], delta=2e-7)

    def test_negative_discount_rate(self):
        x = accrued_legs(hazard=0.02, rate=-0.08)
        self.assertGreater(x["accrual_annuity_per_notional"], 0)
        self.assertGreater(x["protection_leg"], 0)
        self.assertAlmostEqual(
            x["par_spread"] * 1_000_000 * x["total_annuity_per_notional"],
            x["protection_leg"], delta=1e-7)

    def test_coupon_frequency_sensitivity(self):
        results = [
            accrued_legs(hazard=0.06, rate=0.02, payments_per_year=f)["par_spread"]
            for f in (1, 2, 4, 12)
        ]
        self.assertTrue(all(math.isfinite(x) and x > 0 for x in results))
        # Discrete scheduled coupons create a positive spread premium
        # relative to the continuous-premium limit h*(1-R).
        self.assertTrue(all(a > b for a, b in zip(results, results[1:])))
        self.assertGreater(results[-1], 0.06 * 0.6)

    def test_extreme_permitted_hazard_and_rate(self):
        x = accrued_legs(hazard=2, rate=1, years=30, payments_per_year=12)
        self.assertTrue(math.isfinite(x["par_spread"]))
        self.assertGreater(x["total_annuity_per_notional"], 0)


if __name__ == "__main__":
    unittest.main()
