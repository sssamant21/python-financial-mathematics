import unittest
from maturity_diagnostics import diagnostics, duration


class MaturityDiagnosticsTests(unittest.TestCase):
    def test_single_year_duration(self):
        self.assertAlmostEqual(duration({3: 100}, 0.04), 3)

    def test_matching_flows(self):
        row = diagnostics({1: 100, 2: 100}, {1: 100, 2: 100})["rates"][1]
        self.assertAlmostEqual(row["pv_gap"], 0)
        self.assertAlmostEqual(row["duration_gap_years"], 0)
        self.assertAlmostEqual(row["gap_rate_derivative"], 0)

    def test_timing_mismatch_with_equal_nominal_total(self):
        x = diagnostics({1: 80, 2: 120}, {1: 100, 2: 100})
        self.assertLess(x["minimum_cumulative_balance"], 0)
        self.assertGreater(x["rates"][1]["duration_gap_years"], 0)
        self.assertLess(x["rates"][1]["pv_gap"], 0)

    def test_rate_derivative_finite_difference(self):
        a, l, r, h = {1: 80, 2: 120}, {1: 100, 2: 100}, .04, 1e-5
        actual = diagnostics(a, l, (r,))["rates"][0]["gap_rate_derivative"]
        up = diagnostics(a, l, (r+h,))["rates"][0]["pv_gap"]
        down = diagnostics(a, l, (r-h,))["rates"][0]["pv_gap"]
        self.assertAlmostEqual(actual, (up-down)/(2*h), places=5)

    def test_empty_rates(self):
        with self.assertRaises(ValueError):
            diagnostics({1: 1}, {1: 1}, ())

    def test_invalid_rate(self):
        with self.assertRaises(ValueError):
            diagnostics({1: 1}, {1: 1}, (-.01,))

    def test_zero_pv_duration(self):
        with self.assertRaises(ValueError):
            duration({1: 0}, .04)

    def test_no_mutation(self):
        a, l = {1: 80, 2: 120}, {1: 100, 2: 100}
        diagnostics(a, l)
        self.assertEqual(a, {1: 80, 2: 120})
        self.assertEqual(l, {1: 100, 2: 100})


if __name__ == "__main__":
    unittest.main()
