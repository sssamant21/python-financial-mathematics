import math
import unittest
from hedge import call_price_delta, simulate, experiment

class HedgeTests(unittest.TestCase):
    def test_black_scholes(self):
        p,d=call_price_delta(100,100,1,.05,.2)
        self.assertAlmostEqual(p,10.4505835722,places=8)
        self.assertAlmostEqual(d,.6368306512,places=8)
    def test_expiry(self):
        self.assertEqual(call_price_delta(120,100,0,0,.2),(20,1))
        self.assertEqual(call_price_delta(80,100,0,0,.2),(0,0))
    def test_repeatability(self):
        self.assertEqual(simulate(seed=7),simulate(seed=7))
    def test_cost_drag(self):
        a=simulate(seed=7,cost_bps=0)
        b=simulate(seed=7,cost_bps=10)
        self.assertEqual(a["terminal_spot"],b["terminal_spot"])
        self.assertAlmostEqual(a["turnover_notional"],b["turnover_notional"])
        self.assertGreater(b["transaction_cost"],0)
        self.assertLess(b["hedge_pnl"],a["hedge_pnl"])
    def test_frequency(self):
        self.assertNotEqual(simulate(seed=7,rebalance_every=1)["hedge_pnl"],simulate(seed=7,rebalance_every=13)["hedge_pnl"])
    def test_scenarios(self):
        rows=experiment(range(4),(1,4),(0,5))
        self.assertEqual(len(rows),4)
        self.assertTrue(all(math.isfinite(r["rmse_pnl"]) for r in rows))
    def test_guardrails(self):
        for kwargs in ({"steps":1},{"rebalance_every":0},{"cost_bps":-1},{"maturity":0},{"volatility":0},{"spot":float("nan")},{"steps":5001},{"seed":2.5}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError): simulate(**kwargs)

if __name__=="__main__": unittest.main()
