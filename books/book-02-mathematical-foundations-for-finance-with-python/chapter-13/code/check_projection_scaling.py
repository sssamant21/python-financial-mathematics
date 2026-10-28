"""Regression checks for scale-independent line projection."""
import math
import unittest
from section_13_04 import FactorVector, project_line

def vector(values):
    return FactorVector(('X','Y'),values,'standardized_exposure')

class ProjectionScaling(unittest.TestCase):
    def test_known_projection_across_scales(self):
        for scale in (1.0, 1e200, 1e-200, -1e200):
            with self.subTest(scale=scale):
                result=project_line(vector((scale,2*scale)),vector((3,7)),vector((1,1)))
                self.assertTrue(math.isclose(result['projected']['X'],3.4,rel_tol=1e-14))
                self.assertTrue(math.isclose(result['projected']['Y'],6.8,rel_tol=1e-14))
                self.assertTrue(math.isclose(result['distance_l2'],math.sqrt(.2),rel_tol=1e-13))
                self.assertTrue(math.isclose(result['coefficient']*scale,3.4,rel_tol=1e-14))
    def test_zero_direction_rejected(self):
        with self.assertRaises(ValueError):
            project_line(vector((0,0)),vector((3,7)),vector((1,1)))

if __name__ == '__main__': unittest.main()
