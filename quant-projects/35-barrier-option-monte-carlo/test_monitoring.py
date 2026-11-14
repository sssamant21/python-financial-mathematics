"""Deterministic checks for matched Brownian-path monitoring."""
import unittest
from monitoring import black_scholes_call, matched_monitoring


class MonitoringTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(matched_monitoring(pairs=60, fine_steps=24, monitoring=(4, 8, 24), seed=8),
                         matched_monitoring(pairs=60, fine_steps=24, monitoring=(4, 8, 24), seed=8))

    def test_nested_pathwise_monotonicity(self):
        x = matched_monitoring(pairs=200, fine_steps=24, monitoring=(4, 8, 24))
        values = [g['barrier_call'] for g in x['grids']]
        self.assertTrue(all(a >= b for a, b in zip(values, values[1:])))
        self.assertLessEqual(values[0], x['vanilla_mc'])
        self.assertTrue(all(a['knockout_fraction'] <= b['knockout_fraction'] for a, b in zip(x['grids'], x['grids'][1:])))

    def test_high_barrier_is_vanilla(self):
        x = matched_monitoring(barrier=1e9, pairs=30, fine_steps=12, monitoring=(3, 6, 12))
        self.assertTrue(all(g['barrier_call'] == x['vanilla_mc'] for g in x['grids']))

    def test_black_scholes_reference(self):
        self.assertAlmostEqual(black_scholes_call(100, 100, 1, 0.05, 0.2), 10.450583572185565, places=9)

    def test_mc_benchmark_with_sampling_tolerance(self):
        x = matched_monitoring(pairs=4000, fine_steps=12, monitoring=(3, 6, 12), seed=11)
        self.assertLess(abs(x['vanilla_mc_minus_bs']), 5 * x['vanilla_standard_error'] + 0.02)

    def test_invalid_grids(self):
        for kwargs in ({'fine_steps': 0}, {'monitoring': (5,), 'fine_steps': 12},
                       {'monitoring': (3, 3), 'fine_steps': 12}, {'monitoring': ()},
                       {'pairs': 1}, {'barrier': 100}, {'vol': float('nan')},
                       {'seed': True}, {'rate': 1e308}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                matched_monitoring(**kwargs)


if __name__ == '__main__':
    unittest.main()
