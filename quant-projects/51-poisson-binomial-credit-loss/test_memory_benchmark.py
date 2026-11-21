"""Deterministic assertions for memory diagnostics; no brittle byte targets."""
import tracemalloc
import unittest
from memory_benchmark import measure_peak_allocations


class MemoryBenchmarkTests(unittest.TestCase):
    def test_equal_state_count(self):
        row = measure_peak_allocations(8, "equal")
        self.assertEqual(row["peak_states"], 9)
        self.assertGreaterEqual(row["peak_traced_bytes"], row["final_traced_bytes"])
        self.assertGreater(row["peak_traced_bytes"], 0)
        self.assertTrue(row["tail_probability"].startswith("0."))

    def test_distinct_state_count(self):
        row = measure_peak_allocations(4, "distinct")
        self.assertEqual(row["peak_states"], 16)
        self.assertEqual(row["final_states"], 16)

    def test_state_limit_and_trace_cleanup(self):
        with self.assertRaisesRegex(ValueError, "state limit"):
            measure_peak_allocations(8, "distinct", max_states=100)
        self.assertFalse(tracemalloc.is_tracing())

    def test_input_guards(self):
        for args in ((True, "equal"), (0, "equal"), (13, "distinct"), (4, "invalid")):
            with self.subTest(args=args), self.assertRaises(ValueError):
                measure_peak_allocations(*args)

    def test_equal_tail_matches_independent_analytic_formula(self):
        from decimal import Decimal
        for n in (1, 4, 12, 20):
            with self.subTest(n=n):
                row = measure_peak_allocations(n, "equal", precision=100)
                expected = Decimal(1) - (Decimal(3) / 4) ** n
                self.assertEqual(Decimal(row["tail_probability"]), expected)
                self.assertEqual(row["peak_states"], n + 1)
                self.assertEqual(row["final_states"], n + 1)

    def test_distinct_state_limit_exact_boundary(self):
        row = measure_peak_allocations(8, "distinct", max_states=256)
        self.assertEqual(row["peak_states"], 256)
        self.assertEqual(row["final_states"], 256)
        with self.assertRaisesRegex(ValueError, "state limit"):
            measure_peak_allocations(8, "distinct", max_states=255)
        self.assertFalse(tracemalloc.is_tracing())

    def test_preexisting_tracing_is_not_stopped(self):
        tracemalloc.start()
        try:
            with self.assertRaisesRegex(RuntimeError, "already active"):
                measure_peak_allocations(4)
            self.assertTrue(tracemalloc.is_tracing())
        finally:
            tracemalloc.stop()


if __name__ == "__main__":
    unittest.main()
