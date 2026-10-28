"""Regression cases for Chapter 11 projection coefficient scaling."""
import math
import unittest
from section_11_06 import Vector, projection

class ProjectionCoefficientRange(unittest.TestCase):
    def test_large_direction_coefficient(self):
        result=projection(Vector(('A','B'),(1,1),'USD'),
                          Vector(('A','B'),(1.5e308,1.5e308),'dimensionless'))
        expected=1/1.5e308
        self.assertNotEqual(result['coefficient'],0)
        self.assertTrue(math.isclose(result['coefficient'],expected,rel_tol=1e-14,abs_tol=0))
        for component in result['projection'].values:
            self.assertTrue(math.isclose(component,1,rel_tol=1e-14))
    def test_direction_sign_reversal(self):
        result=projection(Vector(('A','B'),(1,1),'USD'),
                          Vector(('A','B'),(-1.5e308,-1.5e308),'dimensionless'))
        self.assertLess(result['coefficient'],0)
        for component in result['projection'].values:
            self.assertTrue(math.isclose(component,1,rel_tol=1e-14))
    def test_zero_direction(self):
        with self.assertRaises(ValueError):
            projection(Vector(('A','B'),(1,1),'USD'),Vector(('A','B'),(0,0),'dimensionless'))

if __name__ == '__main__': unittest.main()
