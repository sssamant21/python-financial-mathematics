"""Chapter 21 exercise reference checks; runtime validation pending."""
import math
import unittest
from section_21_03 import present_value, to_continuous, to_effective
from section_21_04 import derivatives, approximations
from section_21_05 import solve_2x2
from section_21_06 import solve, diagnostics, objective
from section_21_07 import transition
from section_21_09 import build_report

class ExerciseChecks(unittest.TestCase):
    def test_continuous_pv(self): self.assertAlmostEqual(present_value([(100, 1)], math.log(2), "continuous"), 50)
    def test_effective_pv(self): self.assertAlmostEqual(present_value([(125, 1)], .25, "effective_annual"), 100)
    def test_conversion(self): self.assertAlmostEqual(to_effective(to_continuous(.25)), .25)
    def test_derivatives(self): self.assertEqual(derivatives(100, 0, 2), (-200, 400))
    def test_approximation(self):
        a, b = approximations(100, 0, 2, .01)
        self.assertAlmostEqual(a, 98); self.assertAlmostEqual(b, 98.02)
    def test_replication(self):
        x = solve_2x2([[1, 1], [1, 2]], [3, 5])["solution"]
        self.assertAlmostEqual(x[0], 1); self.assertAlmostEqual(x[1], 2)
    def test_singular(self):
        with self.assertRaises(ValueError): solve_2x2([[1, 1], [2, 2]], [2, 5])
    def test_allocation(self):
        r = solve(.7, .2)
        self.assertAlmostEqual(r["weights"][0], .75)
        self.assertAlmostEqual(r["objective"], .005)
    def test_feasible_not_optimal(self):
        self.assertTrue(diagnostics(.5, .5)["feasible"])
        self.assertGreater(objective(.5, .5, .7, .2), solve(.7, .2)["objective"])
    def test_account(self): self.assertEqual(transition(1000, 0, 200, 3), 1600)
    def test_unconstrained(self): self.assertEqual(transition(100, 0, -60, 2), -20)
    def test_pending_report(self):
        self.assertEqual(build_report()["approval"], "pending")

if __name__ == "__main__": unittest.main()
