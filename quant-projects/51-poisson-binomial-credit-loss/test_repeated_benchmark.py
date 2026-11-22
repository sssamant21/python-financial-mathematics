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


    def test_rejects_mathematical_drift_between_repetitions(self):
        from unittest.mock import patch
        row = {"borrowers": 4, "pattern": "equal", "final_states": 5,
               "peak_states": 5, "expected_states": 5,
               "tail_probability": "0.5", "analytical_tail": "0.5",
               "peak_traced_bytes": 12}
        base = {"schema_version": 1, "synthetic_only": True,
                "python_version": "test", "platform": "test",
                "batch_elapsed_seconds": 0.1, "rows": [row]}
        changed = {**base, "rows": [{**row, "tail_probability": "0.6",
                                    "analytical_tail": "0.6"}]}
        with patch("repeated_benchmark.collect_report", side_effect=[base, changed]):
            with self.assertRaisesRegex(AssertionError, "non-deterministic"):
                collect_repeated(2, (4,))

    def test_rejects_corrupted_state_counts(self):
        from unittest.mock import patch
        row = {"borrowers": 4, "pattern": "equal", "final_states": 4,
               "peak_states": 5, "expected_states": 5,
               "tail_probability": "0.5", "analytical_tail": "0.5",
               "peak_traced_bytes": 12}
        run = {"schema_version": 1, "synthetic_only": True,
               "batch_elapsed_seconds": 0.1, "rows": [row]}
        with patch("repeated_benchmark.collect_report", return_value=run):
            with self.assertRaisesRegex(AssertionError, "state count mismatch"):
                collect_repeated(2, (4,))

    def test_rejects_nonfinite_or_negative_elapsed(self):
        from unittest.mock import patch
        for elapsed in (-0.01, float("nan"), float("inf")):
            row = {"borrowers": 4, "pattern": "equal", "final_states": 5,
                   "peak_states": 5, "expected_states": 5,
                   "tail_probability": "0.5", "analytical_tail": "0.5",
                   "peak_traced_bytes": 12}
            run = {"schema_version": 1, "synthetic_only": True,
                   "batch_elapsed_seconds": elapsed, "rows": [row]}
            with self.subTest(elapsed=elapsed), patch(
                "repeated_benchmark.collect_report", return_value=run
            ):
                with self.assertRaisesRegex(AssertionError, "invalid elapsed"):
                    collect_repeated(2, (4,))

    def test_rejects_invalid_traced_allocation(self):
        from unittest.mock import patch
        for allocation in (-1, 1.5):
            row = {"borrowers": 4, "pattern": "equal", "final_states": 5,
                   "peak_states": 5, "expected_states": 5,
                   "tail_probability": "0.5", "analytical_tail": "0.5",
                   "peak_traced_bytes": allocation}
            run = {"schema_version": 1, "synthetic_only": True,
                   "batch_elapsed_seconds": 0.1, "rows": [row]}
            with self.subTest(allocation=allocation), patch(
                "repeated_benchmark.collect_report", return_value=run
            ):
                with self.assertRaisesRegex(AssertionError, "invalid traced memory"):
                    collect_repeated(2, (4,))

if __name__ == "__main__":
    unittest.main()
