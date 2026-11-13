"""Deterministic synthetic tests for PDE grid sensitivity."""
import math
import unittest
from grid_sensitivity import GRIDS, black_scholes_european_put, grid_sensitivity

class GridSensitivityTests(unittest.TestCase):
    def test_analytic_reference(self):
        self.assertAlmostEqual(black_scholes_european_put(), 5.5735260223, delta=1e-7)

    def test_preset_grid_order_and_finiteness(self):
        rows = grid_sensitivity()
        self.assertEqual([(r["spot_steps"], r["time_steps"]) for r in rows], list(GRIDS))
        self.assertTrue(all(math.isfinite(r["american"]) for r in rows))

    def test_american_premium_nonnegative(self):
        self.assertTrue(all(r["exercise_premium"] >= -1e-9 for r in grid_sensitivity()))

    def test_european_reference_coarse_tolerance(self):
        self.assertTrue(all(r["european_abs_error"] < 0.5 for r in grid_sensitivity()))

    def test_invalid_reference_inputs(self):
        for args in ({"spot": float("nan")}, {"strike": 0}, {"volatility": -1}, {"years": 0}):
            with self.subTest(args=args), self.assertRaises(ValueError):
                black_scholes_european_put(**args)

    def test_invalid_grids(self):
        for grids in ([], [(40,)], [(40, 2000, 1)]):
            with self.subTest(grids=grids), self.assertRaises(ValueError):
                grid_sensitivity(grids)

if __name__ == "__main__":
    unittest.main()
