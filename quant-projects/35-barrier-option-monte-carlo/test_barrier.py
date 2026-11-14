import unittest
from barrier import simulate


class BarrierTests(unittest.TestCase):
    def test_repeatable(self):
        self.assertEqual(simulate(pairs=100, seed=42), simulate(pairs=100, seed=42))

    def test_pathwise_barrier_bounded_by_vanilla(self):
        x = simulate(pairs=500)
        self.assertGreaterEqual(x['barrier_call'], 0)
        self.assertLessEqual(x['barrier_call'], x['vanilla_call'])

    def test_barrier_knockouts_occur(self):
        x = simulate(barrier=101, pairs=200)
        self.assertGreater(x['knockout_fraction'], 0)

    def test_high_barrier_matches_vanilla(self):
        x = simulate(barrier=1e9, pairs=100)
        self.assertEqual(x['barrier_call'], x['vanilla_call'])

    def test_invalid_inputs(self):
        for kwargs in ({'barrier': 100}, {'vol': 0}, {'pairs': 1}, {'steps': 0},
                       {'spot': float('nan')}, {'rate': 1e308}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                simulate(**kwargs)

    def test_standard_error(self):
        self.assertGreaterEqual(simulate(pairs=100)['standard_error'], 0)


if __name__ == '__main__':
    unittest.main()
