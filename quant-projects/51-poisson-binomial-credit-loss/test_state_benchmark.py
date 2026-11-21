"""Benchmark invariants; never assert a machine-dependent runtime target."""
import unittest
from decimal import Decimal
from state_benchmark import benchmark_case, binomial_reference, run_suite


class BenchmarkTests(unittest.TestCase):
    def test_equal_loss_combinatorial_reference(self):
        for n in (4, 8, 12, 20, 40):
            with self.subTest(n=n):
                row = benchmark_case(n, "equal")
                self.assertEqual(row["expected_states"], n+1)
                self.assertEqual(Decimal(row["absolute_error"]), 0)

    def test_distinct_loss_exhaustive_reference(self):
        for n in (4, 8, 12):
            with self.subTest(n=n):
                row = benchmark_case(n, "distinct")
                self.assertEqual(row["expected_states"], 2**n)
                self.assertEqual(Decimal(row["absolute_error"]), 0)

    def test_state_cap_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "state limit"):
            benchmark_case(8, "distinct", max_states=100)

    def test_guardrails(self):
        for n, kind in ((0, "equal"), (13, "distinct"), (4, "unknown"), (True, "equal")):
            with self.subTest(n=n, kind=kind), self.assertRaises(ValueError):
                benchmark_case(n, kind)

    def test_inventory(self):
        self.assertEqual(len(run_suite()), 8)
        self.assertEqual(binomial_reference(2, "0.5", 1), Decimal("0.75"))


if __name__ == "__main__":
    unittest.main()
