"""Scale-aware tolerance regression tests (synthetic, no market data)."""
import unittest
from joint_feasibility import joint_feasible


class NormalizedToleranceTests(unittest.TestCase):
    def test_material_convexity_violation_across_units(self):
        # Slopes -0.5 then -0.5001: a genuine convexity violation.
        for factor in (1e-3, 1.0, 1e3):
            with self.subTest(factor=factor):
                k = [factor * x for x in (90, 100, 110)]
                c = [factor * x for x in (20, 15, 9.999)]
                self.assertFalse(joint_feasible(k, c, c)["joint_feasible"])

    def test_exact_convex_boundary_across_units(self):
        for factor in (1e-3, 1.0, 1e3):
            with self.subTest(factor=factor):
                k = [factor * x for x in (90, 100, 110, 120)]
                c = [factor * x for x in (20, 12, 6, 2)]
                self.assertTrue(joint_feasible(k, c, c)["joint_feasible"])

    def test_wide_intervals_remain_feasible(self):
        for factor in (1e-3, 1.0, 1e3):
            with self.subTest(factor=factor):
                k = [factor * x for x in (90, 100, 110)]
                b = [factor * x for x in (14, 9, 5)]
                a = [factor * x for x in (15, 10, 6)]
                self.assertTrue(joint_feasible(k, b, a)["joint_feasible"])


if __name__ == "__main__":
    unittest.main()
