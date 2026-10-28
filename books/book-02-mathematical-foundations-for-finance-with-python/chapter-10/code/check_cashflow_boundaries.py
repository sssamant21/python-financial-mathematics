"""Chapter 10 cash-flow range and repeatability regression checks."""
import math
import unittest
from section_10_05 import exponential_integral as integral05
from section_10_09 import exponential_integral as integral09, Curve, Stream, parallel_shift_derivative

class CashFlowBoundaries(unittest.TestCase):
    def test_subnormal_exponential_integral(self):
        for fn in (integral05,integral09):
            for exponent in (5e-324,-5e-324):
                with self.subTest(function=fn.__module__,exponent=exponent):
                    self.assertTrue(math.isclose(fn(.1,exponent,3),.3,rel_tol=1e-14))
    def test_payment_iterator_derivative(self):
        actual=parallel_shift_derivative(iter([]),iter([(1,100)]),Curve(0),1)
        self.assertTrue(math.isclose(actual,-100,rel_tol=1e-8))
    def test_stream_iterator_matches_sequence(self):
        streams=[Stream('constant',100)]
        expected=parallel_shift_derivative(streams,[],Curve(.05),1)
        actual=parallel_shift_derivative(iter(streams),iter([]),Curve(.05),1)
        self.assertEqual(actual,expected)
    def test_unrepresentable_bump(self):
        with self.assertRaises(ValueError):
            parallel_shift_derivative([],[(1,100)],Curve(.05),1,bump=1e-30)
    def test_denominator_overflow(self):
        with self.assertRaises(OverflowError):
            parallel_shift_derivative([],[],Curve(0),0,bump=1e308)

if __name__ == '__main__': unittest.main()
