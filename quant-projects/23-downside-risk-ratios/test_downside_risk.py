"""Deterministic regression tests for synthetic Project 23."""
import math
import unittest

from downside_risk import downside_metrics, trailing_metrics


class DownsideRiskTests(unittest.TestCase):
    def test_known_values(self):
        m = downside_metrics([0.1, -0.2, 0.3, -0.1], periods_per_year=4)
        self.assertAlmostEqual(m["downside_deviation_per_period"], math.sqrt(0.0125))
        self.assertAlmostEqual(m["omega"], 4 / 3)
        self.assertAlmostEqual(m["shortfall_fraction"], 0.5)
        self.assertAlmostEqual(m["sortino"], 0.025 * 2 / math.sqrt(0.0125))

    def test_zero_shortfall_undefined(self):
        m = downside_metrics([0.01, 0.02, 0.03])
        self.assertIsNone(m["sortino"])
        self.assertIsNone(m["omega"])

    def test_all_losses(self):
        m = downside_metrics([-0.1, -0.2, -0.3])
        self.assertEqual(m["omega"], 0.0)
        self.assertLess(m["sortino"], 0)

    def test_target_sensitivity(self):
        values = [0.01, 0.02, -0.01, 0.03]
        self.assertGreater(downside_metrics(values, 0.0)["omega"],
                           downside_metrics(values, 0.02)["omega"])

    def test_annualization(self):
        a = downside_metrics([0.1, -0.1, 0.03], periods_per_year=4)
        b = downside_metrics([0.1, -0.1, 0.03], periods_per_year=16)
        self.assertAlmostEqual(b["sortino"], 2 * a["sortino"])
        self.assertAlmostEqual(a["omega"], b["omega"])

    def test_future_mutation_isolation(self):
        a = [0.02, -0.04, 0.03, 0.01, -0.02]
        b = a[:]
        b[-1] = -0.9
        self.assertEqual(trailing_metrics(a, 3)[0], trailing_metrics(b, 3)[0])

    def test_window_count(self):
        self.assertEqual(len(trailing_metrics([0, 0.1, -0.1, 0.2, -0.2], 3)), 3)

    def test_reject_bad_returns(self):
        for bad in ([], [0, 0], [0, 0, float("nan")], [0, 0, -1.01],
                    [0, 0, True], "bad"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                downside_metrics(bad)

    def test_reject_bad_target(self):
        for target in (True, -1.0, float("inf"), float("nan")):
            with self.subTest(target=target), self.assertRaises(ValueError):
                downside_metrics([0.1, 0.2, -0.1], target)

    def test_reject_bad_frequency_and_window(self):
        for freq in (True, 0, 367, 12.0):
            with self.subTest(freq=freq), self.assertRaises(ValueError):
                downside_metrics([0.1, -0.1, 0], periods_per_year=freq)
        for window in (True, 2, 5, 3.0):
            with self.subTest(window=window), self.assertRaises(ValueError):
                trailing_metrics([0.1, -0.1, 0, 0.2], window)


if __name__ == "__main__":
    unittest.main()
