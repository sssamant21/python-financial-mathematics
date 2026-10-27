"""Independent cash-flow reference checks; runtime validation pending."""
import math
import unittest
from section_21_03 import discount_factor, present_value, to_continuous, to_effective

class CashFlowChecks(unittest.TestCase):
    def test_zero_rate(self): self.assertEqual(present_value([(100, 1), (200, 2)], 0, "continuous"), 300)
    def test_zero_time(self): self.assertEqual(present_value([(-25, 0)], .1, "continuous"), -25)
    def test_half(self): self.assertAlmostEqual(present_value([(100, 1)], math.log(2), "continuous"), 50)
    def test_effective(self): self.assertAlmostEqual(present_value([(125, 1)], .25, "effective_annual"), 100)
    def test_equivalent_factor(self): self.assertAlmostEqual(discount_factor(to_continuous(.25), 2, "continuous"), 1/1.25**2)
    def test_conversion_known(self): self.assertAlmostEqual(to_effective(math.log(2)), 1)
    def test_empty(self): self.assertEqual(present_value([], .05, "continuous"), 0)
    def test_rate_boundary(self):
        with self.assertRaises(ValueError): discount_factor(-1, 1, "effective_annual")
    def test_negative_time(self):
        with self.assertRaises(ValueError): discount_factor(.05, -1, "continuous")
    def test_nonfinite(self):
        with self.assertRaises(ValueError): present_value([(math.nan, 1)], 0, "continuous")
    def test_boolean(self):
        with self.assertRaises(TypeError): discount_factor(True, 1, "continuous")
    def test_unknown_convention(self):
        with self.assertRaises(ValueError): present_value([], 0, "unknown")
    def test_split(self):
        self.assertTrue(math.isclose(present_value([(100, 2)], .05, "continuous"), present_value([(40, 2), (60, 2)], .05, "continuous"), rel_tol=1e-12, abs_tol=1e-9))
    def test_overflow(self):
        with self.assertRaises(OverflowError): discount_factor(-1000, 1, "continuous")

if __name__ == "__main__": unittest.main()
