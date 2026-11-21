"""Synthetic report-contract tests; no fixed timing or memory-byte thresholds."""
import unittest
from datetime import datetime
from benchmark_report import collect_report


class ReportTests(unittest.TestCase):
    def test_report_has_observation_context(self):
        report = collect_report((4,))
        self.assertTrue(report["synthetic_only"])
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["scenario_sizes"], [4])
        self.assertEqual(len(report["rows"]), 2)
        self.assertGreaterEqual(report["batch_elapsed_seconds"], 0)
        datetime.fromisoformat(report["observed_at_utc"])

    def test_mathematical_support_and_tail(self):
        report = collect_report((4, 16))
        self.assertEqual(
            [(r["borrowers"], r["pattern"], r["expected_states"]) for r in report["rows"]],
            [(4, "equal", 5), (4, "distinct", 16), (16, "equal", 17)])
        for row in report["rows"]:
            self.assertEqual(row["tail_probability"], row["analytical_tail"])

    def test_fail_closed_on_state_cap(self):
        with self.assertRaisesRegex(ValueError, "state limit"):
            collect_report((8,), max_states=100)


if __name__ == "__main__":
    unittest.main()
