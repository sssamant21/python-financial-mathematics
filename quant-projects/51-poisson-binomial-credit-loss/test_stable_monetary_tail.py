"""Synthetic regression checks for high-precision tail enumeration."""
import unittest
from decimal import Decimal
from monetary_loss import loss_distribution, tail_probability
from stable_monetary_tail import stable_tail


class StableTailTests(unittest.TestCase):
    def test_two_borrowers(self):
        self.assertEqual(stable_tail([0.1, 0.2], [100, 200], [1, 1], 300), Decimal("0.02"))

    def test_normal_tail_matches_float(self):
        p, e, g = [0.1, 0.2, 0.3], [100, 200, 300], [1, 1, 1]
        self.assertAlmostEqual(float(stable_tail(p, e, g, 300)),
                               tail_probability(loss_distribution(p, e, g), 300), places=14)

    def test_extreme_joint_tail(self):
        value = stable_tail([1e-200, 1e-200], [100, 100], [1, 1], 200)
        self.assertEqual(value, Decimal("1e-400"))
        self.assertEqual(tail_probability(loss_distribution([1e-200, 1e-200], [100, 100], [1, 1]), 200), 0.0)

    def test_deterministic(self):
        self.assertEqual(stable_tail([1, 0], [100, 200], [1, 1], 100), Decimal(1))
        self.assertEqual(stable_tail([1, 0], [100, 200], [1, 1], 101), Decimal(0))

    def test_threshold_zero_and_unreachable(self):
        self.assertEqual(stable_tail([0.2, 0.3], [100, 200], [1, 1], 0), Decimal(1))
        self.assertEqual(stable_tail([0.2, 0.3], [100, 200], [1, 1], 301), Decimal(0))

    def test_order_invariance_and_colliding_losses(self):
        a = stable_tail([0.1, 0.2, 0.3], [100, 100, 100], [1, 1, 1], 200)
        b = stable_tail([0.3, 0.1, 0.2], [100, 100, 100], [1, 1, 1], 200)
        self.assertEqual(a, b)
        self.assertEqual(a, Decimal("0.098"))

    def test_zero_lgd_and_deterministic_mass(self):
        self.assertEqual(stable_tail([1, 0.4], [100, 200], [1, 0], 100), Decimal(1))
        self.assertEqual(stable_tail([1, 0.4], [100, 200], [1, 0], 101), Decimal(0))

    def test_guards(self):
        for precision in [True, 31, 1001, 42.5]:
            with self.assertRaises(ValueError):
                stable_tail([0.1], [100], [1], 1, precision)
        with self.assertRaises(ValueError):
            stable_tail([0.1], [100], [1], True)
        with self.assertRaises(ValueError):
            stable_tail([0.1], [101], [0.5], 1)


if __name__ == "__main__":
    unittest.main()
