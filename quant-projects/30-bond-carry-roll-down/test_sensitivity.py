"""Synthetic nonparallel yield-curve stress regression tests."""
import math
import unittest
from sensitivity import sensitivity_grid, shock_curve

C = {1.: .03, 2.: .035, 3.: .04, 5.: .045}
ZERO = {k: 0. for k in C}

class SensitivityTests(unittest.TestCase):
    def test_nonparallel_shock_interpolates(self):
        s = {1.: 0., 2.: .01, 3.: 0., 5.: 0.}
        row = sensitivity_grid(100, 3, [0.5], C, {"belly": s})[0]
        self.assertAlmostEqual(row['rolled'] + row['curve_shock_effect'], 100 * math.exp(-.0425 * 2.5))
    def test_zero_shock_reconciles(self):
        for row in sensitivity_grid(100, 3, [0.5, 1.0], C, {"base": ZERO}):
            self.assertAlmostEqual(row['curve_shock_effect'], 0)
            self.assertAlmostEqual(row['scenario_pnl'], row['carry'] + row['roll_down'])
    def test_all_scenarios_reconcile(self):
        scenarios = {"up": {k: .01 for k in C}, "down": {k: -.01 for k in C}}
        for row in sensitivity_grid(100, 3, [0.5, 1.0], C, scenarios):
            self.assertAlmostEqual(row['scenario_pnl'], row['carry'] + row['roll_down'] + row['curve_shock_effect'])
    def test_upward_shock_reduces_price(self):
        rows = sensitivity_grid(100, 3, [1.], C, {"up": {k: .01 for k in C}})
        self.assertLess(rows[0]['curve_shock_effect'], 0)
    def test_inputs_not_mutated(self):
        curve = C.copy()
        shock = ZERO.copy()
        sensitivity_grid(100, 3, [1.], curve, {"zero": shock})
        self.assertEqual(curve, C)
        self.assertEqual(shock, ZERO)
    def test_reject_missing_extra_nodes(self):
        for shocks in ({1.: 0.}, {**ZERO, 7.: 0.}):
            with self.assertRaises(ValueError): shock_curve(C, shocks)
    def test_reject_invalid_shocks(self):
        for value in (float('nan'), float('inf'), True, .21, -.21, '1'):
            with self.assertRaises(ValueError): shock_curve(C, {**ZERO, 2.: value})
    def test_reject_invalid_grids(self):
        for horizons, scenarios in (([], {'x': ZERO}), ([1., 1.], {'x': ZERO}), ([1.], {}), ([1.], {'': ZERO}), ([3.], {'x': ZERO})):
            with self.assertRaises(ValueError): sensitivity_grid(100, 3, horizons, C, scenarios)

if __name__ == '__main__': unittest.main()
