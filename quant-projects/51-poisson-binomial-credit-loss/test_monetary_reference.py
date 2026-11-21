"""Independent exhaustive oracle for small synthetic independent-default losses."""
import itertools
import math
import unittest
from decimal import Decimal

from monetary_loss import expected_loss, loss_distribution, tail_probability


def enumerate_reference(probabilities, exposures_cents, lgds):
    """Enumerate all default masks independently of the production recurrence."""
    losses = [int(Decimal(e) * Decimal(str(g))) for e, g in zip(exposures_cents, lgds)]
    result = {}
    for mask in itertools.product((False, True), repeat=len(probabilities)):
        amount = sum(loss for loss, default in zip(losses, mask) if default)
        weight = math.prod(p if default else 1 - p for p, default in zip(probabilities, mask))
        if weight:
            result[amount] = result.get(amount, 0.0) + weight
    return result


class MonetaryReferenceTests(unittest.TestCase):
    def check_case(self, probabilities, exposures, lgds):
        actual = loss_distribution(probabilities, exposures, lgds)
        reference = enumerate_reference(probabilities, exposures, lgds)
        self.assertEqual(set(actual), set(reference))
        for amount in reference:
            self.assertAlmostEqual(actual[amount], reference[amount], places=12)
        self.assertAlmostEqual(sum(actual.values()), 1.0, places=12)
        expected = math.fsum(p * int(Decimal(e) * Decimal(str(g)))
                             for p, e, g in zip(probabilities, exposures, lgds))
        self.assertAlmostEqual(expected_loss(actual), expected, places=9)
        for threshold in (0, 1, max(actual), max(actual) + 1):
            oracle_tail = sum(mass for amount, mass in reference.items() if amount >= threshold)
            self.assertAlmostEqual(tail_probability(actual, threshold), oracle_tail, places=12)

    def test_heterogeneous_four_borrowers(self):
        self.check_case([0.02, 0.15, 0.35, 0.8], [100, 250, 1000, 800],
                        ["0.5", "0.4", "0.2", "0.25"])

    def test_colliding_loss_states(self):
        self.check_case([0.1, 0.3, 0.6], [100, 200, 100], ["1", "0.5", "1"])

    def test_deterministic_and_zero_lgd(self):
        self.check_case([0, 1, 0.25, 0.75], [100, 400, 200, 100],
                        ["1", "0.5", "0", "1"])

    def test_order_invariance(self):
        p, e, g = [0.05, 0.3, 0.7], [100, 200, 300], ["1", "0.5", "1"]
        forward = loss_distribution(p, e, g)
        reverse = loss_distribution(p[::-1], e[::-1], g[::-1])
        self.assertEqual(set(forward), set(reverse))
        for amount in forward:
            self.assertAlmostEqual(forward[amount], reverse[amount], places=12)

    def test_extreme_tail_underflow_is_not_certified(self):
        actual = loss_distribution([1e-200, 1e-200], [100, 200], ["1", "1"])
        self.assertNotIn(300, actual)  # binary64 underflow, not zero true probability
        self.assertEqual(tail_probability(actual, 300), 0.0)


if __name__ == "__main__":
    unittest.main()
