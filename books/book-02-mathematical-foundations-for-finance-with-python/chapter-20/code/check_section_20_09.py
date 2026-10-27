"""Independent reference checks for project; runtime validation pending."""
import math
import unittest
from section_20_09 import value, pending_dossier

class ProjectChecks(unittest.TestCase):
    def test_zero_rate(self): self.assertEqual(value([(100, 1), (200, 2)], 0), 300)
    def test_known_value(self): self.assertAlmostEqual(value([(100, 1)], math.log(2)), 50)
    def test_time_zero(self): self.assertEqual(value([(75, 0)], .2), 75)
    def test_empty(self): self.assertEqual(value([], .05), 0)
    def test_signed(self): self.assertEqual(value([(100, 1), (-40, 2)], 0), 60)
    def test_negative_time(self):
        with self.assertRaises(ValueError): value([(100, -1)], .05)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): value([(math.nan, 1)], .05)
    def test_bool(self):
        with self.assertRaises(TypeError): value([(True, 1)], .05)
    def test_split(self):
        self.assertTrue(math.isclose(value([(100, 2)], .05), value([(40, 2), (60, 2)], .05), rel_tol=1e-12, abs_tol=1e-9))
    def test_permutation(self):
        flows = [(100, 1), (-40, 2), (75, 3)]
        self.assertTrue(math.isclose(value(flows, .04), value(flows[::-1], .04), rel_tol=1e-12, abs_tol=1e-9))
    def test_scaling(self):
        self.assertTrue(math.isclose(value([(-200, 1)], .05), -2*value([(100, 1)], .05), rel_tol=1e-12, abs_tol=1e-9))
    def test_pending(self):
        dossier = pending_dossier()
        self.assertEqual(dossier["execution"], "not run")
        self.assertEqual(dossier["approval"], "pending")

if __name__ == "__main__": unittest.main()
