import math
import unittest

from reverse_stress import borrower_stress, expected_loss, reverse_stress


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


    def test_borrower_specific_pd_shock_reconciliation(self):
        # Predeclared idiosyncratic PD shocks are represented as fixed input PDs,
        # not inferred from outcomes or optimized after observing the threshold.
        eads = [100, 200, 300]
        stressed_pds = [.05, .10, .20]
        lgds = [.5, .25, .4]
        # Baseline EL = 2.5 + 5 + 24 = 31.5; at m=2, EL = 63.
        self.assertAlmostEqual(expected_loss(eads, stressed_pds, lgds), 31.5)
        self.assertAlmostEqual(expected_loss(eads, stressed_pds, lgds, 2), 63)
        result = reverse_stress(eads, stressed_pds, lgds, 63,
                                maximum_multiplier=3)
        self.assertAlmostEqual(result["breach_multiplier"], 2, places=10)

    def test_zero_exposure_and_search_boundary(self):
        # A zero-EAD borrower must not affect the stress threshold.
        base = reverse_stress([100], [.1], [.5], 10, maximum_multiplier=2)
        with_zero = reverse_stress([100, 0], [.1, 1], [.5, 1], 10,
                                   maximum_multiplier=2)
        self.assertAlmostEqual(base["breach_multiplier"], 2, places=10)
        self.assertEqual(base["breach_multiplier"], with_zero["breach_multiplier"])


    def test_explicit_vector_attribution(self):
        result = borrower_stress([100, 200, 300], [.5, .1, 0], [.5, .25, 1], [3, 2, 100])
        self.assertAlmostEqual(result["baseline_loss"], 30)
        self.assertAlmostEqual(result["stressed_loss"], 60)
        self.assertAlmostEqual(result["incremental_loss"], 30)
        self.assertEqual([row["stressed_pd"] for row in result["borrowers"]], [1, .2, 0])
        for row, expected in zip(result["borrowers"], [25, 5, 0]):
            self.assertAlmostEqual(row["incremental_loss"], expected)

    def test_vector_common_multiplier_equivalence(self):
        for m in [1, 2, 100]:
            result = borrower_stress([100, 200], [.1, .4], [.5, .25], [m, m])
            self.assertAlmostEqual(result["stressed_loss"],
                                   expected_loss([100, 200], [.1, .4], [.5, .25], m))

    def test_invalid_vector(self):
        for vector in [[], [1, 2], [.9], [True], [float("inf")], [float("nan")]]:
            with self.subTest(vector=vector):
                with self.assertRaises(ValueError):
                    borrower_stress([100], [.1], [.5], vector)

    def test_vector_loss_overflow(self):
        with self.assertRaises(ValueError):
            borrower_stress([1e308, 1e308], [.1, .1], [1, 1], [10, 10])


if __name__ == "__main__":
    unittest.main()
