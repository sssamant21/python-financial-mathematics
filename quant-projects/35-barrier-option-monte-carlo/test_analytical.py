"""Synthetic analytical checks; no external market data."""
import math
import unittest
from analytical import up_and_out_call
from bridge import compare_bridge


class AnalyticalTests(unittest.TestCase):
    def test_strike_at_or_above_barrier(self):
        self.assertEqual(up_and_out_call(strike=130), 0.)
        self.assertEqual(up_and_out_call(strike=150), 0.)

    def test_barrier_increases_price_in_example(self):
        self.assertLessEqual(up_and_out_call(barrier=120),up_and_out_call(barrier=150))

    def test_vanilla_limit(self):
        spot, strike, rate, vol, years = 100.,100.,0.02,0.2,1.
        d1=(math.log(spot/strike)+(rate+vol*vol/2)*years)/(vol*math.sqrt(years))
        d2=d1-vol*math.sqrt(years)
        cdf=lambda z:0.5*math.erfc(-z/math.sqrt(2))
        vanilla=spot*cdf(d1)-strike*math.exp(-rate*years)*cdf(d2)
        self.assertAlmostEqual(up_and_out_call(barrier=1000),vanilla,places=6)

    def test_bridge_monte_carlo_consistency(self):
        mc=compare_bridge(pairs=3000,steps=12,seed=2026)
        reference=up_and_out_call()
        self.assertLess(abs(mc['continuous_bridge_call']-reference),6*mc['continuous_se']+0.03)

    def test_invalid_inputs(self):
        for kw in ({'spot':0},{'barrier':100},{'vol':0},{'years':float('nan')},
                   {'rate':float('inf')},{'vol':1e-12}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):
                up_and_out_call(**kw)

if __name__ == '__main__':
    unittest.main()
