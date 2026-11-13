import math
import unittest
from sensitivity import grid


class SensitivityTests(unittest.TestCase):
    def test_reproducible_equal_budget(self):
        kwargs = dict(pairs=40, seeds=(3, 5, 7), strikes=(90., 110.), volatilities=(.1, .3))
        a = grid(**kwargs)
        self.assertEqual(a, grid(**kwargs))
        self.assertEqual(a['paths_per_method'], 80)
        self.assertEqual(len(a['rows']), 4)

    def test_analytical_benchmark_and_bounds(self):
        rows = grid(pairs=40, seeds=(3, 5), strikes=(80., 120.),
                    volatilities=(.1, .4))['rows']
        self.assertGreater(rows[0]['benchmark'], rows[2]['benchmark'])
        self.assertGreater(rows[1]['benchmark'], rows[0]['benchmark'])
        for row in rows:
            self.assertGreaterEqual(row['naive_variance'], 0)
            self.assertGreaterEqual(row['antithetic_variance'], 0)
            self.assertTrue(0 <= row['naive_coverage'] <= 1)
            self.assertTrue(0 <= row['antithetic_coverage'] <= 1)

    def test_invalid_inputs(self):
        for kwargs in ({'strikes': ()}, {'strikes': (100., 100.)},
                       {'strikes': (math.nan,)}, {'strikes': (True,)},
                       {'volatilities': (0.,)}, {'volatilities': (.2, .2)},
                       {'pairs': 1}, {'seeds': (1, 1)}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                grid(**kwargs)


if __name__ == '__main__':
    unittest.main()
