import unittest
from migration import BASE, STRESS, distribution, expected_loss, validate

class MigrationTests(unittest.TestCase):
    def test_initial_state(self):
        self.assertEqual(distribution('A', 0), {'A': 1., 'B': 0., 'C': 0., 'D': 0.})

    def test_one_year_matches_row(self):
        self.assertEqual(tuple(distribution('B', 1).values()), BASE[1])

    def test_default_absorbing(self):
        self.assertEqual(distribution('D', 50)['D'], 1.)

    def test_probability_conservation(self):
        for matrix in (BASE, STRESS):
            for years in (0, 1, 3, 10, 50):
                x = distribution('C', years, matrix)
                self.assertAlmostEqual(sum(x.values()), 1., places=12)
                self.assertTrue(all(0 <= p <= 1 for p in x.values()))

    def test_cumulative_default_nondecreasing(self):
        for matrix in (BASE, STRESS):
            ds = [distribution('B', t, matrix)['D'] for t in range(11)]
            self.assertEqual(ds, sorted(ds))

    def test_stress_increases_default_for_example(self):
        self.assertGreater(distribution('B', 3, STRESS)['D'], distribution('B', 3, BASE)['D'])

    def test_expected_loss_identity(self):
        self.assertAlmostEqual(expected_loss('B', 3, .6), .6 * distribution('B', 3)['D'])
        self.assertEqual(expected_loss('B', 3, 0), 0.)

    def test_bad_inputs(self):
        for bad in (-1, 1.5, float('nan'), True):
            with self.assertRaises(ValueError):
                expected_loss(lgd=bad)
        for bad in (-1, 1.5, True, 51):
            with self.assertRaises(ValueError):
                distribution(years=bad)
        with self.assertRaises(ValueError):
            distribution(start='X')

    def test_reject_invalid_matrices(self):
        for matrix in ([(.25,)*4]*3, [(float('nan'), .2, .3, .5)]*4,
                       [(1., 0., 0., 0.)]*4, [(True, 0., 0., 0.)]*4):
            with self.assertRaises(ValueError):
                validate(matrix)

if __name__ == '__main__':
    unittest.main()
