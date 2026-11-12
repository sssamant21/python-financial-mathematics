"""Synthetic arithmetic tests and optional QuantLib integration (never silently pass)."""
import importlib.util
import math
import unittest
from external_pricing_check import manual_present_value, compare_quantlib

class ArithmeticTests(unittest.TestCase):
    def test_single_payment(self):
        self.assertAlmostEqual(manual_present_value([(365, 100.0)], None, 0.05),
                               100 * math.exp(-0.05), places=12)
    def test_two_payments(self):
        expected = 5 * math.exp(-0.05) + 105 * math.exp(-0.1)
        self.assertAlmostEqual(manual_present_value([(365, 5), (730, 105)], None, .05),
                               expected, places=12)
    def test_rejects_invalid(self):
        for flows, rate in [([], .05), ([(0, 100)], .05), ([(365, -1)], .05),
                            ([(365, float("nan"))], .05), ([(365, 100)], float("inf"))]:
            with self.subTest(flows=flows, rate=rate):
                with self.assertRaises(ValueError):
                    manual_present_value(flows, None, rate)

@unittest.skipUnless(importlib.util.find_spec("QuantLib") is not None,
                     "QuantLib not installed: external comparison UNVERIFIED")
class QuantLibIntegrationTests(unittest.TestCase):
    def test_fixed_coupon_npv(self):
        for coupon, rate in ((0.0, 0.0), (.05, .045), (.08, .12)):
            with self.subTest(coupon=coupon, rate=rate):
                result = compare_quantlib(coupon, rate)
                self.assertGreater(result["cashflow_count"], 0)
                self.assertLess(result["absolute_difference"], 1e-7)

if __name__ == "__main__":
    unittest.main()
