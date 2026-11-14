"""Deterministic synthetic checks; not market certification."""
import math
import unittest
from bridge import bridge_survival, compare_bridge

class BridgeTests(unittest.TestCase):
    def test_touch(self):
        self.assertEqual(bridge_survival(100,130,130,0.2,0.1), 0)
        self.assertEqual(bridge_survival(131,100,130,0.2,0.1), 0)
    def test_formula(self):
        expected = 1-math.exp(-2*math.log(130/100)*math.log(130/110)/(0.2**2*0.1))
        self.assertAlmostEqual(bridge_survival(100,110,130,0.2,0.1), expected)
    def test_barrier_monotonicity(self):
        self.assertLessEqual(bridge_survival(100,110,120,0.2,0.1),
                             bridge_survival(100,110,150,0.2,0.1))
    def test_seed_and_bounds(self):
        x = compare_bridge(pairs=100,steps=12,seed=9)
        self.assertEqual(x,compare_bridge(pairs=100,steps=12,seed=9))
        self.assertLessEqual(0,x["continuous_bridge_call"])
        self.assertLessEqual(x["continuous_bridge_call"],x["discrete_call"]+1e-12)
        self.assertLessEqual(x["discrete_call"],x["vanilla_call"]+1e-12)
    def test_high_barrier(self):
        x = compare_bridge(barrier=1e9,pairs=60,steps=12)
        self.assertAlmostEqual(x["continuous_bridge_call"],x["vanilla_call"],places=10)
        self.assertEqual(x["discrete_call"],x["vanilla_call"])
    def test_invalid(self):
        for kw in ({"pairs":1},{"steps":0},{"seed":True},{"barrier":100},
                   {"vol":float("nan")},{"rate":1e308}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):
                compare_bridge(**kw)
        with self.assertRaises(ValueError):
            bridge_survival(0,100,130,0.2,0.1)

if __name__ == "__main__":
    unittest.main()
