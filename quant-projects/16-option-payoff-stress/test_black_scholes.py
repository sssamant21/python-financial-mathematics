"""Deterministic independent benchmark and invariants for educational BSM."""
import math
import unittest
from black_scholes import price, parity_residual, greeks_fd

class BlackScholesTests(unittest.TestCase):
    def test_classic_atm_benchmark(self):
        self.assertAlmostEqual(price('call', 100, 100, 1, .05, .2), 10.450583572185565, places=8)
        self.assertAlmostEqual(price('put', 100, 100, 1, .05, .2), 5.573526022256971, places=8)
    def test_parity_with_dividends(self):
        for q in (0, .02, -.01):
            self.assertAlmostEqual(parity_residual(105, 95, 2, .03, .25, q), 0, places=10)
    def test_positive_and_bounds(self):
        c = price('call', 100, 95, 1, .02, .3, .01)
        p = price('put', 100, 95, 1, .02, .3, .01)
        self.assertGreaterEqual(c, max(0, 100*math.exp(-.01)-95*math.exp(-.02))-1e-10)
        self.assertLessEqual(c, 100*math.exp(-.01))
        self.assertGreaterEqual(p, 0)
        self.assertLessEqual(p, 95*math.exp(-.02))
    def test_monotonic_spot(self):
        self.assertGreater(price('call', 110, 100, 1, .02, .2), price('call', 90, 100, 1, .02, .2))
        self.assertLess(price('put', 110, 100, 1, .02, .2), price('put', 90, 100, 1, .02, .2))
    def test_greeks_against_analytic_atm(self):
        g = greeks_fd('call', 100, 100, 1, .05, .2)
        d1 = (.05 + .5*.2**2)/.2
        cdf = .5*(1+math.erf(d1/math.sqrt(2)))
        pdf = math.exp(-d1*d1/2)/math.sqrt(2*math.pi)
        self.assertAlmostEqual(g['delta'], cdf, places=5)
        self.assertAlmostEqual(g['gamma'], pdf/(100*.2), places=5)
        self.assertAlmostEqual(g['vega'], 100*pdf, places=4)
    def test_put_call_delta_difference(self):
        c = greeks_fd('call', 100, 100, 1, .02, .2, .01)
        p = greeks_fd('put', 100, 100, 1, .02, .2, .01)
        self.assertAlmostEqual(c['delta']-p['delta'], math.exp(-.01), places=6)
    def test_invalid_inputs(self):
        bad = [(0,100,1,.05,.2,0), (100,0,1,.05,.2,0), (100,100,0,.05,.2,0),
               (100,100,1,.05,0,0), (100,100,1,.05,float('nan'),0),
               (True,100,1,.05,.2,0), (100,100,1,2,.2,0)]
        for args in bad:
            with self.subTest(args=args), self.assertRaises(ValueError):
                price('call', *args)
        with self.assertRaises(ValueError):
            price('other',100,100,1,.05,.2)
    def test_bad_steps(self):
        for h, v in ((0,.001), (100,.001), (.01,0), (.01,.2)):
            with self.assertRaises(ValueError):
                greeks_fd('call',100,100,1,.05,.2,spot_step=h,vol_step=v)
    def test_deterministic(self):
        self.assertEqual(price('put', 99, 101, .5, -.01, .4), price('put', 99, 101, .5, -.01, .4))

if __name__ == '__main__':
    unittest.main()
