"""Reference checks for Chapter 20 exercises; runtime validation pending."""
import math
import unittest
from section_20_09 import value

class ExerciseChecks(unittest.TestCase):
    def test_zero_rate(self): self.assertEqual(value([(100, 2)], 0), 100)
    def test_zero_time(self): self.assertEqual(value([(75, 0)], .1), 75)
    def test_half(self): self.assertAlmostEqual(value([(100, 1)], math.log(2)), 50)
    def test_empty(self): self.assertEqual(value([], 0), 0)
    def test_negative_time(self):
        with self.assertRaises(ValueError): value([(1, -1)], 0)
    def test_nan(self):
        with self.assertRaises(ValueError): value([(math.nan, 1)], 0)
    def test_split(self):
        self.assertTrue(math.isclose(value([(100, 2)], .05), value([(40, 2), (60, 2)], .05), rel_tol=1e-12, abs_tol=1e-9))
    def test_permutation(self):
        flows = [(100, 1), (-40, 2)]
        self.assertTrue(math.isclose(value(flows, .05), value(flows[::-1], .05), rel_tol=1e-12, abs_tol=1e-9))
    def test_scaling(self):
        self.assertTrue(math.isclose(value([(-200, 1)], .05), -2 * value([(100, 1)], .05), rel_tol=1e-12, abs_tol=1e-9))
    def test_positive_monotonic(self): self.assertLess(value([(100, 1)], .1), value([(100, 1)], .05))
    def test_negative_monotonic(self): self.assertGreater(value([(-100, 1)], .1), value([(-100, 1)], .05))
    def test_known_effective_discount(self): self.assertEqual(100 / 1.25, 80)

if __name__ == "__main__": unittest.main()
