"""Reference checks for the constrained example; runtime validation pending."""
import math
import unittest
from section_21_06 import solve, diagnostics, objective

class OptimizationChecks(unittest.TestCase):
    def test_interior(self):
        w = solve(.7, .2)["weights"]
        self.assertAlmostEqual(w[0], .75); self.assertAlmostEqual(w[1], .25)
    def test_objective(self): self.assertAlmostEqual(solve(.7, .2)["objective"], .005)
    def test_upper_boundary(self): self.assertEqual(solve(2, 0)["weights"], (1, 0))
    def test_lower_boundary(self): self.assertEqual(solve(0, 2)["weights"], (0, 1))
    def test_target_feasible(self): self.assertAlmostEqual(solve(.4, .6)["objective"], 0)
    def test_feasible(self): self.assertTrue(diagnostics(.5, .5)["feasible"])
    def test_equality_violation(self): self.assertFalse(diagnostics(.4, .5)["feasible"])
    def test_long_only_violation(self): self.assertAlmostEqual(diagnostics(1.2, -.2)["long_only_violation"], .2)
    def test_nonoptimal(self): self.assertGreater(objective(.5, .5, .7, .2), solve(.7, .2)["objective"])
    def test_negative_tolerance(self):
        with self.assertRaises(ValueError): diagnostics(.5, .5, -1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): solve(math.nan, .2)
    def test_boolean(self):
        with self.assertRaises(TypeError): solve(True, .2)
    def test_overflow(self):
        with self.assertRaises(OverflowError): objective(0, 1, 1e308, 0)

if __name__ == "__main__": unittest.main()
