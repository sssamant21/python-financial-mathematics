"""Deterministic synthetic analytical CVA regression tests."""
import math
import unittest
from cva_benchmark import analytical_cva, compare_cva


class CVABenchmarkTests(unittest.TestCase):
    def test_zero_hazard(self):
        self.assertEqual(sum(r['incremental_cva'] for r in analytical_cva(hazard=0)), 0)

    def test_zero_volatility(self):
        self.assertEqual(sum(r['incremental_cva'] for r in analytical_cva(volatility=0)), 0)

    def test_default_mass_telescopes(self):
        rows = analytical_cva(hazard=.1, years=4)
        self.assertAlmostEqual(sum(r['default_mass'] for r in rows), 1-math.exp(-.4))

    def test_threshold_monotonic(self):
        total = lambda threshold: sum(r['incremental_cva'] for r in analytical_cva(threshold=threshold))
        self.assertGreater(total(0), total(100000))

    def test_discount_monotonic(self):
        total = lambda rate: sum(r['incremental_cva'] for r in analytical_cva(rate=rate))
        self.assertGreater(total(0), total(.1))

    def test_comparison_reproducible(self):
        a = compare_cva(paths=100, seed=7, years=2)
        self.assertEqual(a, compare_cva(paths=100, seed=7, years=2))
        self.assertAlmostEqual(a['absolute_error'], abs(a['simulated_cva']-a['analytical_cva']))

    def test_invalid_inputs(self):
        for params in ({'years': 0}, {'hazard': -1}, {'threshold': -1}, {'lgd': 2}, {'rate': float('nan')}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                analytical_cva(**params)


if __name__ == '__main__':
    unittest.main()
