"""Adversarial synthetic conditioning fixtures; independent exact Fraction oracle.

These intentionally probe small strike gaps and tiny convexity differences.
The floating-point solver may disagree: a failure is evidence to investigate,
not a reason to weaken the oracle or silently enlarge tolerances.
"""
import unittest

from joint_feasibility import joint_feasible
from test_interval_reference import reference_three_strikes


class NearZeroPivotTests(unittest.TestCase):
    def compare(self, strikes, prices, expected):
        self.assertIs(reference_three_strikes(strikes, prices, prices), expected)
        self.assertIs(
            joint_feasible(strikes, prices, prices, tolerance=0)["joint_feasible"],
            expected,
        )

    def test_tight_irregular_grid_feasible(self):
        # Slopes -0.5, -0.4; positive but small gap on the left.
        self.compare([100, 100.0001, 110], [20, 19.99995, 16.00001], True)

    def test_tight_irregular_grid_nonconvex(self):
        # Slopes -0.5, approximately -0.6: violates convexity.
        self.compare([100, 100.0001, 110], [20, 19.99995, 14.00001], False)

    def test_near_flat_feasible(self):
        # Flat calls are permitted; all slopes are exactly zero.
        self.compare([90, 100, 110], [5, 5, 5], True)

    def test_near_flat_nonmonotone(self):
        # Exact arithmetic detects the positive last secant.
        self.compare([90, 100, 110], [5, 5, 5.000001], False)


if __name__ == "__main__":
    unittest.main()
