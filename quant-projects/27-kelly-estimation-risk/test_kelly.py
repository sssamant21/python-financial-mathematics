"""Deterministic synthetic tests for Project 27."""
import math
import unittest
from kelly import optimal_fraction, expected_log_growth, stress_grid

class KellyTests(unittest.TestCase):
    def test_fair_game(self):
        self.assertEqual(optimal_fraction(.5, 1, 1), 0)
    def test_known_value(self):
        self.assertAlmostEqual(optimal_fraction(.6, 1, 1), .2)
    def test_negative_edge(self):
        self.assertEqual(optimal_fraction(.4, 1, 1), 0)
    def test_cap(self):
        self.assertEqual(optimal_fraction(.9, 1, 1, .25), .25)
    def test_asymmetric(self):
        self.assertAlmostEqual(optimal_fraction(.6, 2, 1), .4)
    def test_growth_at_optimum(self):
        self.assertGreater(expected_log_growth(.2, .6, 1, 1), expected_log_growth(0, .6, 1, 1))
    def test_ruin(self):
        self.assertEqual(expected_log_growth(1, .6, 1, 1), -math.inf)
    def test_stress(self):
        f, rows = stress_grid(.6, 1, 1, (-.1, 0, .1))
        self.assertAlmostEqual(f, .2)
        self.assertEqual(len(rows), 3)
        self.assertLess(rows[0][1], rows[1][1])
    def test_invalid_probability(self):
        with self.assertRaises(ValueError): optimal_fraction(1, 1, 1)
    def test_bool_rejected(self):
        with self.assertRaises(ValueError): optimal_fraction(True, 1, 1)
    def test_bad_stress(self):
        with self.assertRaises(ValueError): stress_grid(.6, 1, 1, (-.7,))
    def test_bad_fraction(self):
        with self.assertRaises(ValueError): expected_log_growth(float("nan"), .6, 1, 1)

if __name__ == "__main__":
    unittest.main()
