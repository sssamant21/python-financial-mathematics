"""Chapter 8 regressions for representable finite-difference controls."""
import math
import unittest
from section_8_06 import centered_second_difference
from section_8_08 import second_difference, centered_difference
from section_8_09 import compare_derivatives
from section_8_10 import centered_second

class DifferenceDenominators(unittest.TestCase):
    def test_squared_step_underflow(self):
        for fn in (centered_second_difference,second_difference,centered_second):
            with self.subTest(function=fn.__module__),self.assertRaises(ValueError):
                fn(lambda x:x*x,0,1e-200)
        with self.assertRaises(ValueError):
            compare_derivatives(lambda x:x*x,lambda x:2*x,0,1e-200,lambda x:2)
    def test_squared_step_overflow(self):
        for fn in (centered_second_difference,second_difference,centered_second):
            with self.subTest(function=fn.__module__),self.assertRaises(ValueError):
                fn(lambda x:1,0,1e200)
    def test_unchanged_perturbation(self):
        with self.assertRaises(ValueError): centered_second_difference(lambda x:x*x,1,1e-30)
    def test_normal_quadratic(self):
        for fn in (centered_second_difference,second_difference,centered_second):
            self.assertTrue(math.isclose(fn(lambda x:x*x,2,.1),2,rel_tol=1e-12))
    def test_first_derivative_denominator_overflow(self):
        with self.assertRaises(ValueError): centered_difference(lambda x:x/1e308,0,1e308)

if __name__ == '__main__': unittest.main()
