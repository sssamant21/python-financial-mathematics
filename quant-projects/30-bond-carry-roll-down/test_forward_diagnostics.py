"""Deterministic synthetic forward and horizon checks."""
import math
import unittest
from forward_diagnostics import forward_rate, forward_grid, horizon_diagnostics

C = {1.: .03, 2.: .035, 3.: .04, 5.: .045}

class ForwardDiagnosticsTests(unittest.TestCase):
    def test_node_forward_benchmark(self):
        self.assertAlmostEqual(forward_rate(2., 3., C), .05)
    def test_node_forward_method_agreement(self):
        self.assertAlmostEqual(forward_rate(2., 3., C, "linear_spot"), .05)
    def test_discount_ratio_identity(self):
        from interpolation import discount_factor
        a, b = 2.25, 2.75
        for method in ("linear_spot", "log_discount"):
            f = forward_rate(a, b, C, method)
            self.assertAlmostEqual(math.exp(-f*(b-a)), discount_factor(b,C,method)/discount_factor(a,C,method))
    def test_piecewise_constant_log_discount_forward(self):
        self.assertAlmostEqual(forward_rate(2.1, 2.8, C), .05)
    def test_interpolation_method_difference(self):
        self.assertNotAlmostEqual(forward_rate(2.1, 2.8, C, "linear_spot"), .05)
    def test_grid(self):
        self.assertEqual(len(forward_grid(C)), 3)
    def test_horizon_node_agreement(self):
        self.assertAlmostEqual(horizon_diagnostics(100.,3.,[1.],C)[0]["difference"], 0.)
    def test_horizon_off_node_difference(self):
        self.assertGreater(abs(horizon_diagnostics(100.,3.,[.5],C)[0]["difference"]), 1e-8)
    def test_immutable(self):
        before = C.copy()
        forward_grid(C)
        horizon_diagnostics(100.,3.,[.5,1.],C)
        self.assertEqual(before,C)
    def test_bad_intervals(self):
        for a,b in ((0.,1.),(2.,2.),(3.,2.),(float("nan"),3.),(True,2.),(1.,6.)):
            with self.assertRaises(ValueError): forward_rate(a,b,C)
    def test_bad_horizons(self):
        for h in ([],[0.],[3.],[.5,.5],[float("nan")]):
            with self.assertRaises(ValueError): horizon_diagnostics(100.,3.,h,C)

if __name__ == "__main__":
    unittest.main()
