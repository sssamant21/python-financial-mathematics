"""Independent FRA discount-factor sensitivities; synthetic educational inputs."""
import math
import unittest
from decimal import Decimal, localcontext

from fra import fra_value


class CurveSensitivityTests(unittest.TestCase):
    def test_decimal_pv_reference_grid(self):
        cases = [
            ("1000000", "0.04", "0.98", "0.96", "0.5"),
            ("500000", "-0.01", "0.99", "1.01", "0.25"),
            ("1200000", "0.0", "1.0", "1.0", "1.0"),
            ("250000", "0.07", "0.92", "0.87", "0.75"),
        ]
        with localcontext() as ctx:
            ctx.prec = 60
            for n, k, d1, d2, a in cases:
                with self.subTest(case=(n, k, d1, d2, a)):
                    expected = Decimal(n) * (Decimal(d1) - Decimal(d2) * (1 + Decimal(k) * Decimal(a)))
                    got = fra_value(*map(float, (n, k, d1, d2, a)))["pv_t0"]
                    self.assertAlmostEqual(got, float(expected), delta=1e-7)

    def test_discount_factor_derivatives(self):
        n, k, d1, d2, a = 1_000_000.0, 0.04, 0.98, 0.96, 0.5
        h = 1e-5
        def pv(start, end):
            return fra_value(n, k, start, end, a)["pv_t0"]
        start_slope = (pv(d1 + h, d2) - pv(d1 - h, d2)) / (2 * h)
        end_slope = (pv(d1, d2 + h) - pv(d1, d2 - h)) / (2 * h)
        self.assertAlmostEqual(start_slope, n, delta=0.01)
        self.assertAlmostEqual(end_slope, -n * (1 + k * a), delta=0.01)

    def test_strike_derivative_and_payer_sign(self):
        n, k, d1, d2, a = 800_000.0, 0.035, 0.99, 0.97, 0.25
        h = 1e-5
        def pv(strike, receive=True):
            return fra_value(n, strike, d1, d2, a, receive_float=receive)["pv_t0"]
        slope = (pv(k + h) - pv(k - h)) / (2 * h)
        self.assertAlmostEqual(slope, -n * a * d2, delta=0.01)
        self.assertAlmostEqual(pv(k, False), -pv(k), delta=1e-8)

    def test_start_settlement_matches_discounted_end_cashflow(self):
        n, k, d1, d2, a = 1_000_000.0, 0.04, 0.98, 0.96, 0.5
        result = fra_value(n, k, d1, d2, a)
        # End-of-period equivalent cashflow is N*a*(F-K), discounted by D(t2).
        end_pv = n * a * (result["forward"] - k) * d2
        self.assertAlmostEqual(result["pv_t0"], end_pv, delta=1e-8)
        self.assertAlmostEqual(result["settlement_t1"] * d1, end_pv, delta=1e-8)

    def test_fair_strike_under_negative_forward(self):
        d1, d2, a = 0.98, 1.01, 0.5
        fair = (d1 / d2 - 1) / a
        result = fra_value(1_000_000, fair, d1, d2, a)
        self.assertLess(fair, 0)
        self.assertTrue(math.isfinite(result["pv_t0"]))
        self.assertAlmostEqual(result["pv_t0"], 0.0, delta=1e-8)


if __name__ == "__main__":
    unittest.main()
