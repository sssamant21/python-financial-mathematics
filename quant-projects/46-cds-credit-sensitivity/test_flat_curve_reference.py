"""Independent closed-form reference for a flat synthetic CDS hazard curve.

For equal coupon/default settlement intervals, the ratio of protection to
premium annuity telescopes to (1-R)*f*(exp(h/f)-1), independent of discounting.
This is deliberately NOT an ISDA or market-convention benchmark.
"""
import math
import unittest

from multi_tenor_cs01 import calibrate, legs, bucket_cs01


class FlatCurveReferenceTests(unittest.TestCase):
    def test_one_tenor_closed_form_hazard(self):
        for quote in (0., 50., 250., 1000.):
            for rate in (-.01, .02, .10):
                expected = 4 * math.log1p((quote / 10000) / (.6 * 4))
                actual = calibrate((5,), (quote,), rate=rate)[0]
                self.assertAlmostEqual(actual, expected, delta=1e-10)

    def test_flat_quotes_produce_flat_hazards(self):
        for quote in (50., 200., 600.):
            expected = 4 * math.log1p((quote / 10000) / (.6 * 4))
            hazards = calibrate((1, 3, 5), (quote, quote, quote))
            for hazard in hazards:
                self.assertAlmostEqual(hazard, expected, delta=1e-10)

    def test_independent_par_spread_identity(self):
        for hazard in (0., .01, .10):
            spread = .6 * 4 * math.expm1(hazard / 4)
            a, p = legs(5, (5,), (hazard,))
            self.assertAlmostEqual(p / a, spread, delta=1e-12)

    def test_par_coupon_zero_pv(self):
        quote = 120.
        result = bucket_cs01((5,), (quote,), maturity=5, coupon_bp=quote)
        self.assertAlmostEqual(result["pv"], 0., delta=1e-6)


if __name__ == "__main__":
    unittest.main()
