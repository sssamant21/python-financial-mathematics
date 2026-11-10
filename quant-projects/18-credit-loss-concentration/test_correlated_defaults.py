import unittest
from credit_risk import Exposure
from correlated_defaults import simulate

class CorrelatedDefaultsTests(unittest.TestCase):
    def setUp(self):
        self.book = (Exposure('A', 100, .15, .5), Exposure('B', 200, .25, .4), Exposure('C', 300, .1, .6))

    def test_reproducible(self):
        self.assertEqual(simulate(self.book, scenarios=500, seed=8), simulate(self.book, scenarios=500, seed=8))

    def test_expected_loss_identity(self):
        self.assertAlmostEqual(simulate(self.book, scenarios=100)['analytical_expected_loss'], 45.5)

    def test_tail_order(self):
        r = simulate(self.book, scenarios=1000)
        self.assertGreaterEqual(r['loss_expected_shortfall'], r['loss_var'])

    def test_zero_pd(self):
        r = simulate((Exposure('A', 100, 0, .5),), scenarios=100)
        self.assertEqual(r['loss_var'], 0)

    def test_certain_default(self):
        r = simulate((Exposure('A', 100, 1, .5),), scenarios=100)
        self.assertEqual(r['loss_var'], 50)

    def test_rho_bounds(self):
        for rho in (-.1, 1, float('nan'), True):
            with self.subTest(rho=rho), self.assertRaises(ValueError):
                simulate(self.book, asset_correlation=rho, scenarios=100)

    def test_scenario_bounds(self):
        for n in (0, 99, 1000001, 100.0, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                simulate(self.book, scenarios=n)

    def test_quantile_bounds(self):
        for q in (0, 1, float('inf'), True):
            with self.subTest(q=q), self.assertRaises(ValueError):
                simulate(self.book, quantile=q, scenarios=100)

    def test_invalid_book(self):
        with self.assertRaises(ValueError):
            simulate((Exposure('A', -1, .1, .5),), scenarios=100)

    def test_input_unchanged(self):
        before = self.book
        simulate(self.book, scenarios=100)
        self.assertEqual(self.book, before)

if __name__ == '__main__':
    unittest.main()
