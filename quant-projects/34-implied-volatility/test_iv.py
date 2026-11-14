import math
import unittest
from iv import price, implied_vol

class Tests(unittest.TestCase):
    def test_roundtrip(self):
        for kind in ("call", "put"):
            for vol in (0.1, 0.25, 0.6):
                q = price(100, 105, 1, 0.02, vol, kind)
                self.assertAlmostEqual(implied_vol(q, 100, 105, 1, 0.02, kind), vol, places=7)
    def test_parity(self):
        self.assertAlmostEqual(price(100,105,1,.02,.25)-price(100,105,1,.02,.25,"put"),100-105*math.exp(-.02),places=10)
    def test_zero_boundary(self):
        self.assertEqual(implied_vol(price(100,105,1,.02,0),100,105,1,.02),0)
    def test_monotonicity(self):
        self.assertLess(price(100,100,1,0,.1),price(100,100,1,0,.4))
    def test_bad_quote(self):
        with self.assertRaises(ValueError):
            implied_vol(150,100,100,1,0)
    def test_invalid_inputs(self):
        for v in (float("nan"),float("inf"),-1):
            with self.assertRaises(ValueError):
                price(100,100,1,0,v)
        with self.assertRaises(ValueError):
            implied_vol(10,100,100,1,0,tolerance=0)
    def test_nonconvergence(self):
        with self.assertRaises(RuntimeError):
            implied_vol(price(100,100,1,0,.2),100,100,1,0,iterations=1)

if __name__ == "__main__":
    unittest.main()
