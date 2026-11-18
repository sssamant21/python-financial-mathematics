import math
import unittest
from cds_risk import legs, pv
from quote_cs01 import hazard_from_quote, quote_cs01


class TestQuoteCS01(unittest.TestCase):
    def test_recalibrated_par_quote(self):
        for q in (0, 20, 120, 800):
            for f in (1, 4, 12):
                with self.subTest(q=q, f=f):
                    h = hazard_from_quote(q, frequency=f)
                    a, p = legs(h, maturity=2, frequency=f)
                    self.assertAlmostEqual(p / a * 10000, q, places=7)

    def test_at_par_pv_is_zero(self):
        self.assertAlmostEqual(quote_cs01(quote_bp=120, coupon_bp=120)["pv"], 0, places=7)

    def test_quote_cs01_positive_for_buyer(self):
        self.assertGreater(quote_cs01()["quote_cs01"], 0)

    def test_quote_cs01_matches_independent_repricing(self):
        x = quote_cs01(quote_bp=120, bump_bp=2)
        def value(q):
            return pv(hazard_from_quote(q), .01)
        self.assertAlmostEqual(x["quote_cs01"], (value(122)-value(118))/4, places=7)

    def test_zero_quote_forward(self):
        x = quote_cs01(quote_bp=0)
        self.assertEqual(x["difference"], "forward")
        self.assertAlmostEqual(x["quote_cs01"], pv(hazard_from_quote(1), .01) - pv(0, .01), places=7)

    def test_notional_scaling(self):
        a = quote_cs01(notional=100_000)
        b = quote_cs01(notional=1_000_000)
        self.assertAlmostEqual(b["quote_cs01"], 10*a["quote_cs01"], places=7)

    def test_rejects_bad_inputs(self):
        for kwargs in ({"quote_bp": True}, {"quote_bp": -1}, {"coupon_bp": math.nan},
                       {"bump_bp": 0}, {"recovery": 1}, {"frequency": True},
                       {"maturity": .3}, {"notional": float("inf")},
                       {"quote_bp": 100000}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                quote_cs01(**kwargs)

    def test_one_sided_near_zero(self):
        self.assertEqual(quote_cs01(quote_bp=.5, bump_bp=1)["difference"], "forward")


if __name__ == "__main__":
    unittest.main()
