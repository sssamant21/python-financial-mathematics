"""Regression checks for Chapter 14 decomposition boundaries."""
import math
import unittest
from section_14_05 import solve_2x2
from section_14_08 import frobenius_error

class DecompositionBoundaries(unittest.TestCase):
    def test_frobenius_large_representable(self):
        self.assertEqual(frobenius_error([[1e200]], [[0]]), 1e200)
    def test_frobenius_small_representable(self):
        self.assertEqual(frobenius_error([[1e-200]], [[0]]), 1e-200)
    def test_frobenius_known(self):
        self.assertEqual(frobenius_error([[3,4]], [[0,0]]), 5)
    def test_unrepresentable_error(self):
        with self.assertRaises(ValueError): frobenius_error([[1e308]], [[-1e308]])
    def test_matrix_iterator(self):
        result=solve_2x2((row for row in ((4,2),(2,3))), (6,5))
        for actual in result['solution']: self.assertTrue(math.isclose(actual,1,abs_tol=1e-12))
        self.assertLess(result['solve_residual_norm'],1e-12)
    def test_wrong_matrix_shape(self):
        with self.assertRaises(ValueError): solve_2x2(iter([(1,2)]),(1,2))

if __name__ == '__main__': unittest.main()
