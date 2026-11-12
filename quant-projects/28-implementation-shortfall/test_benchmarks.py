import unittest
from benchmarks import Bar, compare_vwap

class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.rows = [Bar(100, 100, 101, 5), Bar(102, 100, 103, 5)]
    def test_market_and_fill_vwap(self):
        x = compare_vwap(100, 10, self.rows)
        self.assertAlmostEqual(x['market_vwap'], 101)
        self.assertAlmostEqual(x['execution_vwap'], 102)
        self.assertAlmostEqual(x['vwap_slippage_bps'], 10000/101)
    def test_sell_sign(self):
        self.assertLess(compare_vwap(100, 10, self.rows, side='sell')['vwap_slippage_bps'], 0)
    def test_fees(self):
        self.assertAlmostEqual(compare_vwap(100, 10, self.rows, fee_bps=10)['fees'], 1.02)
    def test_partial(self):
        x = compare_vwap(100, 20, self.rows)
        self.assertEqual(x['unfilled'], 10)
        self.assertEqual(x['fill_rate'], .5)
    def test_zero_fill(self):
        x = compare_vwap(100, 10, [Bar(100, 100, 100, 0)])
        self.assertIsNone(x['execution_vwap'])
        self.assertIsNone(x['vwap_slippage_bps'])
    def test_participation(self):
        with self.assertRaises(ValueError): compare_vwap(100, 10, self.rows, max_participation=.01)
    def test_overfill(self):
        with self.assertRaises(ValueError): compare_vwap(100, 1, self.rows)
    def test_nan(self):
        with self.assertRaises(ValueError): compare_vwap(float('nan'), 10, self.rows)
    def test_bad_side(self):
        with self.assertRaises(ValueError): compare_vwap(100, 10, self.rows, side='hold')
    def test_empty(self):
        with self.assertRaises(ValueError): compare_vwap(100, 10, [])
    def test_bad_bar(self):
        with self.assertRaises(ValueError): compare_vwap(100, 10, [(100,100,101,5)])
    def test_bad_fee(self):
        with self.assertRaises(ValueError): compare_vwap(100, 10, self.rows, fee_bps=-1)

if __name__ == '__main__': unittest.main()
