"""Deterministic tests of yield interpolation and accounting reconciliation."""
import math
import unittest
from interpolation import discount_factor, compare

C = {1.: .03, 2.: .035, 3.: .04, 5.: .045}

class InterpolationTests(unittest.TestCase):
    def test_node_agreement(self):
        for t, r in C.items():
            for method in ("linear_spot", "log_discount"):
                self.assertAlmostEqual(discount_factor(t, C, method), math.exp(-r*t))
    def test_log_discount_geometric_interpolation(self):
        expected = math.sqrt(math.exp(-.035*2) * math.exp(-.04*3))
        self.assertAlmostEqual(discount_factor(2.5, C, "log_discount"), expected)
    def test_spot_linear_benchmark(self):
        self.assertAlmostEqual(discount_factor(2.5, C), math.exp(-.0375*2.5))
    def test_discount_factors_positive(self):
        for method in ("linear_spot", "log_discount"):
            for t in (1., 1.5, 2., 2.5, 3., 4., 5.):
                self.assertGreater(discount_factor(t, C, method), 0.)
    def test_reconcile_both_methods(self):
        for row in compare(100., 3., .5, C).values():
            self.assertAlmostEqual(row["carry"] + row["roll_down"], row["pnl"])
    def test_exact_node_horizon_agreement(self):
        rows = compare(100., 3., 1., C)
        self.assertAlmostEqual(rows["linear_spot"]["pnl"], rows["log_discount"]["pnl"])
    def test_input_immutability(self):
        curve = C.copy()
        compare(100., 3., .5, curve)
        self.assertEqual(curve, C)
    def test_invalid_inputs(self):
        for t in (0., .5, 6., float("nan"), True):
            with self.assertRaises(ValueError):
                discount_factor(t, C)
        for method in ("cubic", "", None):
            with self.assertRaises(ValueError):
                discount_factor(2., C, method)
        for face, h in ((0., .5), (100., 0.), (100., 3.), (float("inf"), .5)):
            with self.assertRaises(ValueError):
                compare(face, 3., h, C)
    def test_invalid_curve_nodes(self):
        for bad in ({1.: .03}, {1.: float("nan"), 2.: .04}, {1.: .03, 2.: 1.2}):
            with self.assertRaises(ValueError):
                discount_factor(1.5, bad)

if __name__ == "__main__":
    unittest.main()
