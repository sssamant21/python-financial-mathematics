import unittest
from math import exp
from repricing_check import price, check

FLOWS = [(1.0, 5.0), (2.0, 5.0), (3.0, 105.0)]

class RepricingTests(unittest.TestCase):
    def test_price_manual(self):
        self.assertAlmostEqual(price([(1.0, 100.0)], .02, .01), 100 * exp(-.03))
    def test_zero_shock(self):
        r = check(FLOWS, .02, .01, 0)
        self.assertAlmostEqual(r['approx_pnl'], 0)
        self.assertAlmostEqual(r['repriced_pnl'], 0)
    def test_small_shock_accuracy(self):
        self.assertLess(abs(check(FLOWS, .02, .01, 1)['error_bps_of_value']), 1e-5)
    def test_widening_loss(self):
        self.assertLess(check(FLOWS, .02, .01, 100)['repriced_pnl'], 0)
    def test_tightening_gain(self):
        self.assertGreater(check(FLOWS, .02, .01, -100)['repriced_pnl'], 0)
    def test_error_grows_for_large_shock(self):
        self.assertGreater(abs(check(FLOWS, .02, .01, 500)['error']), abs(check(FLOWS, .02, .01, 25)['error']))
    def test_single_payment_duration(self):
        r = check([(2.0, 100.0)], .02, .01, 100)
        self.assertAlmostEqual(r['spread_duration'], 2.0)
        self.assertAlmostEqual(r['spread_convexity'], 4.0)
    def test_invalid_flows(self):
        for flows in ([], [(0, 1)], [(1, -1)], [(2, 1), (1, 1)], [(1, float('nan'))]):
            with self.subTest(flows=flows), self.assertRaises(ValueError):
                price(flows, .02, .01)
    def test_invalid_shocks(self):
        for shock in (2001, float('inf'), float('nan'), True):
            with self.subTest(shock=shock), self.assertRaises(ValueError):
                check(FLOWS, .02, .01, shock)
    def test_invalid_yield(self):
        with self.assertRaises(ValueError):
            price(FLOWS, float('nan'), .01)

if __name__ == '__main__':
    unittest.main()
