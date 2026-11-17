import math
import unittest
from cds import legs

class CDSTests(unittest.TestCase):
    def test_zero_hazard_zero_protection(self):
        result=legs(hazard=0)
        self.assertEqual(result["protection_leg"],0)
        self.assertEqual(result["par_spread"],0)
        self.assertEqual(result["terminal_survival"],1)
    def test_full_recovery_zero_protection(self):
        self.assertEqual(legs(recovery=1)["par_spread"],0)
    def test_higher_hazard_higher_spread(self):
        self.assertGreater(legs(hazard=.05)["par_spread"],legs(hazard=.01)["par_spread"])
    def test_lower_recovery_higher_spread(self):
        self.assertGreater(legs(recovery=.2)["par_spread"],legs(recovery=.6)["par_spread"])
    def test_notional_scales_protection_not_spread(self):
        a,b=legs(notional=100),legs(notional=200)
        self.assertAlmostEqual(b["protection_leg"],2*a["protection_leg"])
        self.assertEqual(a["par_spread"],b["par_spread"])
    def test_survival_identity(self):
        x=legs(hazard=.03,years=3)
        self.assertAlmostEqual(x["terminal_survival"],math.exp(-.09))
    def test_par_leg_reconciliation(self):
        x=legs()
        self.assertAlmostEqual(x["par_spread"]*1_000_000*x["premium_annuity_per_notional"],x["protection_leg"])
    def test_hazard_approximation_small(self):
        x=legs(hazard=1e-5,rate=0)
        self.assertAlmostEqual(x["par_spread"]/(.6e-5),1,delta=.002)
    def test_frequency_sensitivity(self):
        self.assertNotEqual(legs(payments_per_year=1)["par_spread"],legs(payments_per_year=4)["par_spread"])
    def test_bad_inputs(self):
        for kwargs in ({"hazard":-1},{"hazard":float("nan")},{"recovery":1.1},
                       {"years":0},{"notional":0},{"rate":float("inf")},
                       {"payments_per_year":3},{"payments_per_year":True},
                       {"years":1.1,"payments_per_year":4}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                legs(**kwargs)

if __name__=="__main__":
    unittest.main()
