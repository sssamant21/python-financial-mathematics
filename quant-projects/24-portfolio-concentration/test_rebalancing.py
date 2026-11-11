import unittest
from rebalancing import simulate


class RebalancingTests(unittest.TestCase):
    def setUp(self):
        self.targets = [[0.5, 0.5]] * 3
        self.returns = [[0.2, -0.1], [-0.05, 0.1], [0.0, 0.03]]

    def test_zero_cost_first_period(self):
        rows = simulate([0.5, 0.5], self.targets, self.returns, 0)
        self.assertAlmostEqual(rows[0]['end_wealth'], 1.05)
        self.assertEqual(rows[0]['turnover'], 0)

    def test_cost_reduces_wealth(self):
        free = simulate([0.5, 0.5], self.targets, self.returns, 0)
        costly = simulate([0.5, 0.5], self.targets, self.returns, 50)
        self.assertLess(costly[-1]['end_wealth'], free[-1]['end_wealth'])

    def test_drift_causes_next_period_turnover(self):
        rows = simulate([0.5, 0.5], self.targets, self.returns)
        self.assertGreater(rows[1]['turnover'], 0)

    def test_future_mutation_does_not_change_past(self):
        baseline = simulate([0.5, 0.5], self.targets, self.returns)
        altered = simulate([0.5, 0.5], self.targets, self.returns[:2] + [[-1, 0]])
        self.assertEqual(baseline[:2], altered[:2])

    def test_known_turnover(self):
        rows = simulate([0.5, 0.5], [[1, 0]], [[0, 0]], 100)
        self.assertAlmostEqual(rows[0]['turnover'], 0.5)
        self.assertAlmostEqual(rows[0]['cost'], 0.005)
        self.assertAlmostEqual(rows[0]['end_wealth'], 0.995)

    def test_invalid_costs(self):
        for bps in (-1, 10000, True, float('nan'), float('inf')):
            with self.subTest(bps=bps), self.assertRaises(ValueError):
                simulate([0.5, 0.5], self.targets, self.returns, bps)

    def test_invalid_schedules(self):
        for targets, returns in (([], []), (self.targets[:1], self.returns), ([[1]], [[0, 0]])):
            with self.subTest(targets=targets), self.assertRaises(ValueError):
                simulate([0.5, 0.5], targets, returns)

    def test_loss_depletion(self):
        with self.assertRaises(ValueError):
            simulate([0.5, 0.5], [[0.5, 0.5]], [[-1, -1]])

    def test_asset_order_swap_invariance(self):
        a = simulate([0.5, 0.5], self.targets, self.returns)
        b = simulate([0.5, 0.5], self.targets, [list(reversed(x)) for x in self.returns])
        self.assertAlmostEqual(a[-1]['end_wealth'], b[-1]['end_wealth'])


if __name__ == '__main__':
    unittest.main()
