"""Regression checks for normalized two-by-two inverse calculations."""
import math
import unittest
import section_12_06 as s06
import section_12_07 as s07

class InverseScaling(unittest.TestCase):
    def test_scaled_identity(self):
        for scale in (1.0, 1e200, 1e-200):
            with self.subTest(scale=scale):
                a=s06.Matrix2(('A','B'),('X','Y'),((scale,0),(0,scale)),'standardized_sensitivity')
                inv=s06.inverse(a).rows
                self.assertTrue(math.isclose(inv[0][0],1/scale,rel_tol=1e-14))
                self.assertTrue(math.isclose(inv[1][1],1/scale,rel_tol=1e-14))
                self.assertEqual(inv[0][1],0)
                b=s07.Matrix2(('A','B'),('X','Y'),((scale,0),(0,scale)),'standardized_sensitivity')
                self.assertTrue(math.isclose(s07.condition_inf(b),1,rel_tol=1e-14))
    def test_scaled_nondiagonal_known_inverse(self):
        for scale in (1e200,1e-200):
            a=s06.Matrix2(('A','B'),('X','Y'),((2*scale,scale),(scale,scale)),'standardized_sensitivity')
            expected=((1,-1),(-1,2))
            for actual_row,want_row in zip(s06.inverse(a).rows,expected):
                for actual,want in zip(actual_row,want_row):
                    self.assertTrue(math.isclose(actual*scale,want,rel_tol=1e-14))
    def test_singular_still_rejected(self):
        a=s06.Matrix2(('A','B'),('X','Y'),((1,1),(1,1)),'standardized_sensitivity')
        with self.assertRaises(ValueError): s06.inverse(a)

if __name__ == '__main__': unittest.main()
