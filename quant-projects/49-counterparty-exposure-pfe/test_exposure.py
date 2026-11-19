"""Deterministic, synthetic-only Project 49 regression tests."""
import math
import unittest
from exposure import simulate, quantile

class ExposureTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(simulate(paths=200, seed=7), simulate(paths=200, seed=7))

    def test_nonnegative_and_ordered(self):
        for row in simulate(paths=500, seed=3):
            self.assertGreaterEqual(row["epe"], 0)
            self.assertGreaterEqual(row["pfe95"], 0)
            self.assertGreaterEqual(row["incremental_cva"], 0)

    def test_zero_volatility(self):
        for row in simulate(volatility=0, paths=100):
            self.assertEqual(row["epe"], 0)
            self.assertEqual(row["pfe95"], 0)
            self.assertEqual(row["incremental_cva"], 0)

    def test_zero_hazard_or_lgd(self):
        for key in ("hazard", "lgd"):
            for row in simulate(paths=100, **{key: 0}):
                self.assertEqual(row["incremental_cva"], 0)

    def test_threshold_reduces_exposure_and_cva(self):
        a = simulate(paths=300, seed=12, threshold=0)
        b = simulate(paths=300, seed=12, threshold=100000)
        for x, y in zip(a, b):
            self.assertLessEqual(y["epe"], x["epe"])
            self.assertLessEqual(y["pfe95"], x["pfe95"])
            self.assertLessEqual(y["incremental_cva"], x["incremental_cva"])

    def test_default_mass_reconciliation(self):
        rows = simulate(paths=100, years=4, hazard=.1)
        self.assertAlmostEqual(sum(r["default_mass"] for r in rows), 1-math.exp(-.4))

    def test_quantile(self):
        self.assertEqual(quantile([0, 10], .5), 5)

    def test_invalid(self):
        for kwargs in ({"paths": 99}, {"years": True}, {"hazard": -1},
                       {"volatility": float("nan")}, {"lgd": 1.1}, {"seed": 1.5}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                simulate(**kwargs)

if __name__ == "__main__":
    unittest.main()
