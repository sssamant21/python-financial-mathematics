"""Deterministic checks for repeated synthetic cohort diagnostics."""
import math
import unittest

from cohort_calibration import cohort_diagnostics
from repeated_cohorts import repeated_diagnostics


class RepeatedCohortTests(unittest.TestCase):
    def test_reproducible_and_all_runs_reported(self):
        a = repeated_diagnostics(repetitions=3, first_seed=17)
        self.assertEqual(a, repeated_diagnostics(repetitions=3, first_seed=17))
        self.assertEqual([r["seed"] for r in a["runs"]], [17, 18, 19])

    def test_matches_individual_runs(self):
        result = repeated_diagnostics(repetitions=3, first_seed=10)
        for index, row in enumerate(result["runs"]):
            self.assertEqual(row, cohort_diagnostics(seed=10 + index))

    def test_aggregate_reconciliation(self):
        result = repeated_diagnostics(repetitions=4)
        gaps = [r["heldout_calibration_gap"] for r in result["runs"]]
        self.assertAlmostEqual(result["aggregate"]["heldout_calibration_gap"]["mean"],
                               sum(gaps) / len(gaps))
        self.assertAlmostEqual(result["aggregate"]["mean_absolute_calibration_gap"],
                               sum(map(abs, gaps)) / len(gaps))
        self.assertAlmostEqual(result["aggregate"]["root_mean_squared_calibration_gap"],
                               math.sqrt(sum(g*g for g in gaps) / len(gaps)))

    def test_invalid_repetition_and_seed_ranges(self):
        for kwargs in ({"repetitions": 1}, {"repetitions": 201},
                       {"repetitions": True}, {"repetitions": 2.5},
                       {"first_seed": -1}, {"first_seed": True},
                       {"first_seed": 2**32 - 1, "repetitions": 2}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                repeated_diagnostics(**kwargs)

    def test_invalid_model_inputs_propagate(self):
        with self.assertRaises(ValueError):
            repeated_diagnostics(true_pd=float("nan"), repetitions=2)


if __name__ == "__main__":
    unittest.main()
