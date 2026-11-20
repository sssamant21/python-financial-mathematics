"""Deterministic regression checks for synthetic EPE convergence."""
import math
import unittest
from convergence import convergence

class ConvergenceTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(convergence(path_counts=(100, 400), seeds=(1, 2, 3)),
                         convergence(path_counts=(100, 400), seeds=(1, 2, 3)))

    def test_zero_volatility_exact(self):
        rows = convergence(path_counts=(100, 200), seeds=(1, 2), volatility=0)
        self.assertTrue(all(r["mean_epe"] == r["analytical_epe"] == r["absolute_error"] == r["between_seed_se"] == 0 for r in rows))

    def test_threshold_reduces_benchmark(self):
        a = convergence(path_counts=(100,), seeds=(1, 2), threshold=0)[0]
        b = convergence(path_counts=(100,), seeds=(1, 2), threshold=100)[0]
        self.assertLess(b["analytical_epe"], a["analytical_epe"])

    def test_error_definition(self):
        r = convergence(path_counts=(100,), seeds=(1, 2))[0]
        self.assertAlmostEqual(r["absolute_error"], abs(r["mean_epe"]-r["analytical_epe"]))
        self.assertTrue(math.isfinite(r["between_seed_se"]))

    def test_no_monotonic_error_claim(self):
        rows = convergence(path_counts=(100, 400), seeds=(1, 2, 3))
        self.assertEqual([r["paths"] for r in rows], [100, 400])
        self.assertTrue(all(r["between_seed_se"] >= 0 for r in rows))

    def test_invalid_counts(self):
        for counts in ((), (99,), (100, 100), (200, 100), (True,)):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                convergence(path_counts=counts)

    def test_invalid_seeds(self):
        for seeds in ((), (1,), (1, 1), (True, 2), (1, 2.5)):
            with self.subTest(seeds=seeds), self.assertRaises(ValueError):
                convergence(path_counts=(100,), seeds=seeds)

    def test_invalid_economics(self):
        for kwargs in ({"year": 0}, {"year": True}, {"notional": -1},
                       {"volatility": -1}, {"threshold": float("nan")}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                convergence(path_counts=(100,), seeds=(1, 2), **kwargs)

    def test_budget_guard(self):
        with self.assertRaises(ValueError):
            convergence(path_counts=(200000,), seeds=(1, 2, 3, 4), year=5)

if __name__ == "__main__":
    unittest.main()
