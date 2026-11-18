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


class TestCDSRiskAnalyticalRegression(unittest.TestCase):
    def test_flat_hazard_par_spread_closed_form(self):
        import math
        for h in (0.0, 0.01, 0.2):
            for f in (1, 4, 12):
                with self.subTest(h=h, frequency=f):
                    annuity, protection = legs(h, maturity=2, frequency=f, rate=0.03, recovery=0.4)
                    self.assertAlmostEqual(protection / annuity, 0.6 * f * math.expm1(h / f), places=11)

    def test_notional_scaling(self):
        a = sensitivities(notional=100_000)
        b = sensitivities(notional=1_000_000)
        for key in ('pv', 'coupon_dv01', 'hazard01'):
            self.assertAlmostEqual(b[key], 10 * a[key], places=7)
        self.assertAlmostEqual(a['par_spread_bp'], b['par_spread_bp'])

    def test_upper_hazard_bump_guardrail(self):
        with self.assertRaisesRegex(ValueError, 'hazard bump exceeds'):
            sensitivities(hazard=5, bump_bp=1)

    def test_forward_hazard_difference_at_zero(self):
        bump_bp = 2
        bump = bump_bp / 10000
        x = sensitivities(hazard=0, bump_bp=bump_bp)
        self.assertEqual(x['hazard_difference'], 'forward')
        self.assertAlmostEqual(x['hazard01'], pv(bump, .012) - pv(0, .012), places=8)


    def test_coupon_linearity_and_exact_dv01(self):
        for hazard in (0.0, 0.01, 0.15):
            with self.subTest(hazard=hazard):
                a, _ = legs(hazard, maturity=3, frequency=4)
                base = pv(hazard, 0.01, maturity=3, frequency=4)
                bumped = pv(hazard, 0.0101, maturity=3, frequency=4)
                self.assertAlmostEqual(bumped - base, -1_000_000 * a * 0.0001, places=7)

    def test_zero_hazard_coupon_pv_identity(self):
        a, protection = legs(0.0, maturity=2, rate=0.03, frequency=4)
        self.assertEqual(protection, 0.0)
        self.assertAlmostEqual(pv(0.0, 0.015, maturity=2, rate=0.03),
                               -1_000_000 * 0.015 * a, places=8)


if __name__ == '__main__':
    unittest.main()
