"""Near-expiry synthetic implied-volatility identifiability checks.

These are numerical guardrail tests, not market-data validation.
"""
import math
import unittest
from iv import implied_vol, price
from sensitivity import vega


class NearExpiryTests(unittest.TestCase):
    def test_at_the_money_short_expiry_roundtrip(self):
        for years in (1 / 365, 7 / 365, 30 / 365):
            quote = price(100, 100, years, 0.0, 0.25)
            recovered = implied_vol(quote, 100, 100, years, 0.0)
            self.assertAlmostEqual(recovered, 0.25, places=6)

    def test_short_expiry_vega_decreases_at_the_money(self):
        values = [vega(100, 100, t, 0.0, 0.25) for t in (1 / 365, 7 / 365, 30 / 365)]
        self.assertTrue(all(math.isfinite(v) and v > 0 for v in values))
        self.assertLess(values[0], values[1])
        self.assertLess(values[1], values[2])

    def test_deep_out_of_money_short_expiry_is_not_identifiable(self):
        # A near-zero theoretical premium may be within solver's absolute
        # price tolerance of the zero-volatility lower boundary.
        years = 1 / 365
        quote = price(100, 150, years, 0.0, 0.25)
        self.assertLessEqual(quote, 1e-9)
        self.assertEqual(implied_vol(quote, 100, 150, years, 0.0), 0.0)

    def test_invalid_short_expiry_rejected(self):
        with self.assertRaises(ValueError):
            implied_vol(1.0, 100, 100, 0.0, 0.0)
        with self.assertRaises(ValueError):
            vega(100, 100, 0.0, 0.0, 0.25)


if __name__ == "__main__":
    unittest.main()
