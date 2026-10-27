"""Reference checks for sensitivity module; runtime validation pending."""
import math
import unittest
from section_21_04 import pv, derivatives, central_difference, approximations

class SensitivityChecks(unittest.TestCase):
    def test_pv_zero_rate(self): self.assertEqual(pv(100, 0, 2), 100)
    def test_derivatives(self): self.assertEqual(derivatives(100, 0, 2), (-200, 400))
    def test_zero_time(self): self.assertEqual(derivatives(100, .1, 0), (0, 0))
    def test_negative_amount(self): self.assertEqual(derivatives(-100, 0, 1), (100, -100))
    def test_known_value(self): self.assertAlmostEqual(pv(100, math.log(2), 1), 50)
    def test_basis_point(self): self.assertAlmostEqual(derivatives(100, 0, 1)[0] * .0001, -.01)
    def test_approximations(self):
        first, second = approximations(100, 0, 2, .01)
        self.assertAlmostEqual(first, 98)
        self.assertAlmostEqual(second, 98.02)
    def test_central(self): self.assertTrue(math.isclose(central_difference(100, 0, 2, 1e-5), -200, rel_tol=1e-8))
    def test_zero_step(self):
        with self.assertRaises(ValueError): central_difference(100, 0, 2, 0)
    def test_tiny_step(self):
        with self.assertRaises(ValueError): central_difference(100, 1, 2, 1e-30)
    def test_bad_time(self):
        with self.assertRaises(ValueError): pv(100, 0, -1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): pv(math.nan, 0, 1)
    def test_overflow(self):
        with self.assertRaises(OverflowError): pv(100, -1000, 1)

if __name__ == "__main__": unittest.main()
