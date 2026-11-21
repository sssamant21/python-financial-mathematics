"""Benchmark invariants; never assert a machine-dependent runtime target."""
import unittest
from decimal import Decimal
from state_benchmark import benchmark_case, binomial_reference, run_suite
from sparse_monetary_tail import sparse_tail


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

    def test_repeated_synthetic_results_ignore_timing(self):
        first = benchmark_case(8, "equal")
        second = benchmark_case(8, "equal")
        first.pop("elapsed_seconds")
        second.pop("elapsed_seconds")
        self.assertEqual(first, second)

    def test_precision_sensitivity_against_independent_reference(self):
        for digits in (32, 100, 1000):
            with self.subTest(precision=digits):
                row = benchmark_case(12, "equal", precision=digits)
                self.assertEqual(Decimal(row["absolute_error"]), 0)
                self.assertEqual(row["precision_digits"], digits)

    def test_distinct_support_boundary(self):
        self.assertEqual(benchmark_case(4, "distinct", max_states=16)["expected_states"], 16)
        with self.assertRaisesRegex(ValueError, "state limit"):
            benchmark_case(4, "distinct", max_states=15)

    def test_observed_state_counts_equal_and_distinct(self):
        for exposures, expected in (([100]*8, 9), ([1, 2, 4, 8], 16)):
            with self.subTest(exposures=exposures):
                probability, diag = sparse_tail(["0.25"]*len(exposures), exposures,
                                                [1]*len(exposures), 1,
                                                return_diagnostics=True)
                baseline = sparse_tail(["0.25"]*len(exposures), exposures,
                                       [1]*len(exposures), 1)
                self.assertEqual(probability, baseline)
                self.assertEqual(diag["peak_states"], expected)
                self.assertEqual(diag["final_states"], expected)
                self.assertEqual(diag["processed_borrowers"], len(exposures))
                self.assertFalse(diag["early_exit"])

    def test_diagnostics_early_exit_and_type_guard(self):
        probability, diag = sparse_tail(["0.25"], [100], [1], 101,
                                        return_diagnostics=True)
        self.assertEqual(probability, Decimal(0))
        self.assertTrue(diag["early_exit"])
        self.assertEqual(diag["processed_borrowers"], 0)
        with self.assertRaisesRegex(ValueError, "return_diagnostics"):
            sparse_tail(["0.25"], [100], [1], 1, return_diagnostics=1)

    def test_inventory(self):
        self.assertEqual(len(run_suite()), 8)
        self.assertEqual(binomial_reference(2, "0.5", 1), Decimal("0.75"))


if __name__ == "__main__":
    unittest.main()
