"""Deterministic synthetic tests; no market downloads."""
import math
import unittest
from asian_option import price_asian_call


class AsianOptionTests(unittest.TestCase):
    def test_seed_reproducible(self):
        self.assertEqual(price_asian_call(pairs=100, seed=7), price_asian_call(pairs=100, seed=7))

    def test_single_observation_matches_vanilla_pathwise(self):
        result = price_asian_call(observations=1, pairs=100, seed=3)
        self.assertAlmostEqual(result["asian_price"], result["vanilla_price"], places=12)

    def test_zero_payoff_with_very_high_strike(self):
        result = price_asian_call(strike=1e30, pairs=100)
        self.assertEqual(result["asian_price"], 0.0)
        self.assertEqual(result["standard_error"], 0.0)

    def test_nonnegative_and_finite(self):
        result = price_asian_call(pairs=200)
        self.assertGreaterEqual(result["asian_price"], 0)
        self.assertTrue(math.isfinite(result["standard_error"]))
        self.assertGreaterEqual(result["standard_error"], 0)

    def test_invalid_inputs(self):
        for kwargs in ({"spot": 0}, {"volatility": float("nan")},
                       {"maturity": -1}, {"observations": 0},
                       {"observations": 1.5}, {"pairs": 1},
                       {"rate": 100}, {"seed": True}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    price_asian_call(**kwargs)


if __name__ == "__main__":
    unittest.main()
