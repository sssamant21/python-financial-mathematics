"""Synthetic, deterministic checks for the predeclared paired-prior study."""
import math
import unittest

from cohort_calibration import cohort_diagnostics
from prior_stability import prior_stability


class PriorStabilityTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(prior_stability(repetitions=3), prior_stability(repetitions=3))

    def test_paired_cohorts_and_training_only_fit(self):
        result = prior_stability(train_size=80, heldout_size=40,
                                 repetitions=3, strengths=(0.5, 5.0))
        for seed in range(42, 45):
            rows = [r for r in result["runs"] if r["seed"] == seed]
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["train_defaults"], rows[1]["train_defaults"])
            self.assertEqual(rows[0]["heldout_defaults"], rows[1]["heldout_defaults"])
            for row in rows:
                reference = cohort_diagnostics(0.04, 80, 40,
                    (row["strength"], row["strength"]), seed)
                for key, value in reference.items():
                    self.assertEqual(row[key], value)

    def test_aggregate_reconciliation(self):
        result = prior_stability(repetitions=4, strengths=(0.5, 1.0))
        for summary in result["summary"]:
            group = [r for r in result["runs"] if r["strength"] == summary["strength"]]
            self.assertAlmostEqual(summary["mean_log_loss"],
                sum(r["heldout_log_loss"] for r in group) / len(group))
            self.assertAlmostEqual(summary["mean_brier"],
                sum(r["heldout_brier_score"] for r in group) / len(group))
            self.assertAlmostEqual(summary["mean_absolute_gap"],
                sum(abs(r["heldout_calibration_gap"]) for r in group) / len(group))

    def test_invalid_grid_and_budget(self):
        cases = ({"strengths": (0.0,)}, {"strengths": (float("nan"),)},
                 {"strengths": (1.0, 1.0)}, {"strengths": (True,)},
                 {"strengths": ()}, {"repetitions": 1},
                 {"first_seed": 2**32 - 1},
                 {"train_size": 100000, "heldout_size": 100000,
                  "repetitions": 100, "strengths": (1.0, 2.0)})
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                prior_stability(**kwargs)

    def test_no_real_data_or_selection(self):
        result = prior_stability(repetitions=2)
        self.assertTrue(result["synthetic"])
        self.assertNotIn("best_strength", result)
        self.assertEqual(len(result["runs"]), 6)


if __name__ == "__main__":
    unittest.main()
