"""Deterministic standard-library regression checks."""
import unittest
from cashflow_matching import present_value, funding_gap, coverage_by_year, stress


class CashflowTests(unittest.TestCase):
    def test_zero_rate(self):
        self.assertEqual(present_value({1: 100, 2: 50}, 0), 150)

    def test_discount(self):
        self.assertAlmostEqual(present_value({1: 110}, 0.1), 100)

    def test_matching(self):
        self.assertAlmostEqual(funding_gap({1: 110}, {1: 110}, 0.05), 0)

    def test_coverage(self):
        self.assertEqual(coverage_by_year({1: 100, 2: 50}, {1: 80, 2: 70}), [(1, 20), (2, 0)])

    def test_intermediate_shortfall(self):
        self.assertEqual(coverage_by_year({2: 100}, {1: 50}), [(1, -50), (2, 50)])

    def test_rate_stress(self):
        self.assertEqual(len(stress({1: 100}, {1: 90})), 3)

    def test_reject_bad_rate(self):
        for rate in (-0.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                present_value({1: 10}, rate)

    def test_reject_bad_year(self):
        for year in (0, -1, 1.5, True, 101):
            with self.assertRaises(ValueError):
                present_value({year: 10}, 0.02)

    def test_reject_negative_flow(self):
        with self.assertRaises(ValueError):
            present_value({1: -1}, 0.02)

    def test_no_mutation(self):
        assets = {1: 100}
        funding_gap(assets, {1: 50}, 0.03)
        self.assertEqual(assets, {1: 100})


if __name__ == "__main__":
    unittest.main()
