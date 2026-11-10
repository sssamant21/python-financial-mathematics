import unittest
from credit_risk import Exposure
from correlation_sensitivity import sensitivity

class SensitivityTests(unittest.TestCase):
    def setUp(self):
        self.book = (Exposure('A', 100, .15, .5), Exposure('B', 200, .25, .4), Exposure('C', 300, .1, .6))
    def test_repeatability(self):
        self.assertEqual(sensitivity(self.book, correlations=(0, .3), seeds=(1, 2), scenarios=200),
                         sensitivity(self.book, correlations=(0, .3), seeds=(1, 2), scenarios=200))
    def test_analytical_el_independent_of_rho(self):
        rows = sensitivity(self.book, correlations=(0, .7), seeds=(1, 2), scenarios=200)
        self.assertEqual([r['analytical_expected_loss'] for r in rows], [45.5, 45.5])
    def test_one_seed_has_no_sd(self):
        row = sensitivity(self.book, seeds=(1,), scenarios=100)[0]
        self.assertIsNone(row['var_seed_sd'])
        self.assertIsNone(row['mean_loss_seed_sd'])
    def test_multiple_seeds_nonnegative_dispersion(self):
        row = sensitivity(self.book, seeds=(1, 2, 3), scenarios=200)[0]
        self.assertGreaterEqual(row['var_seed_sd'], 0)
        self.assertGreaterEqual(row['tail_average_seed_sd'], 0)
    def test_invalid_correlation(self):
        for rhos in ((), (1,), (-.1,), (float('nan'),), (True,), (.2, .2)):
            with self.subTest(rhos=rhos), self.assertRaises(ValueError):
                sensitivity(self.book, correlations=rhos, scenarios=100)
    def test_invalid_seeds(self):
        for seeds in ((), (1, 1), (True,), (1.5,)):
            with self.subTest(seeds=seeds), self.assertRaises(ValueError):
                sensitivity(self.book, seeds=seeds, scenarios=100)
    def test_invalid_budget(self):
        with self.assertRaises(ValueError):
            sensitivity(self.book, correlations=(0, .1, .2), seeds=tuple(range(30)), scenarios=30000)
    def test_invalid_scenarios(self):
        for scenarios in (99, True, 1000001):
            with self.subTest(scenarios=scenarios), self.assertRaises(ValueError):
                sensitivity(self.book, scenarios=scenarios)
    def test_invalid_quantile(self):
        for q in (0, 1, float('inf'), True):
            with self.subTest(q=q), self.assertRaises(ValueError):
                sensitivity(self.book, quantile=q, scenarios=100)
    def test_input_immutable(self):
        before = self.book
        sensitivity(self.book, scenarios=100)
        self.assertEqual(before, self.book)

if __name__ == '__main__':
    unittest.main()
