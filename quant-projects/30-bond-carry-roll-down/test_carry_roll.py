"""Deterministic no-market-data regression tests."""
import math
import unittest
from carry_roll import price, carry_roll

C = {1.0: .03, 2.0: .035, 3.0: .04, 5.0: .045}

class CarryRollTests(unittest.TestCase):
    def test_node_price(self):
        self.assertAlmostEqual(price(100, 2, C), 100 * math.exp(-.07))
    def test_interpolation(self):
        self.assertAlmostEqual(price(100, 2.5, C), 100 * math.exp(-.0375 * 2.5))
    def test_accounting_identity(self):
        r = carry_roll(100, 3, 1, C)
        self.assertAlmostEqual(r["carry"] + r["roll_down"], r["rolled"] - r["start"])
        self.assertAlmostEqual(r["carry"] + r["roll_down"] + r["curve_shock_effect"], r["scenario_pnl"])
    def test_flat_curve_has_no_roll_down(self):
        r = carry_roll(100, 3, 1, {1: .04, 2: .04, 3: .04})
        self.assertAlmostEqual(r["roll_down"], 0)
    def test_upward_shift_hurts(self):
        r = carry_roll(100, 3, 1, C, {k: v + .01 for k, v in C.items()})
        self.assertLess(r["curve_shock_effect"], 0)
    def test_guardrails(self):
        for args in [(0, 2, C), (100, .5, C), (100, 6, C), (100, 2, {1: .03}), (100, 2, {1: float("nan"), 2: .04})]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                price(*args)
        for h in (0, 3, -1, float("nan"), True):
            with self.subTest(h=h), self.assertRaises(ValueError):
                carry_roll(100, 3, h, C)
    def test_no_input_mutation(self):
        original = C.copy()
        carry_roll(100, 3, 1, C)
        self.assertEqual(C, original)

if __name__ == "__main__":
    unittest.main()
