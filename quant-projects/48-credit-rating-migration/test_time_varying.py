import unittest
from migration import BASE, STRESS, distribution
from time_varying import path_distributions, annual_default_increments, scenario_summary

class TimeVaryingTests(unittest.TestCase):
    def test_constant_matrix_matches_homogeneous_model(self):
        for years in (1, 3, 10):
            self.assertAlmostEqual(path_distributions('B', (BASE,) * years)[-1]['D'],
                                   distribution('B', years, BASE)['D'], places=12)

    def test_first_year_matches_transition_row(self):
        self.assertEqual(tuple(path_distributions('C', (STRESS,))[1].values()), STRESS[2])

    def test_shock_order_changes_path(self):
        a = path_distributions('B', (STRESS, BASE, BASE))[-1]
        b = path_distributions('B', (BASE, BASE, STRESS))[-1]
        self.assertNotAlmostEqual(a['D'], b['D'], places=8)

    def test_increments_reconcile(self):
        seq = (BASE, STRESS, BASE)
        path = path_distributions('B', seq)
        increments = annual_default_increments('B', seq)
        self.assertAlmostEqual(sum(increments), path[-1]['D'], places=12)
        self.assertTrue(all(x >= 0 for x in increments))

    def test_absorbing_default(self):
        self.assertEqual(scenario_summary('D', (BASE, STRESS))['cumulative_pd'], 0)
        self.assertEqual(path_distributions('D', (BASE, STRESS))[-1]['D'], 1)

    def test_el_identity(self):
        x = scenario_summary('B', (BASE, STRESS, BASE), 0.4)
        self.assertAlmostEqual(x['cumulative_el_per_notional'], x['cumulative_pd'] * 0.4)

    def test_invalid_inputs(self):
        for seq in ((), (BASE,) * 51, 'bad', (BASE, ((1, 0, 0, 0),) * 4)):
            with self.assertRaises(ValueError):
                path_distributions('B', seq)
        for lgd in (-0.1, 1.1, float('nan'), True):
            with self.assertRaises(ValueError):
                scenario_summary(lgd=lgd)
        with self.assertRaises(ValueError):
            path_distributions('X', (BASE,))

if __name__ == '__main__':
    unittest.main()
