import math
import unittest
from rare_event import exact_tail, estimate


class RareEventTests(unittest.TestCase):
    def test_single_bernoulli(self):
        self.assertAlmostEqual(exact_tail(1, .2, 1), .2)

    def test_exact_binomial(self):
        self.assertAlmostEqual(exact_tail(3, .5, 2), .5)

    def test_reproducibility(self):
        self.assertEqual(estimate(paths=300, seed=7), estimate(paths=300, seed=7))

    def test_unbiased_within_sampling_error(self):
        result = estimate(paths=30000, seed=51)
        self.assertLess(abs(result['importance']-result['exact']), 5*result['importance_se'])

    def test_nonnegative(self):
        result = estimate(paths=1000)
        self.assertTrue(all(result[k] >= 0 for k in result))

    def test_bad_inputs(self):
        for bad in ({'n': True}, {'p': 0}, {'q': 1}, {'threshold': 31},
                    {'paths': 99}, {'paths': True}, {'seed': -1},
                    {'p': math.nan}, {'q': math.inf}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                estimate(**bad)


if __name__ == '__main__':
    unittest.main()
