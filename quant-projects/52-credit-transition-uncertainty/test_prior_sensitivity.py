"""Synthetic prior-strength sensitivity and held-out scoring checks.

All synthetic observations are predeclared; no market data is used.
"""
import math
import unittest
from transition_uncertainty import summarize_default, posterior_alpha


def prior_strength_grid(counts, baseline_prior, default_index, strengths=(0.5, 1.0, 5.0), draws=4000, seed=42):
    """Return comparable posterior summaries for fixed prior multipliers."""
    if not isinstance(strengths, (tuple, list)) or not strengths:
        raise ValueError("nonempty strength grid required")
    if any(isinstance(s, bool) or not isinstance(s, (int, float)) or
           not math.isfinite(s) or s <= 0 for s in strengths):
        raise ValueError("strengths must be finite positive numbers")
    if len(set(strengths)) != len(strengths):
        raise ValueError("duplicate strengths")
    results = []
    for strength in strengths:
        scaled = [float(a) * strength for a in baseline_prior]
        result = summarize_default(counts, scaled, default_index, draws, seed)
        results.append({"strength": strength, **result})
    return results


def heldout_log_score(posterior_default_probability, default_events, total_events):
    """Negative average Bernoulli log likelihood, using *held-out* counts."""
    p = posterior_default_probability
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 < p < 1:
        raise ValueError("probability must be strictly between zero and one")
    if type(default_events) is not int or type(total_events) is not int or not 0 <= default_events <= total_events or total_events == 0:
        raise ValueError("invalid held-out event counts")
    return -(default_events * math.log(p) + (total_events - default_events) * math.log1p(-p)) / total_events


class PriorSensitivityTests(unittest.TestCase):
    def test_grid_reproduces_single_run(self):
        rows = prior_strength_grid([90, 8, 2], [1, 1, 1], 2, (1.0,), 200, 11)
        self.assertEqual(rows[0]["posterior_mean_default"], 3 / 103)
        self.assertEqual(rows[0]["credible_interval_95"], summarize_default([90, 8, 2], [1, 1, 1], 2, 200, 11)["credible_interval_95"])

    def test_prior_strength_changes_mean_toward_prior(self):
        rows = prior_strength_grid([90, 8, 2], [1, 1, 1], 2, (0.5, 5.0), 200, 11)
        self.assertLess(rows[0]["posterior_mean_default"], rows[1]["posterior_mean_default"])

    def test_grid_rejects_invalid_values(self):
        for grid in [(), (0,), (-1,), (float("nan"),), (float("inf"),), (1, 1), (True,)]:
            with self.subTest(grid=grid), self.assertRaises(ValueError):
                prior_strength_grid([1, 1], [1, 1], 1, grid, 100, 0)

    def test_heldout_score_prefers_matching_rate(self):
        self.assertLess(heldout_log_score(0.1, 10, 100), heldout_log_score(0.5, 10, 100))

    def test_heldout_validation(self):
        for args in [(0, 1, 2), (1, 1, 2), (0.5, -1, 2), (0.5, 3, 2), (0.5, 0, 0), (float("nan"), 1, 2)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                heldout_log_score(*args)


if __name__ == "__main__":
    unittest.main()
