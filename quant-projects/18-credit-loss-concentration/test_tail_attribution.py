"""Synthetic deterministic tail-attribution regression tests."""
import unittest
from credit_risk import Exposure
from tail_attribution import attribute, concentration_comparison

BOOK = (Exposure('A', 1000000, .01, .45), Exposure('B', 500000, .03, .60), Exposure('C', 250000, .06, .50))

class TailAttributionTests(unittest.TestCase):
    def test_additivity(self):
        x = attribute(BOOK, scenarios=2000)
        self.assertAlmostEqual(sum(x['tail_contributions'].values()), x['tail_average_loss'])
    def test_repeatable(self):
        self.assertEqual(attribute(BOOK, scenarios=200), attribute(BOOK, scenarios=200))
    def test_tail_count(self):
        self.assertEqual(attribute(BOOK, scenarios=1000, quantile=.99)['tail_count'], 11)
    def test_var_bounded_by_tail_mean(self):
        x = attribute(BOOK, scenarios=1000)
        self.assertLessEqual(x['loss_var'], x['tail_average_loss'])
    def test_zero_pd(self):
        self.assertEqual(attribute((Exposure('X', 100, 0, .5),), scenarios=100)['tail_average_loss'], 0)
    def test_certain_default(self):
        self.assertEqual(attribute((Exposure('X', 100, 1, .5),), scenarios=100)['tail_contributions']['X'], 50)
    def test_concentration_reduction(self):
        x = concentration_comparison(BOOK, scenarios=1000)
        self.assertLess(x['redistributed']['ead_hhi'], x['baseline']['ead_hhi'])
        self.assertEqual(x['total_ead'], 1750000)
    def test_input_immutable(self):
        before = repr(BOOK)
        concentration_comparison(BOOK, scenarios=100)
        self.assertEqual(repr(BOOK), before)
    def test_invalid_correlation(self):
        for v in (-.1, 1, float('nan'), True):
            with self.subTest(v=v), self.assertRaises(ValueError):
                attribute(BOOK, asset_correlation=v)
    def test_invalid_budget(self):
        with self.assertRaises(ValueError):
            attribute(BOOK, scenarios=100001)
    def test_invalid_quantile(self):
        with self.assertRaises(ValueError):
            attribute(BOOK, quantile=1)
    def test_invalid_transfer(self):
        with self.assertRaises(ValueError):
            concentration_comparison(BOOK, transfer_fraction=0)
    def test_single_borrower(self):
        with self.assertRaises(ValueError):
            concentration_comparison((BOOK[0],))

if __name__ == '__main__':
    unittest.main()
