import math
import unittest
from iv import price
from sensitivity import grid, quote_interval, vega


class SensitivityTests(unittest.TestCase):
    def test_vega_finite_difference(self):
        h = 1e-5
        numerical = (price(100, 100, 1, .02, .25 + h) - price(100, 100, 1, .02, .25 - h)) / (2*h)
        self.assertAlmostEqual(vega(100, 100, 1, .02, .25), numerical, places=5)

    def test_bid_ask_order(self):
        r = quote_interval(100, 100, 1, .02, .25)
        self.assertLess(r['iv_bid'], .25)
        self.assertGreater(r['iv_ask'], .25)
        self.assertGreater(r['iv_width'], 0)

    def test_spread_monotonicity(self):
        narrow = quote_interval(100, 100, 1, .02, .25, .02)
        wide = quote_interval(100, 100, 1, .02, .25, .1)
        self.assertGreater(wide['iv_width'], narrow['iv_width'])

    def test_put_call_vega_symmetry(self):
        c = quote_interval(100, 100, 1, .02, .25, kind='call')
        p = quote_interval(100, 100, 1, .02, .25, kind='put')
        self.assertAlmostEqual(c['iv_width'], p['iv_width'], places=7)

    def test_grid_deterministic(self):
        self.assertEqual(grid(), grid())
        self.assertEqual(len(grid()), 9)
        self.assertTrue(all(r['status'] in ('ok', 'unavailable') for r in grid()))

    def test_bad_spreads_and_inputs(self):
        for spread in (0, -1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                quote_interval(100, 100, 1, .02, .25, spread)
        with self.assertRaises(ValueError):
            vega(100, 100, 0, .02, .25)
        with self.assertRaises(ValueError):
            grid(kind='binary')

    def test_invalid_quote_flagged(self):
        rows = grid(half_spread=10)
        self.assertTrue(any(r['status'] == 'unavailable' for r in rows))

    def test_local_linear_approximation(self):
        r = quote_interval(100, 100, 1, .02, .25, .001)
        self.assertAlmostEqual(r['iv_width'], r['linear_width'], delta=1e-5)


if __name__ == '__main__':
    unittest.main()
