"""Deterministic CRR pricing checks with independent one-step arithmetic."""
import math
import unittest
from binomial import price_put


class BinomialTests(unittest.TestCase):
    def test_one_step_exact(self):
        u = math.exp(0.2)
        d = 1 / u
        p = (math.exp(0.05) - d) / (u - d)
        expected = math.exp(-0.05) * (1 - p) * (100 - 100 * d)
        self.assertAlmostEqual(price_put(steps=1), expected, places=11)

    def test_american_not_cheaper(self):
        for steps in (1, 20, 100):
            self.assertGreaterEqual(price_put(steps=steps, american=True) + 1e-10,
                                    price_put(steps=steps))

    def test_deep_in_money_immediate_exercise(self):
        self.assertAlmostEqual(price_put(spot=40, strike=100, american=True),
                               60, places=8)

    def test_european_black_scholes_benchmark(self):
        # Independent closed-form put for S=K=100, r=5%, sigma=20%, T=1.
        self.assertAlmostEqual(price_put(steps=400), 5.5735260223, delta=0.02)

    def test_more_volatility_increases_european_put(self):
        self.assertGreater(price_put(volatility=0.4), price_put(volatility=0.2))

    def test_invalid_parameters(self):
        for kwargs in ({"steps": 0}, {"steps": True}, {"steps": 2001},
                       {"volatility": 0}, {"spot": float("nan")},
                       {"rate": 0.5, "dividend": -0.2, "steps": 1}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    price_put(**kwargs)


if __name__ == "__main__":
    unittest.main()
