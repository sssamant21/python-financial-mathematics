"""Reference cases for section 20.4; runtime validation pending."""
import math
import unittest
from section_20_04 import present_value, annuity_pv

class BoundaryChecks(unittest.TestCase):
    def test_zero_horizon(self): self.assertEqual(present_value(100, .05, 0), 100)
    def test_zero_rate(self): self.assertEqual(annuity_pv(100, 0, 3), 300)
    def test_empty_annuity(self): self.assertEqual(annuity_pv(100, .05, 0), 0)
    def test_negative_rate(self): self.assertAlmostEqual(present_value(100, -.1, 2), 100 / .81)
    def test_one_period(self): self.assertAlmostEqual(annuity_pv(100, .25, 1), 80)
    def test_near_zero(self): self.assertTrue(math.isclose(annuity_pv(100, 1e-12, 3), 300, rel_tol=1e-10))
    def test_subnormal_rate_small_payment(self):
        self.assertTrue(math.isclose(annuity_pv(.1, 5e-324, 3), .3, rel_tol=1e-15))
    def test_bad_rate(self):
        for r in (-1, -2):
            with self.subTest(rate=r), self.assertRaises(ValueError): present_value(100, r, 2)
    def test_nonfinite(self):
        for x in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(x=x), self.assertRaises(ValueError): present_value(x, 0, 1)
    def test_wrong_types(self):
        for x in (True, "1", None):
            with self.subTest(x=x), self.assertRaises(TypeError): present_value(x, 0, 1)
    def test_periods(self):
        for n in (True, 1.5):
            with self.subTest(n=n), self.assertRaises(TypeError): annuity_pv(100, .1, n)
        with self.assertRaises(ValueError): annuity_pv(100, .1, -1)
    def test_signed_amount(self): self.assertAlmostEqual(present_value(-100, .25, 1), -80)
    def test_overflow(self):
        with self.assertRaises(OverflowError): present_value(100, -.99, 1000)

if __name__ == "__main__": unittest.main()
