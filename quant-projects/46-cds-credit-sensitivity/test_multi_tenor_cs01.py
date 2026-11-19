"""Deterministic synthetic tests; no third-party market data."""
import unittest
from multi_tenor_cs01 import calibrate, legs, bucket_cs01


class MultiTenorTests(unittest.TestCase):
    def test_reprices_quotes(self):
        tenors = (1, 3, 5)
        quotes = (60, 100, 140)
        hazards = calibrate(tenors, quotes)
        for i, (t, q) in enumerate(zip(tenors, quotes)):
            a, p = legs(t, tenors[:i+1], hazards[:i+1])
            self.assertAlmostEqual(10000 * p / a, q, places=6)

    def test_positive_hazards_and_pv(self):
        x = bucket_cs01()
        self.assertEqual(len(x["buckets"]), 3)
        self.assertTrue(all(0 <= h <= 5 for h in x["hazards"]))

    def test_bucket_sum(self):
        x = bucket_cs01()
        self.assertAlmostEqual(sum(b["cs01"] for b in x["buckets"]), x["parallel_sum"], places=8)

    def test_notional_scaling(self):
        a = bucket_cs01(notional=100_000)
        b = bucket_cs01(notional=1_000_000)
        for x, y in zip(a["buckets"], b["buckets"]):
            self.assertAlmostEqual(y["cs01"], 10 * x["cs01"], places=5)

    def test_zero_quote_one_sided(self):
        x = bucket_cs01(tenors=(1,), quotes_bp=(0,), maturity=1)
        self.assertEqual(x["buckets"][0]["method"], "forward")

    def test_infeasible_curve(self):
        with self.assertRaises(ValueError):
            calibrate((1, 3), (1000, 0))

    def test_invalid_inputs(self):
        for kwargs in ({"quotes_bp": (True, 100, 140)},
                       {"tenors": (1, 1, 5)},
                       {"maturity": 6}, {"frequency": True},
                       {"bump_bp": 0}, {"notional": float("nan")}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                bucket_cs01(**kwargs)


if __name__ == "__main__":
    unittest.main()
