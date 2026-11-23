"""Deterministic synthetic checks for Dirichlet transition uncertainty."""
import math
import unittest
from transition_uncertainty import posterior_alpha, summarize_default

class TransitionTests(unittest.TestCase):
    def test_conjugate_update(self):
        self.assertEqual(posterior_alpha([10, 2, 0], [1, 1, 1]), [11, 3, 1])

    def test_posterior_mean_identity(self):
        result = summarize_default([8, 1, 1], [1, 1, 1], 2, 1000, 7)
        self.assertAlmostEqual(result["posterior_mean_default"], 2 / 13)
        self.assertEqual(result["observed_transitions"], 10)

    def test_seed_reproducibility(self):
        self.assertEqual(summarize_default([20, 3, 1], [1, 1, 1], 2, 500, 3),
                         summarize_default([20, 3, 1], [1, 1, 1], 2, 500, 3))

    def test_interval_bounded_ordered(self):
        lo, hi = summarize_default([30, 2, 1], [1, 1, 1], 2, 500, 5)["credible_interval_95"]
        self.assertTrue(0 <= lo <= hi <= 1)

    def test_zero_observations_prior_only(self):
        result = summarize_default([0, 0], [2, 3], 1, 500, 4)
        self.assertAlmostEqual(result["posterior_mean_default"], 3 / 5)

    def test_bad_inputs(self):
        cases = [([1, -1], [1, 1], 1), ([True, 1], [1, 1], 1),
                 ([1, 2], [0, 1], 1), ([1, 2], [math.nan, 1], 1),
                 ([1, 2], [1], 1), ([1, 2], [1, 1], 2)]
        for counts, prior, idx in cases:
            with self.subTest(counts=counts, prior=prior, idx=idx):
                with self.assertRaises(ValueError):
                    summarize_default(counts, prior, idx, 100, 0)

    def test_bad_draws_and_seed(self):
        for draws, seed in [(99, 1), (True, 1), (100, -1), (100, True)]:
            with self.assertRaises(ValueError):
                summarize_default([1, 1], [1, 1], 1, draws, seed)

if __name__ == "__main__":
    unittest.main()
