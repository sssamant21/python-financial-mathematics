import unittest
from execution import Slice, shortfall

class ShortfallTests(unittest.TestCase):
    def test_buy(self):
        x = shortfall(100, 10, [Slice(101, 10, 100)], fee_bps=10)
        self.assertAlmostEqual(x["total_cost"], 11.01)
        self.assertAlmostEqual(x["shortfall_bps"], 110.1)
    def test_sell(self):
        self.assertAlmostEqual(shortfall(100, 10, [Slice(99, 10, 100)], side="sell")["total_cost"], 10)
    def test_improvement(self):
        self.assertLess(shortfall(100, 10, [Slice(99, 10, 100)])["total_cost"], 0)
    def test_unfilled(self):
        x = shortfall(100, 10, [Slice(100, 4, 100)], terminal_price=105)
        self.assertEqual((x["unfilled"], x["opportunity_cost"]), (6, 30))
    def test_zero_fill(self):
        self.assertEqual(shortfall(100, 10, [Slice(100, 0, 100)])["total_cost"], 0)
    def test_participation(self):
        with self.assertRaises(ValueError):
            shortfall(100, 10, [Slice(100, 6, 100)], max_participation=.05)
    def test_overfill(self):
        with self.assertRaises(ValueError):
            shortfall(100, 5, [Slice(100, 6, 100)])
    def test_side(self):
        with self.assertRaises(ValueError):
            shortfall(100, 5, [Slice(100, 5, 100)], side="hold")
    def test_nan(self):
        with self.assertRaises(ValueError):
            shortfall(float("nan"), 5, [Slice(100, 5, 100)])
    def test_fee(self):
        with self.assertRaises(ValueError):
            shortfall(100, 5, [Slice(100, 5, 100)], fee_bps=-1)
    def test_terminal(self):
        with self.assertRaises(ValueError):
            shortfall(100, 5, [Slice(100, 5, 100)], terminal_price=float("inf"))
    def test_empty(self):
        with self.assertRaises(ValueError):
            shortfall(100, 5, [])
    def test_row(self):
        with self.assertRaises(ValueError):
            shortfall(100, 5, [(100, 5, 100)])

if __name__ == "__main__":
    unittest.main()
