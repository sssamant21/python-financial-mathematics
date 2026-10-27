"""Independent reference cases for section 20.6; runtime validation pending."""
import math
import unittest
from section_20_06 import pv, portfolio, cases, close

class Checks(unittest.TestCase):
    def test_zero_rate(self): self.assertEqual(pv(100, 0, 2), 100)
    def test_known_value(self): self.assertAlmostEqual(pv(100, math.log(2), 1), 50)
    def test_zero_time(self): self.assertEqual(pv(-40, .2, 0), -40)
    def test_split(self):
        self.assertTrue(close(portfolio([(40, 2), (60, 2)], .05), pv(100, .05, 2)))
    def test_permutation(self):
        flows = [(100, 1), (-20, 2), (75, 3)]
        self.assertTrue(close(portfolio(flows, .04), portfolio(flows[::-1], .04)))
    def test_scaling(self):
        for amount, rate, years, factor in cases():
            with self.subTest(amount=amount, rate=rate, years=years, factor=factor):
                self.assertTrue(close(pv(factor*amount, rate, years), factor*pv(amount, rate, years)))
    def test_monotonic_positive(self): self.assertLess(pv(100, .1, 2), pv(100, .05, 2))
    def test_monotonic_negative(self): self.assertGreater(pv(-100, .1, 2), pv(-100, .05, 2))
    def test_composition(self):
        self.assertTrue(close(pv(1, .04, 5), pv(1, .04, 2)*pv(1, .04, 3)))
    def test_repeatable_cases(self): self.assertEqual(list(cases()), list(cases()))
    def test_invalid_time(self):
        with self.assertRaises(ValueError): pv(100, .05, -1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): pv(math.nan, .05, 1)

if __name__ == "__main__": unittest.main()
