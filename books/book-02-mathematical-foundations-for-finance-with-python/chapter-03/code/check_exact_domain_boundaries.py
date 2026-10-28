"""Focused exact-domain boundary checks for Chapter 3."""
import unittest
from fractions import Fraction as F
from section_3_01 import discounted_value
from section_3_04 import quantity_from_profit, inverse_restricted_square
from section_3_05 import flat_tier_fee, marginal_tier_fee
from section_3_06 import analyze
from section_3_09 import explore


class ExactDomainBoundaries(unittest.TestCase):
    def test_discount_rate_arbitrarily_close_to_minus_one(self):
        denominator = 10**100
        self.assertEqual(discounted_value(1, F(1, denominator) - 1), denominator)
        with self.assertRaises(ValueError):
            discounted_value(1, -1)

    def test_decreasing_profit_inverse_respects_nonnegative_domain(self):
        params = dict(price=2, unit_cost=5, fixed_cost=7)
        self.assertEqual(quantity_from_profit(-13, **params),
                         {"kind": "unique", "quantity": F(2)})
        self.assertEqual(quantity_from_profit(-6, **params)["kind"], "outside_domain")
        self.assertEqual(quantity_from_profit(-8, **params)["kind"], "not_in_range")

    def test_exact_rational_threshold_neighbors(self):
        epsilon = F(1, 10**100)
        self.assertEqual(flat_tier_fee(100), 2)
        self.assertEqual(flat_tier_fee(100 + epsilon), 5)
        self.assertEqual(marginal_tier_fee(100 - epsilon), 1 - epsilon / 100)
        self.assertEqual(marginal_tier_fee(100 + epsilon), 1 + epsilon / 50)

    def test_large_rational_square_inverse(self):
        x = F(10**100 + 1, 10**80 + 3)
        self.assertEqual(inverse_restricted_square(x*x), {"kind": "unique", "x": x})
        self.assertEqual(inverse_restricted_square(0), {"kind": "unique", "x": F(0)})

    def test_empty_and_singleton_ordered_domains(self):
        with self.assertRaises(ValueError):
            analyze(iter(()))
        result = analyze(iter((7,)))
        self.assertEqual(result["argmin"], (0,))
        self.assertEqual(result["differences"], ())
        # With no ordered pair, both strict conditions hold vacuously.
        self.assertTrue(result["strictly_increasing"])
        self.assertTrue(result["strictly_decreasing"])

    def test_expansion_threshold_and_zero_capacity(self):
        result = explore(price=10, unit_cost=2, fixed_cost=4, capacity=2,
                         expansion_after=1, expansion_cost=20)
        self.assertEqual(tuple(row[3] for row in result["rows"]), (F(-4), F(4), F(-8)))
        self.assertEqual(result["argmax"], (1,))
        self.assertFalse(result["nondecreasing"])
        single = explore(price=10, unit_cost=2, fixed_cost=4, capacity=0,
                         expansion_after=0, expansion_cost=20)
        self.assertEqual(single["rows"], ((0, F(0), F(4), F(-4)),))
        self.assertEqual(single["increments"], ())


if __name__ == "__main__":
    unittest.main()
