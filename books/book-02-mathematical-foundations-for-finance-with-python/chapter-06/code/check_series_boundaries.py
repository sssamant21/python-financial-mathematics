"""Chapter 6 geometric-ratio and verification-control regressions."""
import math
import unittest
from section_6_02 import geometric_sum
from section_6_09 import verify

class SeriesBoundaries(unittest.TestCase):
    def test_tiny_positive_ratio(self):
        self.assertEqual(geometric_sum(1e-100,3),1)
    def test_ratio_near_one(self):
        q=math.nextafter(1,math.inf)
        self.assertTrue(math.isclose(geometric_sum(q,3),math.fsum((1,q,q*q)),rel_tol=1e-14))
    def test_known_geometric_value(self): self.assertAlmostEqual(geometric_sum(.5,4),1.875)
    def test_invalid_tolerances(self):
        for tol in (math.inf,math.nan,-1):
            with self.subTest(tol=tol),self.assertRaises(ValueError):
                verify(100,0,.05,3,rel_tol=tol)
            with self.subTest(abs_tol=tol),self.assertRaises(ValueError):
                verify(100,0,.05,3,abs_tol=tol)
    def test_boolean_tolerance(self):
        with self.assertRaises(TypeError): verify(100,0,.05,3,rel_tol=True)
    def test_known_zero_rate_values(self):
        result=verify(100,0,0,3)
        self.assertEqual(result,{'pv':300,'fv':300})

if __name__ == '__main__': unittest.main()
