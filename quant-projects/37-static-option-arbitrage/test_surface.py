import unittest
from surface import diagnose, sample


class StaticArbitrageTests(unittest.TestCase):
    def test_valid_synthetic_grid(self):
        k, c = sample()
        self.assertTrue(diagnose(k, c)['valid'])

    def test_monotonicity(self):
        self.assertIn('monotonicity:1', diagnose([90, 100, 110], [12, 10, 11])['issues'])

    def test_convexity_irregular_strikes(self):
        self.assertIn('convexity:1', diagnose([90, 100, 130], [18, 14, 1])['issues'])

    def test_vertical_spread_bound(self):
        self.assertIn('vertical_spread_bound:0', diagnose([90, 100, 110], [25, 10, 9])['issues'])

    def test_invalid_inputs(self):
        for k, c in [([90, 90, 110], [10, 8, 5]), ([90, 100], [10, 8]), ([90, 100, 110], [10, float('nan'), 5])]:
            with self.subTest(k=k, c=c), self.assertRaises(ValueError):
                diagnose(k, c)
        with self.assertRaises(ValueError):
            diagnose([90, 100, 110], [10, 8, 5], discount=0)


if __name__ == '__main__':
    unittest.main()
