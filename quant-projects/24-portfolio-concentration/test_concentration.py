import unittest
from concentration import diagnostics, drift, turnover


class ConcentrationTests(unittest.TestCase):
    def test_equal_weights(self):
        d = diagnostics([0.25] * 4)
        self.assertAlmostEqual(d['hhi'], 0.25)
        self.assertAlmostEqual(d['effective_n'], 4)
        self.assertAlmostEqual(d['normalized_entropy'], 1)

    def test_single_asset(self):
        d = diagnostics([1, 0, 0, 0])
        self.assertEqual(d['effective_n'], 1)
        self.assertEqual(d['entropy'], 0)

    def test_concentration_increases_hhi(self):
        self.assertGreater(diagnostics([0.7, 0.1, 0.1, 0.1])['hhi'], diagnostics([0.25]*4)['hhi'])

    def test_permutation_invariance(self):
        self.assertEqual(diagnostics([0.2, 0.3, 0.5]), diagnostics([0.5, 0.2, 0.3]))

    def test_turnover_identity(self):
        self.assertAlmostEqual(turnover([0.5, 0.5], [0.25, 0.75]), 0.25)
        self.assertEqual(turnover([0.5, 0.5], [0.5, 0.5]), 0)

    def test_drift_identity(self):
        self.assertEqual(drift([0.5, 0.5], [0, 0]), [0.5, 0.5])
        self.assertAlmostEqual(drift([0.5, 0.5], [1, 0])[0], 2/3)

    def test_total_loss_single_asset(self):
        self.assertEqual(drift([0.5, 0.5], [-1, 0]), [0, 1])

    def test_total_depletion_rejected(self):
        with self.assertRaises(ValueError):
            drift([0.5, 0.5], [-1, -1])

    def test_invalid_weights(self):
        for w in ([1], [0.4, 0.4], [-0.1, 1.1], [float('nan'), 1], [True, 0]):
            with self.subTest(w=w), self.assertRaises(ValueError):
                diagnostics(w)

    def test_invalid_returns(self):
        for r in ([-1.1, 0], [float('inf'), 0], [True, 0], [0]):
            with self.subTest(r=r), self.assertRaises(ValueError):
                drift([0.5, 0.5], r)

    def test_mismatched_turnover(self):
        with self.assertRaises(ValueError):
            turnover([0.5, 0.5], [0.3, 0.3, 0.4])


if __name__ == '__main__':
    unittest.main()
