"""Synthetic deterministic tests for one-year dependence stress."""
import math
import unittest
from dependence_stress import estimate, analytical_epe

class DependenceStressTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(estimate(paths=300, seed=5), estimate(paths=300, seed=5))
    def test_zero_volatility(self):
        self.assertEqual(estimate(volatility=0, paths=300)["cva"], 0)
    def test_zero_lgd(self):
        self.assertEqual(estimate(lgd=0, paths=300)["cva"], 0)
    def test_analytical_epe(self):
        self.assertAlmostEqual(analytical_epe(100, .2, 0), 20 / math.sqrt(2 * math.pi))
    def test_threshold_reduces_loss_matched_paths(self):
        a = estimate(paths=1000, seed=8, rho=-.5, threshold=0)
        b = estimate(paths=1000, seed=8, rho=-.5, threshold=100000)
        self.assertLessEqual(b["cva"], a["cva"])
    def test_dependence_direction_with_common_draws(self):
        a = estimate(paths=20000, seed=19, rho=-.6)
        b = estimate(paths=20000, seed=19, rho=0)
        c = estimate(paths=20000, seed=19, rho=.6)
        self.assertGreater(a["cva"], b["cva"])
        self.assertGreater(b["cva"], c["cva"])
    def test_independence_within_sampling_uncertainty(self):
        r = estimate(paths=30000, seed=11, rho=0)
        self.assertLess(abs(r["cva"] - r["independent_benchmark"]), 5 * r["standard_error"])
    def test_invalid(self):
        for kwargs in ({"paths": True}, {"paths": 99}, {"rho": 1}, {"rho": float("nan")},
                       {"default_probability": 0}, {"default_probability": 1},
                       {"lgd": 1.1}, {"notional": -1}, {"seed": 1.5}, {"rate": -1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                estimate(**kwargs)

if __name__ == "__main__":
    unittest.main()
