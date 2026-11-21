"""Deterministic mathematical checks; no platform-dependent byte assertions."""
import tracemalloc
import unittest
from decimal import Decimal
from memory_comparison import compare_patterns


class MemoryComparisonTests(unittest.TestCase):
    def test_both_patterns_and_support(self):
        rows = compare_patterns((4, 8))
        self.assertEqual([(r["borrowers"], r["pattern"], r["expected_states"]) for r in rows],
                         [(4, "equal", 5), (4, "distinct", 16),
                          (8, "equal", 9), (8, "distinct", 256)])

    def test_matched_tail_probabilities(self):
        rows = compare_patterns((4, 8, 12))
        for n in (4, 8, 12):
            pair = [r for r in rows if r["borrowers"] == n]
            self.assertEqual(Decimal(pair[0]["tail_probability"]),
                             Decimal(pair[1]["tail_probability"]))
            self.assertGreater(pair[1]["expected_states"], pair[0]["expected_states"])

    def test_traced_allocations_are_descriptive(self):
        for row in compare_patterns((4,)):
            self.assertGreater(row["peak_traced_bytes"], 0)
            self.assertGreaterEqual(row["peak_traced_bytes"], row["final_traced_bytes"])
            self.assertIn("not process RSS", row["memory_metric"])
        self.assertFalse(tracemalloc.is_tracing())

    def test_invalid_sizes(self):
        for sizes in ((), (0,), (13,), (True,), ("4",), 4):
            with self.subTest(sizes=sizes), self.assertRaises(ValueError):
                compare_patterns(sizes)

    def test_state_limit_fails_closed_and_cleans_up(self):
        with self.assertRaisesRegex(ValueError, "state limit"):
            compare_patterns((8,), max_states=100)
        self.assertFalse(tracemalloc.is_tracing())


if __name__ == "__main__":
    unittest.main()
