"""Boundary and unit-scaling regression checks for the small-grid feasibility screen.

These fixtures are synthetic. They do not certify numerical conditioning.
"""
import unittest
from joint_feasibility import joint_feasible


class BoundaryScalingTests(unittest.TestCase):
    def test_exact_convex_boundary(self):
        strikes = [90, 100, 110, 120]
        calls = [20, 12, 6, 2]  # slopes -0.8, -0.6, -0.4
        self.assertTrue(joint_feasible(strikes, calls, calls)["joint_feasible"])

    def test_strict_convexity_violation(self):
        strikes = [90, 100, 110]
        calls = [20, 10, 1]  # convex; control case
        self.assertTrue(joint_feasible(strikes, calls, calls)["joint_feasible"])
        bad = [20, 15, 1]  # slopes -0.5, -1.4
        self.assertFalse(joint_feasible(strikes, bad, bad)["joint_feasible"])

    def test_price_and_strike_unit_scaling(self):
        strikes = [90, 100, 110, 120]
        feasible = [20, 12, 6, 2]
        infeasible = [20, 15, 1, 0]
        for prices, expected in ((feasible, True), (infeasible, False)):
            for factor in (0.1, 1.0, 100.0):
                with self.subTest(prices=prices, factor=factor):
                    result = joint_feasible(
                        [factor * k for k in strikes],
                        [factor * p for p in prices],
                        [factor * p for p in prices],
                    )
                    self.assertEqual(result["joint_feasible"], expected)

    def test_small_material_violation(self):
        strikes = [90, 100, 110]
        bad = [20.0, 15.0, 9.999]
        self.assertFalse(joint_feasible(strikes, bad, bad)["joint_feasible"])

    def test_nonfinite_and_negative_tolerance_rejected(self):
        for tolerance in (-1e-10, float("nan"), float("inf"), True):
            with self.subTest(tolerance=tolerance):
                with self.assertRaises(ValueError):
                    joint_feasible([90, 100, 110], [20, 10, 5], [20, 10, 5], tolerance=tolerance)


if __name__ == "__main__":
    unittest.main()
