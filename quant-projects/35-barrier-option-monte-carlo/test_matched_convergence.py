"""Deterministic synthetic invariants for nested common-path barrier diagnostics."""
import math
import unittest
from matched_convergence import matched_grid

class MatchedGridTests(unittest.TestCase):
    def test_reproducible_sorted(self):
        self.assertEqual(matched_grid((12, 3, 6), pairs=20, seed=9),
                         matched_grid((3, 6, 12), pairs=20, seed=9))

    def test_discrete_pathwise_monotonicity_and_bridge_bounds(self):
        rows = matched_grid((3, 6, 12), pairs=60, seed=10)
        self.assertEqual([r["steps"] for r in rows], [3,6,12])
        self.assertTrue(all(a["discrete_call"] >= b["discrete_call"]-1e-12
                            for a,b in zip(rows,rows[1:])))
        for r in rows:
            self.assertGreaterEqual(r["continuous_bridge_call"], 0.)
            self.assertLessEqual(r["continuous_bridge_call"], r["discrete_call"]+1e-12)
            self.assertGreaterEqual(r["discretization_gap"], -1e-12)
            for key in ("discrete_se","continuous_se","paired_gap_se"):
                self.assertTrue(math.isfinite(r[key]))
                self.assertGreaterEqual(r[key], 0.)

    def test_zero_payoff_when_strike_above_barrier(self):
        for r in matched_grid((2,4), pairs=30, strike=140., barrier=130.):
            self.assertEqual(r["discrete_call"], 0.)
            self.assertEqual(r["continuous_bridge_call"], 0.)

    def test_reject_non_nested_and_invalid(self):
        for grids in ((), (3,4), (0,4), (True,4), (4,4), (10001,)):
            with self.subTest(grids=grids), self.assertRaises(ValueError):
                matched_grid(grids, pairs=20)

    def test_budget_and_model_guardrails(self):
        for kwargs in ({"pairs":1},{"pairs":100000,"steps":(252,)},
                       {"barrier":99.},{"vol":float("nan")},{"seed":True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                matched_grid(**kwargs)

if __name__ == "__main__":
    unittest.main()
