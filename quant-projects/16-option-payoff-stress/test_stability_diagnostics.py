"""Synthetic analytical benchmarks and numerical edge-case guardrails."""
import math
import unittest
from stability_diagnostics import analytic_greeks, diagnose

class StabilityDiagnosticsTests(unittest.TestCase):
    def test_atm_analytic_benchmark(self):
        g = analytic_greeks("call", 100, 100, 1, .05, .2)
        d1 = (.05 + .5*.2**2)/.2
        pdf = math.exp(-d1*d1/2)/math.sqrt(2*math.pi)
        self.assertAlmostEqual(g["gamma"], pdf / 20, places=10)
        self.assertAlmostEqual(g["vega"], 100 * pdf, places=10)

    def test_call_put_delta_identity(self):
        for years, sigma in ((1,.2), (1/365,.01)):
            c = analytic_greeks("call", 100, 100, years, .05, sigma, .02)
            p = analytic_greeks("put", 100, 100, years, .05, sigma, .02)
            self.assertAlmostEqual(c["delta"]-p["delta"], math.exp(-.02*years), places=10)
            self.assertAlmostEqual(c["gamma"], p["gamma"], places=10)
            self.assertAlmostEqual(c["vega"], p["vega"], places=10)

    def test_regular_case_matches_fd(self):
        row = diagnose(scenarios=((1,.2),))[0]
        self.assertTrue(row["within_tolerance"])
        self.assertLess(row["absolute_error"]["gamma"], 1e-4)

    def test_near_expiry_low_vol_finite(self):
        for kind in ("call", "put"):
            rows = diagnose(kind=kind)
            self.assertEqual(len(rows), 3)
            for row in rows:
                self.assertTrue(math.isfinite(row["price"]))
                for values in ("analytic", "finite_difference", "absolute_error"):
                    self.assertTrue(all(math.isfinite(x) for x in row[values].values()))

    def test_determinism(self):
        self.assertEqual(diagnose(), diagnose())

    def test_invalid_inputs(self):
        for kwargs in ({"scenarios": ()}, {"scenarios": ((0,.2),)},
                       {"scenarios": ((1,0),)}, {"scenarios": ((1,.2),)*31},
                       {"relative_spot_step": 0}, {"relative_vol_step": .5},
                       {"relative_spot_step": float("nan")}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                diagnose(**kwargs)
        with self.assertRaises(ValueError):
            analytic_greeks("other", 100, 100, 1, .05, .2)

if __name__ == "__main__":
    unittest.main()
