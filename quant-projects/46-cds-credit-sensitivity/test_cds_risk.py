import unittest
from cds_risk import legs, pv, sensitivities


class TestCDSRisk(unittest.TestCase):
    def test_par_pv_zero(self):
        a, p = legs(.02)
        self.assertAlmostEqual(pv(.02, p/a), 0, places=8)

    def test_zero_hazard_no_protection(self):
        a, p = legs(0)
        self.assertEqual(p, 0)
        self.assertGreater(a, 0)

    def test_coupon_dv01_exact(self):
        x = sensitivities()
        a, _ = legs(.02)
        self.assertAlmostEqual(x['coupon_dv01'], -100*a, places=8)
        self.assertAlmostEqual(pv(.02, .0121)-pv(.02, .012), x['coupon_dv01'], places=7)

    def test_hazard_increase_raises_protection_buyer_pv(self):
        self.assertGreater(sensitivities()['hazard01'], 0)

    def test_zero_hazard_forward_difference(self):
        self.assertEqual(sensitivities(hazard=0)['hazard_difference'], 'forward')

    def test_recovery_reduces_protection(self):
        self.assertLess(legs(.02, recovery=.8)[1], legs(.02, recovery=.2)[1])

    def test_invalid_inputs(self):
        for kw in ({'hazard': True}, {'hazard': float('nan')}, {'maturity': .3},
                   {'frequency': True}, {'recovery': 1}, {'rate': float('inf')}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                legs(**({'hazard': .02} | kw))
        for kw in ({'coupon': True}, {'notional': -1}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                pv(.02, **({'coupon': .012} | kw))
        with self.assertRaises(ValueError):
            sensitivities(bump_bp=0)


if __name__ == '__main__':
    unittest.main()
