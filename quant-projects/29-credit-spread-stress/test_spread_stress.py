import math
import unittest

from spread_stress import Position, example_positions, scenario


class SpreadStressTests(unittest.TestCase):
    def setUp(self):
        self.positions = example_positions()

    def test_zero_shock(self):
        self.assertEqual(scenario(self.positions, 0)["pnl"], 0)

    def test_widening_loses_without_convexity(self):
        self.assertAlmostEqual(scenario([Position("x", 10000, 5)], 100)["pnl"], -500)

    def test_tightening_gains_without_convexity(self):
        self.assertAlmostEqual(scenario([Position("x", 10000, 5)], -100)["pnl"], 500)

    def test_dv01_units(self):
        self.assertAlmostEqual(scenario([Position("x", 10000, 5)], 1)["spread_dv01"], 5)

    def test_convexity_offset(self):
        a = scenario([Position("x", 10000, 5, 10)], 100)["pnl"]
        self.assertAlmostEqual(a, -495)

    def test_attribution_reconciles(self):
        r = scenario(self.positions, 100)
        self.assertAlmostEqual(sum(r["attribution"].values()), r["pnl"])

    def test_loss_sign(self):
        r = scenario(self.positions, 100)
        self.assertAlmostEqual(r["loss"], -r["pnl"])

    def test_deterministic(self):
        self.assertEqual(scenario(self.positions, 50), scenario(self.positions, 50))

    def test_empty(self):
        with self.assertRaises(ValueError):
            scenario([], 10)

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            scenario([Position("x", 1, 1), Position("x", 2, 2)], 10)

    def test_invalid_values(self):
        for p in (Position("x", 0, 1), Position("x", 1, -1), Position("x", 1, 1, -1), Position("x", math.nan, 1)):
            with self.subTest(p=p), self.assertRaises(ValueError):
                scenario([p], 10)

    def test_invalid_shock(self):
        for shock in (math.inf, math.nan, 2001, True):
            with self.subTest(shock=shock), self.assertRaises(ValueError):
                scenario(self.positions, shock)


if __name__ == "__main__":
    unittest.main()
