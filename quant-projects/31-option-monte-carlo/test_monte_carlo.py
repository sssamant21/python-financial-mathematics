import math
import unittest
from monte_carlo import black_scholes_call, estimate


class OptionMonteCarloTests(unittest.TestCase):
    def test_black_scholes_independent_known_benchmark(self):
        self.assertAlmostEqual(black_scholes_call(100, 100, .05, 0, .2, 1), 10.450583572185565, places=9)

    def test_reproducible(self):
        self.assertEqual(estimate(pairs=300, seed=77), estimate(pairs=300, seed=77))

    def test_pair_count_and_interval(self):
        r = estimate(pairs=500, seed=11)
        self.assertEqual((r['pairs'], r['paths']), (500, 1000))
        self.assertAlmostEqual((r['ci95_high'] - r['ci95_low']) / 2, 1.96 * r['standard_error'])
        self.assertGreaterEqual(r['standard_error'], 0)

    def test_at_the_money_synthetic_convergence(self):
        r = estimate(pairs=50000, seed=2026)
        self.assertLess(abs(r['error']), .2)

    def test_dividend_benchmark(self):
        a = black_scholes_call(100, 100, .03, 0, .2, 1)
        b = black_scholes_call(100, 100, .03, .04, .2, 1)
        self.assertLess(b, a)

    def test_invalid_inputs(self):
        for kwargs in ({'spot': 0}, {'volatility': 0}, {'years': -1}, {'pairs': 1},
                       {'pairs': True}, {'rate': math.nan}, {'strike': math.inf},
                       {'seed': 1.5}, {'volatility': 4}, {'pairs': 2000001}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                estimate(**kwargs)

    def test_analytic_invalid(self):
        with self.assertRaises(ValueError):
            black_scholes_call(100, 0, .03, 0, .2, 1)


if __name__ == '__main__':
    unittest.main()
