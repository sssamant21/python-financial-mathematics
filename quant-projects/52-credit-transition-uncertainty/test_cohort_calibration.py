"""Synthetic, deterministic checks for the cohort split and scoring."""
import math
import unittest

from cohort_calibration import cohort_diagnostics


class CohortTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(cohort_diagnostics(), cohort_diagnostics())

    def test_training_only_posterior(self):
        r = cohort_diagnostics(0.2, 30, 40, (2.0, 3.0), 11)
        expected = (r["train_defaults"] + 3) / (r["train_size"] + 5)
        self.assertAlmostEqual(r["posterior_mean_default"], expected)

    def test_heldout_size_does_not_change_training_fit(self):
        a = cohort_diagnostics(0.1, 100, 20, seed=17)
        b = cohort_diagnostics(0.1, 100, 1000, seed=17)
        self.assertEqual(a["train_defaults"], b["train_defaults"])
        self.assertEqual(a["posterior_mean_default"], b["posterior_mean_default"])

    def test_brier_and_log_loss_reconciliation(self):
        r = cohort_diagnostics(0.3, 30, 40, seed=13)
        p, n, d = r["posterior_mean_default"], r["heldout_size"], r["heldout_defaults"]
        self.assertAlmostEqual(r["heldout_brier_score"], (d*(1-p)**2+(n-d)*p**2)/n)
        self.assertAlmostEqual(r["heldout_log_loss"], -(d*math.log(p)+(n-d)*math.log1p(-p))/n)

    def test_invalid_inputs(self):
        bad = [
            {"true_pd": 0}, {"true_pd": 1}, {"true_pd": float("nan")},
            {"train_size": True}, {"heldout_size": 0}, {"seed": -1},
            {"prior": (1,)}, {"prior": (0, 1)},
        ]
        for kwargs in bad:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                cohort_diagnostics(**kwargs)


if __name__ == "__main__":
    unittest.main()
