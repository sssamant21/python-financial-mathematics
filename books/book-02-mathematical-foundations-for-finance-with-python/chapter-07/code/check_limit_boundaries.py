"""Regression checks for Chapter 7 small-change and payment boundaries."""
import math
import unittest
from section_7_06 import power_quotient
from section_7_07 import bond_yield_residual

class LimitBoundaries(unittest.TestCase):
    def test_subnormal_power_limit(self):
        for h in (5e-324,-5e-324):
            for exponent in (.5,-.5,0,1):
                with self.subTest(h=h,exponent=exponent):
                    self.assertTrue(math.isclose(power_quotient(h,exponent),exponent,rel_tol=1e-14,abs_tol=0))
    def test_polynomial_known_value(self):
        self.assertTrue(math.isclose(power_quotient(.1,2),2.1,rel_tol=1e-14))
    def test_empty_iterator_rejected(self):
        with self.assertRaises(ValueError): bond_yield_residual(.05,iter([]),100)
    def test_payment_iterator_known_value(self):
        self.assertAlmostEqual(bond_yield_residual(0,iter([50,1050]),1000),100)

if __name__ == '__main__': unittest.main()
