import math
import unittest
from grid_refinement import path, hedge, experiment

class GridTests(unittest.TestCase):
    def test_seeded(self):
        self.assertEqual(path(42),path(42))
        self.assertNotEqual(path(42),path(43))
    def test_matched_terminal(self):
        values=path(42)
        self.assertEqual(len({hedge(values,g)["terminal"] for g in (13,26,52,104)}),1)
    def test_fee_identity_zero_rate(self):
        values=path(42,rate=0)
        for g in (13,26,52,104):
            a=hedge(values,g,0,rate=0)
            b=hedge(values,g,5,rate=0)
            self.assertAlmostEqual(a["pnl"]-b["pnl"],b["fees"],places=9)
            self.assertAlmostEqual(b["fees"],b["turnover"]*5/10000,places=9)
    def test_financed_fees(self):
        values=path(42)
        for g in (13,26,52,104):
            a=hedge(values,g,0)
            b=hedge(values,g,5)
            self.assertGreaterEqual(a["pnl"]-b["pnl"]+1e-10,b["fees"])
    def test_reproducibility(self):
        self.assertEqual(experiment(paths=3),experiment(paths=3))
    def test_grid_rows(self):
        rows=experiment(paths=3)
        self.assertEqual([r["hedge_steps"] for r in rows],[13,26,52,104])
        self.assertTrue(all(math.isfinite(r["rmse_pnl"]) and r["mean_turnover"]>0 for r in rows))
    def test_zero_cost(self):
        self.assertTrue(all(r["mean_financed_cost_drag"]==0 for r in experiment(paths=3,cost_bps=0)))
    def test_invalid(self):
        for kw in ({"paths":1},{"grids":(13,14)},{"grids":(26,13)},{"fine_steps":1},{"cost_bps":-1},{"seed":-1}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):experiment(**kw)
        with self.assertRaises(ValueError):hedge([100.,101.,102.],3)
        with self.assertRaises(ValueError):path(-1)

if __name__=="__main__": unittest.main()
