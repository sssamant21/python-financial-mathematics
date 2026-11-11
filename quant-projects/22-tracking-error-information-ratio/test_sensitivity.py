import math
import unittest
from sensitivity import aggregate_compound, sensitivity
from tracking_error import diagnostics

class SensitivityTests(unittest.TestCase):
    def setUp(self):
        self.p=[.01,-.02,.03,.02,-.01,.04,.01,-.02,.03,.01,-.01,.02]
        self.b=[0,.01,.02,.01,-.02,.02,0,-.01,.01,.02,0,.01]
    def test_compounding(self):
        self.assertAlmostEqual(aggregate_compound([.1,-.1,.02],3)[0],.0098)
    def test_identity_block(self):
        self.assertEqual(aggregate_compound(self.p,1),self.p)
    def test_monthly_matches_baseline(self):
        self.assertEqual(sensitivity(self.p,{"A":self.b})["A"][1],diagnostics(self.p,self.b))
    def test_quarterly_annualization(self):
        r=sensitivity(self.p,{"A":self.b})["A"][3]
        self.assertEqual(r["observations"],4)
        self.assertTrue(math.isfinite(r["tracking_error"]))
    def test_benchmark_sensitivity(self):
        r=sensitivity(self.p,{"A":self.b,"B":self.p})
        self.assertEqual(r["B"][1]["tracking_error"],0)
        self.assertNotEqual(r["A"][1]["tracking_error"],0)
    def test_no_future_leak(self):
        changed=self.p[:]
        changed[-1]=.9
        self.assertEqual(sensitivity(self.p[:9],{"A":self.b[:9]})["A"][3],
                         sensitivity(changed[:9],{"A":self.b[:9]})["A"][3])
        self.assertNotEqual(sensitivity(self.p,{"A":self.b})["A"][1],
                            sensitivity(changed,{"A":self.b})["A"][1])
    def test_incomplete_block(self):
        with self.assertRaises(ValueError): aggregate_compound(self.p[:-1],3)
    def test_too_few_aggregated(self):
        with self.assertRaises(ValueError): sensitivity(self.p[:6],{"A":self.b[:6]})
    def test_invalid_benchmark(self):
        with self.assertRaises(ValueError): sensitivity(self.p,{"A":self.b[:-1]})
    def test_invalid_frequency(self):
        with self.assertRaises(ValueError): sensitivity(self.p,{"A":self.b},10)
    def test_total_loss_compounds_to_total_loss(self):
        self.assertEqual(aggregate_compound([.05, -1.0, .25], 3), [-1.0])
    def test_boolean_block_rejected(self):
        with self.assertRaises(ValueError):
            aggregate_compound([.01, .02, .03], True)
    def test_benchmark_order_does_not_change_results(self):
        alternative = [x + .001 for x in self.b]
        first = sensitivity(self.p, {"A": self.b, "B": alternative})
        second = sensitivity(self.p, {"B": alternative, "A": self.b})
        self.assertEqual(first["A"], second["A"])
        self.assertEqual(first["B"], second["B"])
    def test_invalid_returns(self):
        with self.assertRaises(ValueError): aggregate_compound([0,float("nan"),0],3)

if __name__=="__main__":
    unittest.main()
