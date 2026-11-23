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

    def test_independent_piecewise_threshold(self):
        # Borrower 1 caps at m=2; borrower 2 stays linear until m=10.
        # For 2 <= m <= 10: EL = 100*0.5 + 200*(0.1*m)*0.5 = 50 + 10*m.
        r = reverse_stress([100, 200], [.5, .1], [.5, .5], 80,
                           maximum_multiplier=10)
        self.assertAlmostEqual(r["baseline_loss"], 35)
        self.assertAlmostEqual(r["breach_multiplier"], 3, places=10)
        self.assertAlmostEqual(expected_loss([100, 200], [.5, .1], [.5, .5], 3), 80)

    def test_exact_upper_bound_and_unreachable_beyond_it(self):
        at_bound = reverse_stress([100], [.1], [.5], 15, maximum_multiplier=3)
        self.assertAlmostEqual(at_bound["breach_multiplier"], 3, places=10)
        beyond = reverse_stress([100], [.1], [.5], 15.01, maximum_multiplier=3)
        self.assertIsNone(beyond["breach_multiplier"])


if __name__ == "__main__":
    unittest.main()
