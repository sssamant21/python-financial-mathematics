"""Synthetic independent coupon reconciliation and discount-factor sensitivity."""
import unittest
from decimal import Decimal
from swap import value_swap


def explicit_legs(notional, fixed_rate, accruals, discounts):
    """Project forward coupons from adjacent discounts; D(0)=1."""
    prev = Decimal('1')
    floating = fixed = Decimal('0')
    n, k = Decimal(str(notional)), Decimal(str(fixed_rate))
    for a, d in zip(accruals, discounts):
        alpha, end = Decimal(str(a)), Decimal(str(d))
        forward = (prev / end - 1) / alpha
        floating += n * alpha * forward * end
        fixed += n * k * alpha * end
        prev = end
    return float(floating), float(fixed)


class CurveReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.a = [0.5] * 4
        self.d = [0.98, 0.96, 0.94, 0.92]

    def test_period_by_period_cashflow_reconciliation(self):
        floating, fixed = explicit_legs(1_000_000, 0.04, self.a, self.d)
        actual = value_swap(1_000_000, 0.04, self.a, self.d)
        self.assertAlmostEqual(actual['floating_pv'], floating, places=7)
        self.assertAlmostEqual(actual['fixed_pv'], fixed, places=7)
        self.assertAlmostEqual(actual['net_pv'], floating-fixed, places=7)

    def test_negative_forward_curve(self):
        d = [1.01, 1.02, 1.03]
        f, k = explicit_legs(1_000_000, -0.02, [0.5]*3, d)
        result = value_swap(1_000_000, -0.02, [0.5]*3, d)
        self.assertAlmostEqual(result['floating_pv'], f, places=7)
        self.assertAlmostEqual(result['fixed_pv'], k, places=7)

    def test_final_discount_factor_bump_identity(self):
        base = value_swap(1_000_000, .04, self.a, self.d)
        bumped = self.d.copy()
        bumped[-1] += 0.0001
        shifted = value_swap(1_000_000, .04, self.a, bumped)
        expected_change = -1_000_000 * (1 + .04 * self.a[-1]) * .0001
        self.assertAlmostEqual(shifted['net_pv']-base['net_pv'], expected_change, places=7)

    def test_interior_discount_factor_bump(self):
        base = value_swap(1_000_000, .04, self.a, self.d)
        bumped = self.d.copy()
        bumped[1] += .0001
        shifted = value_swap(1_000_000, .04, self.a, bumped)
        self.assertAlmostEqual(shifted['floating_pv'], base['floating_pv'], places=7)
        self.assertAlmostEqual(shifted['net_pv']-base['net_pv'], -1_000_000*.04*.5*.0001, places=7)

    def test_par_coupon_matches_explicit_schedule(self):
        f, _ = explicit_legs(1_000_000, 0, self.a, self.d)
        denominator = sum(1_000_000*a*d for a,d in zip(self.a,self.d))
        par = f / denominator
        self.assertAlmostEqual(value_swap(1_000_000, par, self.a, self.d)['net_pv'], 0, places=7)

    def test_nonuniform_accruals(self):
        a, d = [.25, .75, .5], [.99, .955, .925]
        f, k = explicit_legs(250_000, .035, a, d)
        result = value_swap(250_000, .035, a, d)
        self.assertAlmostEqual(result['net_pv'], f-k, places=7)


    def test_notional_linearity_and_payer_receiver_sign(self):
        base = value_swap(250_000, .035, self.a, self.d)
        scaled = value_swap(1_000_000, .035, self.a, self.d)
        receiver = value_swap(1_000_000, .035, self.a, self.d, pay_fixed=False)
        self.assertAlmostEqual(scaled['net_pv'], 4 * base['net_pv'], places=7)
        self.assertAlmostEqual(receiver['net_pv'], -scaled['net_pv'], places=7)
        self.assertAlmostEqual(scaled['par_rate'], base['par_rate'], places=12)

    def test_extreme_finite_input_overflow_rejected(self):
        # Finite inputs can still overflow in intermediate PV arithmetic.
        with self.assertRaises(ValueError):
            value_swap(1e308, 1e308, [0.5], [0.98])


if __name__ == '__main__':
    unittest.main()
