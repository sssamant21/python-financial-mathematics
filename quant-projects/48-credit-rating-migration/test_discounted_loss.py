"""Deterministic year-end discounted credit-loss accounting tests."""
import unittest
from migration import BASE, STRESS
from time_varying import scenario_summary
from discounted_loss import discounted_expected_loss

class DiscountedLossTests(unittest.TestCase):
    def test_zero_rate_reconciles(self):
        matrices = (BASE, STRESS, BASE)
        actual = discounted_expected_loss(matrices=matrices, annual_discount_rate=0)
        old = scenario_summary(matrices=matrices)
        self.assertAlmostEqual(actual['discounted_el_per_notional'], old['cumulative_el_per_notional'])
        self.assertAlmostEqual(actual['cumulative_pd'], old['cumulative_pd'])

    def test_positive_rate_reduces_pv(self):
        result = discounted_expected_loss(annual_discount_rate=.1)
        self.assertLess(result['discounted_el_per_notional'], result['undiscounted_el_per_notional'])

    def test_rate_monotonicity(self):
        low = discounted_expected_loss(annual_discount_rate=.01)
        high = discounted_expected_loss(annual_discount_rate=.2)
        self.assertGreater(low['discounted_el_per_notional'], high['discounted_el_per_notional'])

    def test_loss_reconciliation(self):
        result = discounted_expected_loss(matrices=(BASE, STRESS))
        self.assertAlmostEqual(sum(result['annual_discounted_loss_per_notional']), result['discounted_el_per_notional'])
        self.assertAlmostEqual(sum(result['annual_loss_per_notional']), result['undiscounted_el_per_notional'])

    def test_zero_lgd(self):
        result = discounted_expected_loss(lgd=0)
        self.assertEqual(result['discounted_el_per_notional'], 0)
        self.assertGreater(result['cumulative_pd'], 0)

    def test_default_initial_state_rejected(self):
        with self.assertRaises(ValueError):
            discounted_expected_loss(start='D')

    def test_invalid_rates_and_lgd(self):
        for rate in [-.01, 1.01, float('nan'), float('inf'), True, '0.1']:
            with self.subTest(rate=rate), self.assertRaises(ValueError):
                discounted_expected_loss(annual_discount_rate=rate)
        for lgd in [-.01, 1.01, float('nan'), False]:
            with self.subTest(lgd=lgd), self.assertRaises(ValueError):
                discounted_expected_loss(lgd=lgd)

    def test_bad_matrices_rejected(self):
        with self.assertRaises(ValueError):
            discounted_expected_loss(matrices=(BASE, ((1, 0),)))

if __name__ == '__main__':
    unittest.main()
