"""Deterministic synthetic cross-model tests; no market data or trading."""
import unittest
from pde_benchmark import finite_difference_put
from binomial import price_put


class PdeBenchmarkTests(unittest.TestCase):
    def test_american_not_below_european(self):
        kw = dict(spot_steps=100, time_steps=10000)
        self.assertGreaterEqual(finite_difference_put(american=True, **kw),
                                finite_difference_put(american=False, **kw))

    def test_european_matches_crr_with_discretization_tolerance(self):
        pde = finite_difference_put(american=False, spot_steps=100, time_steps=10000)
        tree = price_put(steps=400, american=False)
        self.assertLess(abs(pde - tree), 0.20)

    def test_american_matches_crr_with_discretization_tolerance(self):
        pde = finite_difference_put(american=True, spot_steps=100, time_steps=10000)
        tree = price_put(steps=400, american=True)
        self.assertLess(abs(pde - tree), 0.25)

    def test_deep_in_money_exercise(self):
        pde = finite_difference_put(spot=50, strike=100, spot_steps=100, time_steps=10000)
        self.assertAlmostEqual(pde, 50, delta=0.5)

    def test_unstable_grid_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unstable'):
            finite_difference_put(spot_steps=200, time_steps=10)

    def test_bad_inputs_rejected(self):
        for kwargs in ({'spot': float('nan')}, {'american': 1}, {'spot_steps': True},
                       {'spot_max': 100}, {'time_steps': 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                finite_difference_put(**kwargs)


if __name__ == '__main__':
    unittest.main()
