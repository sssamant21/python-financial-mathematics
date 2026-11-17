import math
import unittest
from key_rate import (present_value, key_rate_pv01, parallel_pv01,
                      TENORS, ZERO_RATES, CASHFLOWS)


class KeyRateTests(unittest.TestCase):
    def test_zero_coupon_closed_form(self):
        self.assertAlmostEqual(present_value((2,), (0.03,), (100,)),
                               100 * math.exp(-0.06))

    def test_zero_coupon_bucket_analytic(self):
        bump = 0.0001
        expected = 100 * math.exp(-0.06) * math.sinh(2 * bump)
        self.assertAlmostEqual(key_rate_pv01((2,), (0.03,), (100,))[0], expected)

    def test_bucket_parallel_identity(self):
        buckets = key_rate_pv01(TENORS, ZERO_RATES, CASHFLOWS)
        self.assertAlmostEqual(sum(buckets),
                               parallel_pv01(TENORS, ZERO_RATES, CASHFLOWS),
                               places=10)

    def test_positive_cashflows_positive_sensitivity(self):
        self.assertTrue(all(v > 0 for v in
                            key_rate_pv01(TENORS, ZERO_RATES, CASHFLOWS)))

    def test_negative_cashflow_allowed(self):
        self.assertLess(key_rate_pv01((1,), (0.02,), (-100,))[0], 0)

    def test_invalid_tenors(self):
        with self.assertRaises(ValueError):
            present_value((1, 1), (0.02, 0.03), (1, 1))

    def test_invalid_nonfinite(self):
        with self.assertRaises(ValueError):
            present_value((1,), (float("nan"),), (100,))

    def test_invalid_bump(self):
        with self.assertRaises(ValueError):
            key_rate_pv01((1,), (0.02,), (100,), 0)

    def test_unchanged_inputs(self):
        rates = list(ZERO_RATES)
        key_rate_pv01(TENORS, rates, CASHFLOWS)
        self.assertEqual(rates, list(ZERO_RATES))


if __name__ == "__main__":
    unittest.main()
