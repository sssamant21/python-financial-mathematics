"""Independent cash-flow and par-quote sensitivity checks for Project 41."""
import math
import unittest
from curve import bootstrap, forwards, reprice


def floating_coupons(discounts):
    """Discounted one-year forward coupons, each on unit notional."""
    previous = 1.0
    values = []
    for d, forward in zip(discounts, forwards(discounts)):
        values.append(d * forward)
        previous = d
    return tuple(values)


class ReconciliationTests(unittest.TestCase):
    def test_each_coupon_matches_discount_difference(self):
        ds = bootstrap((0.02, 0.035, 0.04, 0.037))
        previous = 1.0
        for d, coupon in zip(ds, floating_coupons(ds)):
            self.assertAlmostEqual(coupon, previous - d, places=12)
            previous = d

    def test_floating_leg_telescopes_for_every_maturity(self):
        ds = bootstrap((0.02, 0.035, 0.04, 0.037))
        coupons = floating_coupons(ds)
        for maturity in range(1, len(ds) + 1):
            self.assertAlmostEqual(sum(coupons[:maturity]), 1 - ds[maturity - 1], places=12)

    def test_fixed_and_floating_legs_reconcile(self):
        quotes = (0.02, 0.035, 0.04, 0.037)
        ds = bootstrap(quotes)
        coupons = floating_coupons(ds)
        for n, rate in enumerate(quotes, 1):
            fixed_pv = rate * sum(ds[:n])
            floating_pv = sum(coupons[:n])
            self.assertAlmostEqual(fixed_pv, floating_pv, places=12)

    def test_earlier_discount_factors_ignore_later_quote(self):
        base = (0.02, 0.035, 0.04, 0.037)
        changed = (0.02, 0.035, 0.04, 0.047)
        self.assertEqual(bootstrap(base)[:3], bootstrap(changed)[:3])
        self.assertNotAlmostEqual(bootstrap(base)[3], bootstrap(changed)[3])

    def test_single_quote_bump_reprices_all_quotes(self):
        base = (0.02, 0.035, 0.04, 0.037)
        bump = 0.0001  # one basis point
        for j in range(len(base)):
            bumped = list(base)
            bumped[j] += bump
            ds = bootstrap(bumped)
            self.assertTrue(all(math.isfinite(x) and x > 0 for x in ds))
            for actual, expected in zip(reprice(ds), bumped):
                self.assertAlmostEqual(actual, expected, places=12)
            self.assertNotAlmostEqual(ds[j], bootstrap(base)[j])

    def test_negative_rate_cash_flow_reconciliation(self):
        ds = bootstrap((-0.01, -0.005, 0.002))
        self.assertAlmostEqual(sum(floating_coupons(ds)), 1 - ds[-1], places=12)
        for actual, expected in zip(reprice(ds), (-0.01, -0.005, 0.002)):
            self.assertAlmostEqual(actual, expected, places=12)


if __name__ == "__main__":
    unittest.main()
