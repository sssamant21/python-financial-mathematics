import math
import unittest

from reverse_stress import expected_loss, reverse_stress


class ReverseStressTests(unittest.TestCase):
    def test_known_expected_loss(self):
        self.assertAlmostEqual(expected_loss([100, 200], [.1, .2], [.5, .25]), 15)

    def test_known_linear_threshold(self):
        r = reverse_stress([100], [.1], [.5], 10)
        self.assertAlmostEqual(r["breach_multiplier"], 2, places=10)

    def test_baseline_threshold(self):
        self.assertEqual(reverse_stress([100], [.1], [.5], 5)["breach_multiplier"], 1)

    def test_unreachable_saturation(self):
        self.assertIsNone(reverse_stress([100], [.1], [.5], 60)["breach_multiplier"])

    def test_pd_cap(self):
        self.assertEqual(expected_loss([100], [.8], [.5], 10), 50)

    def test_monotonicity(self):
        a = [expected_loss([100, 200], [.01, .1], [.4, .6], x) for x in [1, 2, 5, 100]]
        self.assertEqual(a, sorted(a))

    def test_zero_pd_unreachable(self):
        self.assertIsNone(reverse_stress([100], [0], [1], 1)["breach_multiplier"])

    def test_invalid_inputs(self):
        for fn in [
            lambda: expected_loss([100], [.1, .2], [.5]),
            lambda: expected_loss([100], [1.1], [.5]),
            lambda: expected_loss([100], [.1], [float("nan")]),
            lambda: expected_loss([100], [.1], [.5], True),
            lambda: reverse_stress([100], [.1], [.5], 0),
            lambda: reverse_stress([100], [.1], [.5], 5, iterations=True),
            lambda: reverse_stress([100], [.1], [.5], 5, maximum_multiplier=.5),
        ]:
            with self.subTest(fn=fn):
                with self.assertRaises(ValueError):
                    fn()


if __name__ == "__main__":
    unittest.main()
