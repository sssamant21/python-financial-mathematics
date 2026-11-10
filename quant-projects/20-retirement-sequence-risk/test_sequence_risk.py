import unittest
from sequence_risk import simulate, permutation_stress


class SequenceRiskTests(unittest.TestCase):
    def test_zero_withdrawal_order_independent(self):
        a = simulate(100, 0, [-0.5, 0.5])
        b = simulate(100, 0, [0.5, -0.5])
        self.assertAlmostEqual(a['terminal'], b['terminal'])

    def test_withdrawal_order_matters(self):
        a = simulate(100, 10, [-0.5, 0.5])
        b = simulate(100, 10, [0.5, -0.5])
        self.assertLess(a['terminal'], b['terminal'])

    def test_start_of_year_withdrawal(self):
        self.assertAlmostEqual(simulate(100, 10, [0.1])['terminal'], 99)

    def test_ruin_year_and_floor(self):
        result = simulate(10, 8, [0, 0])
        self.assertEqual(result['ruin_year'], 2)
        self.assertEqual(result['terminal'], 0)

    def test_exact_withdrawal_not_ruin(self):
        self.assertIsNone(simulate(10, 10, [0])['ruin_year'])

    def test_inflation_changes_terminal(self):
        self.assertLess(simulate(100, 10, [0, 0], 0.1)['terminal'],
                        simulate(100, 10, [0, 0])['terminal'])

    def test_seed_reproducible(self):
        a = permutation_stress([0.3, -0.2, 0.1], 100, 20, draws=50, seed=3)
        self.assertEqual(a, permutation_stress([0.3, -0.2, 0.1], 100, 20, draws=50, seed=3))

    def test_fraction_bounds(self):
        result = permutation_stress([0, -1, 0.5], 100, 30, draws=50)
        self.assertGreaterEqual(result['ruin_fraction'], 0)
        self.assertLessEqual(result['ruin_fraction'], 1)

    def test_invalid_inputs(self):
        for initial, wd, returns in [(0, 1, [0]), (10, -1, [0]), (10, 1, []), (10, 1, [-1.1]), (10, 1, [float('nan')])]:
            with self.subTest(initial=initial, wd=wd, returns=returns):
                with self.assertRaises(ValueError):
                    simulate(initial, wd, returns)

    def test_invalid_draws(self):
        for draws in [0, 10001, 1.5]:
            with self.assertRaises(ValueError):
                permutation_stress([0], 100, 1, draws=draws)


if __name__ == '__main__':
    unittest.main()
