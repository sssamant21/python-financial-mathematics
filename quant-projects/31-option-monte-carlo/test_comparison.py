import math
import unittest
from comparison import compare


class ComparisonTests(unittest.TestCase):
    def test_equal_budget_and_reproducibility(self):
        a = compare(pairs=120, seeds=(3, 5, 7))
        self.assertEqual(a, compare(pairs=120, seeds=(3, 5, 7)))
        self.assertEqual(a['paths_per_estimator'], 240)
        self.assertEqual(len(a['records']), 3)

    def test_coverage_is_fraction_and_variances_nonnegative(self):
        r = compare(pairs=300)
        for key in ('naive_coverage_fraction', 'antithetic_coverage_fraction'):
            self.assertGreaterEqual(r[key], 0)
            self.assertLessEqual(r[key], 1)
        self.assertGreaterEqual(r['naive_empirical_variance'], 0)
        self.assertGreaterEqual(r['antithetic_empirical_variance'], 0)

    def test_antithetic_reduces_empirical_variance_in_fixed_fixture(self):
        r = compare(pairs=2000)
        self.assertGreater(r['empirical_variance_ratio'], 1)

    def test_input_guards(self):
        for kwargs in ({'seeds': (1,)}, {'seeds': (1, 1)}, {'seeds': (True, 2)},
                       {'seeds': (1, 2.5)}, {'pairs': 1}, {'volatility': math.nan}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                compare(**kwargs)


if __name__ == '__main__':
    unittest.main()
