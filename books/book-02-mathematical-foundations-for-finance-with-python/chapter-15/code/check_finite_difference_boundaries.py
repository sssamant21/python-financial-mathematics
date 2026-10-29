"""Regression checks for Chapter 15 numerical differentiation boundaries."""
import math
import unittest
from section_15_02 import centered_rate_difference, future_value, present_value
from section_15_05 import centered_financial_column, financial_jacobian
from section_15_09 import centered_jacobian_column, jacobian

class DifferenceBoundaries(unittest.TestCase):
    def test_scalar_rate_unrepresentable_step(self):
        with self.assertRaises(ValueError):
            centered_rate_difference(future_value,1000,.05,2,1e-30)
    def test_scalar_rate_denominator_overflow(self):
        with self.assertRaises(OverflowError):
            centered_rate_difference(lambda amount,rate,years: rate,1,0,0,1e308)
    def test_scalar_rate_perturbation_overflow(self):
        with self.assertRaises(ValueError):
            centered_rate_difference(lambda amount,rate,years: rate,1,1e308,0,1e308)
    def test_scalar_linear_rate_oracle(self):
        self.assertEqual(centered_rate_difference(lambda amount,rate,years: 3*rate+2,1,.25,0,.125),3)
    def test_scalar_financial_rate_derivatives(self):
        for fn,expected in ((future_value,2000*math.exp(.1)),(present_value,-2000*math.exp(-.1))):
            with self.subTest(function=fn.__name__):
                self.assertTrue(math.isclose(centered_rate_difference(fn,1000,.05,2),expected,rel_tol=1e-8,abs_tol=1e-8))
    def test_tiny_rate_steps_rejected(self):
        with self.assertRaises(ValueError): centered_financial_column(.05,2,0,1e-30)
        with self.assertRaises(ValueError): centered_jacobian_column((1000,.05,2),1,1e-30)
    def test_centered_time_leaves_domain(self):
        with self.assertRaises(ValueError): centered_financial_column(.05,0,1,.01)
        with self.assertRaises(ValueError): centered_jacobian_column((1000,.05,0),2,.01)
    def test_normal_rate_column_matches_analytic(self):
        for a,b in zip(centered_financial_column(.05,2,0,1e-5), (row[0] for row in financial_jacobian(.05,2))):
            self.assertTrue(math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-8))
        for a,b in zip(centered_jacobian_column((1000,.05,2),1,1e-5), (row[1] for row in jacobian(1000,.05,2))):
            self.assertTrue(math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-8))
    def test_denominator_overflow(self):
        with self.assertRaises(OverflowError): centered_financial_column(0,0,0,1e308)
        with self.assertRaises(OverflowError): centered_jacobian_column((1000,0,0),1,1e308)

if __name__ == '__main__': unittest.main()
