import unittest
from math import exp, log1p
from convention_check import nominal_to_continuous, periodic_price, compare_conventions
FLOWS = [(0.5, 2.5), (1.0, 102.5)]
class ConventionTests(unittest.TestCase):
    def test_conversion(self):
        self.assertAlmostEqual(nominal_to_continuous(.06, 2), 2 * log1p(.03))
    def test_zero_yield(self):
        self.assertAlmostEqual(periodic_price(FLOWS, 0), 105)
    def test_single_payment(self):
        self.assertAlmostEqual(periodic_price([(2, 100)], .04, 2), 100 / 1.02**4)
    def test_equivalent_yield(self):
        for m in (1, 2, 4, 12):
            with self.subTest(m=m):
                self.assertAlmostEqual(compare_conventions(FLOWS, .05, m)["difference"], 0, places=11)
    def test_nominal_not_same_numeric_continuous(self):
        self.assertNotAlmostEqual(periodic_price(FLOWS, .05, 2), sum(c * exp(-.05*t) for t,c in FLOWS), places=5)
    def test_negative_valid_yield(self):
        self.assertAlmostEqual(compare_conventions(FLOWS, -.01, 2)["difference"], 0, places=11)
    def test_invalid_frequency(self):
        for m in (0, -1, 2.5, True, 366):
            with self.subTest(m=m), self.assertRaises(ValueError): nominal_to_continuous(.05, m)
    def test_invalid_rate(self):
        for rate in (float("nan"), float("inf"), True, -2.0):
            with self.subTest(rate=rate), self.assertRaises(ValueError): nominal_to_continuous(rate, 2)
    def test_invalid_flows(self):
        for flows in ([], [(0, 1)], [(1, -1)], [(2, 1), (1, 1)], [(1, float("nan"))], [(1, True)], [("bad", 2)]):
            with self.subTest(flows=flows), self.assertRaises(ValueError): periodic_price(flows, .05)
    def test_discount_exponent(self):
        with self.assertRaises(ValueError): periodic_price([(10000, 100)], 1.0)
if __name__ == "__main__": unittest.main()
