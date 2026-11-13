import math
import unittest
from sensitivity import sensitivity, summarize

class SensitivityTests(unittest.TestCase):
    def test_constant_values(self):
        s=summarize([2.0,2.0,2.0])
        self.assertEqual(s["mean_pnl"],2.0)
        self.assertEqual(s["mc_se_mean"],0.0)
        self.assertEqual(s["rmse_pnl"],2.0)
    def test_known_standard_error(self):
        s=summarize([-1.0,1.0])
        self.assertAlmostEqual(s["mc_se_mean"],1.0)
        self.assertAlmostEqual(s["rmse_pnl"],1.0)
    def test_reproducibility(self):
        kw=dict(path_counts=(2,4),volatilities=(.2,),frequencies=(1,4))
        self.assertEqual(sensitivity(**kw),sensitivity(**kw))
    def test_nested_prefixes(self):
        kw=dict(volatilities=(.2,),frequencies=(4,))
        self.assertEqual(sensitivity(path_counts=(2,),**kw)[0],
                         sensitivity(path_counts=(2,5),**kw)[0])
    def test_cost_drag_paired(self):
        rows=sensitivity(path_counts=(3,),volatilities=(.1,.4),frequencies=(1,13))
        self.assertEqual(len(rows),4)
        self.assertTrue(all(r["mean_cost_drag"]>0 for r in rows))
        self.assertTrue(all(math.isfinite(r["mc_ci95_low"]) for r in rows))
    def test_zero_cost(self):
        row=sensitivity(path_counts=(3,),volatilities=(.2,),frequencies=(1,),cost_bps=0)[0]
        self.assertEqual(row["mean_cost_drag"],0.0)
        self.assertEqual(row["mc_se_cost_drag"],0.0)
    def test_invalid_configurations(self):
        for kw in ({"path_counts":()},{"path_counts":(1,)},{"path_counts":(4,2)},
                   {"path_counts":(2,2)},{"volatilities":(0,)},
                   {"volatilities":(float("nan"),)},{"frequencies":(0,)},
                   {"frequencies":(53,)},{"cost_bps":-1},{"base_seed":1.5}):
            with self.subTest(kw=kw),self.assertRaises(ValueError): sensitivity(**kw)
    def test_bad_samples(self):
        for vals in ([],[1],[1,float("inf")]):
            with self.assertRaises(ValueError): summarize(vals)

    def test_pathwise_cost_accounting_zero_rate(self):
        from hedge import simulate
        for seed in (2026, 2027, 2040):
            for frequency in (1, 4, 13):
                free = simulate(seed=seed, rebalance_every=frequency, cost_bps=0, rate=0)
                paid = simulate(seed=seed, rebalance_every=frequency, cost_bps=5, rate=0)
                self.assertEqual(free["terminal_spot"], paid["terminal_spot"])
                self.assertAlmostEqual(free["hedge_pnl"] - paid["hedge_pnl"],
                                       paid["transaction_cost"], places=9)
                self.assertAlmostEqual(paid["transaction_cost"],
                                       paid["turnover_notional"] * 5 / 10000, places=9)

    def test_positive_rate_finances_early_fees(self):
        from hedge import simulate
        for frequency in (1, 4, 13):
            free = simulate(seed=2026, rebalance_every=frequency, cost_bps=0, rate=0.02)
            paid = simulate(seed=2026, rebalance_every=frequency, cost_bps=5, rate=0.02)
            self.assertGreaterEqual(free["hedge_pnl"] - paid["hedge_pnl"] + 1e-10,
                                    paid["transaction_cost"])
            self.assertEqual(free["terminal_spot"], paid["terminal_spot"])

if __name__=="__main__": unittest.main()
