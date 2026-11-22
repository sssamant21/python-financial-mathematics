"""Deterministic contract checks; timing and byte values are not fixed."""
import unittest
from repeated_benchmark import collect_repeated


class RepeatedBenchmarkTests(unittest.TestCase):
    def test_two_runs_small_synthetic(self):
        report = collect_repeated(2, (4,), 100, 100)
        self.assertEqual(report["repetitions"], 2)
        self.assertEqual([(r["pattern"], r["expected_states"]) for r in report["rows"]],
                         [("equal", 5), ("distinct", 16)])
        self.assertLessEqual(report["batch_seconds_min"], report["batch_seconds_median"])
        self.assertLessEqual(report["batch_seconds_median"], report["batch_seconds_max"])
        for row in report["rows"]:
            self.assertLessEqual(row["peak_traced_bytes_min"], row["peak_traced_bytes_median"])
            self.assertLessEqual(row["peak_traced_bytes_median"], row["peak_traced_bytes_max"])

    def test_fail_closed_repetition_limits(self):
        for value in (0, 1, 11, True, 2.0):
            with self.subTest(value=value), self.assertRaises(ValueError):
                collect_repeated(value, (4,))

    def test_state_limit_propagates(self):
        with self.assertRaisesRegex(ValueError, "state limit"):
            collect_repeated(2, (8,), max_states=100)


if __name__ == "__main__":
    unittest.main()
