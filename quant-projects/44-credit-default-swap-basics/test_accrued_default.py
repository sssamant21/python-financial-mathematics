import math
import unittest
from accrued_default import accrued_legs
from cds import legs

class AccruedDefaultTests(unittest.TestCase):
    def test_zero_hazard(self):
        x = accrued_legs(hazard=0)
        self.assertEqual(x["accrual_annuity_per_notional"], 0)
        self.assertEqual(x["protection_leg"], 0)
        self.assertEqual(x["par_spread"], 0)

    def test_full_recovery(self):
        self.assertEqual(accrued_legs(recovery=1)["par_spread"], 0)

    def test_positive_accrual(self):
        x = accrued_legs()
        self.assertGreater(x["accrual_annuity_per_notional"], 0)
        self.assertAlmostEqual(x["total_annuity_per_notional"],
            x["scheduled_annuity_per_notional"]+x["accrual_annuity_per_notional"])

    def test_independent_midpoint_quadrature(self):
        # Coupon-date survival premiums are discrete; therefore h*(1-R)
        # is NOT an exact par-spread identity with this payment convention.
        for h, r, freq in [(0.02, 0.03, 4), (0.05, -0.02, 12),
                           (0.000001, 0, 1), (0.2, 0.1, 2)]:
            with self.subTest(h=h, r=r, freq=freq):
                years, recovery, intervals, subdivisions = 5, 0.4, 5*freq, 2000
                dt = 1/freq
                scheduled = sum(dt*math.exp(-(h+r)*i*dt)
                                for i in range(1, intervals+1))
                accrued = 0.0
                protection_unit = 0.0
                for i in range(intervals):
                    for j in range(subdivisions):
                        u = (j+0.5)*dt/subdivisions
                        discounted_default = h*math.exp(-(h+r)*(i*dt+u))*dt/subdivisions
                        accrued += u*discounted_default
                        protection_unit += discounted_default
                expected = (1-recovery)*protection_unit/(scheduled+accrued)
                x = accrued_legs(hazard=h, rate=r, payments_per_year=freq)
                self.assertAlmostEqual(x["par_spread"], expected, delta=2e-9)

    def test_reconcile_protection(self):
        x=accrued_legs()
        self.assertAlmostEqual(x["par_spread"]*1_000_000*
            x["total_annuity_per_notional"], x["protection_leg"], places=7)

    def test_notional_invariance(self):
        a=accrued_legs(notional=100)
        b=accrued_legs(notional=200)
        self.assertEqual(a["par_spread"],b["par_spread"])
        self.assertAlmostEqual(2*a["protection_leg"],b["protection_leg"])

    def test_analytic_default_integral(self):
        h,r,t=.04,.02,5
        x=accrued_legs(hazard=h,rate=r,years=t)
        expected=1_000_000*.6*h*(-math.expm1(-(h+r)*t))/(h+r)
        self.assertAlmostEqual(x["protection_leg"],expected)

    def test_comparison_defined(self):
        x=accrued_legs()
        self.assertAlmostEqual(x["spread_change_bp"],
            x["par_spread_bp"]-legs()["par_spread_bp"])

    def test_invalid_inputs_rejected(self):
        for kw in ({"hazard":float("nan")},{"years":1.1},
                   {"payments_per_year":3},{"notional":-1}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):
                accrued_legs(**kw)

if __name__=="__main__":
    unittest.main()
