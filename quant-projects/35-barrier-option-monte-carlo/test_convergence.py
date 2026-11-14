"""Synthetic grid-sensitivity checks, not an independent barrier benchmark."""
import math
import unittest
from convergence import convergence_table

class ConvergenceTests(unittest.TestCase):
    def test_reproducible_sorted(self):
        a = convergence_table((24, 6), pairs=40, seed=11)
        self.assertEqual(a, convergence_table((6, 24), pairs=40, seed=11))
        self.assertEqual([x["steps"] for x in a], [6, 24])

    def test_pathwise_price_bounds(self):
        for r in convergence_table((4, 12, 24), pairs=60):
            self.assertGreaterEqual(r["continuous_bridge_call"], 0)
            self.assertLessEqual(r["continuous_bridge_call"], r["discrete_call"]+1e-12)
            self.assertGreaterEqual(r["discretization_gap"], -1e-12)
            for key in ("continuous_se","discrete_se","paired_gap_se"):
                self.assertTrue(math.isfinite(r[key]))
                self.assertGreaterEqual(r[key], 0)

    def test_zero_payoff_when_strike_above_barrier(self):
        for r in convergence_table((4, 12), pairs=50, strike=140., barrier=130.):
            self.assertEqual(r["continuous_bridge_call"], 0)
            self.assertEqual(r["discrete_call"], 0)

    def test_invalid_grids(self):
        for grid in ((), (0,), (1,1), (True,), (10001,), tuple(range(13))):
            with self.subTest(grid=grid), self.assertRaises(ValueError):
                convergence_table(grid, pairs=20)

    def test_invalid_simulation_propagates(self):
        with self.assertRaises(ValueError):
            convergence_table((12,), pairs=1)

if __name__ == "__main__":
    unittest.main()
