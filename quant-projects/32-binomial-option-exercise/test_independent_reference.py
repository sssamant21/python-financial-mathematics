"""Cross-check bottom-up pricer against a separately coded top-down tree."""
import math
import unittest
from independent_reference import MAX_STEPS, compare_grid, reference_put
from binomial import price_put


class ReferenceTests(unittest.TestCase):
    def test_precommitted_grid_matches(self):
        rows = compare_grid()
        self.assertEqual(len(rows), 30)
        for params, steps, american, expected, actual, error in rows:
            with self.subTest(params=params, steps=steps, american=american):
                self.assertTrue(math.isfinite(expected))
                self.assertAlmostEqual(actual, expected, delta=1e-9)
                self.assertLess(error, 1e-9)

    def test_american_premium(self):
        for spot in (70.0, 100.0, 120.0):
            american = reference_put(spot=spot, american=True)
            european = reference_put(spot=spot, american=False)
            self.assertGreaterEqual(american + 1e-12, european)

    def test_deep_itm_immediate_exercise(self):
        self.assertAlmostEqual(reference_put(spot=40, steps=20), 60, delta=1e-9)
        self.assertAlmostEqual(price_put(spot=40, steps=20, american=True), 60, delta=1e-9)

    def test_invalid_step_and_probability(self):
        for n in (0, -1, 25, True, 2.0):
            with self.subTest(n=n), self.assertRaises(ValueError):
                reference_put(steps=n)
        with self.assertRaises(ValueError):
            reference_put(rate=0.5, dividend=-0.2, volatility=0.01, steps=1)

    def test_nonfinite_and_bad_boolean(self):
        with self.assertRaises(ValueError):
            reference_put(spot=float("nan"))
        with self.assertRaises(ValueError):
            reference_put(american=1)

    def test_boundary_decision_by_value(self):
        # Deep ITM: intrinsic value equals the American price at time zero.
        for spot in (35.0, 40.0):
            self.assertAlmostEqual(reference_put(spot=spot, steps=20),
                                   100.0 - spot, delta=1e-9)
        # At the money, positive time value implies no immediate exercise.
        self.assertGreater(reference_put(spot=100.0, steps=20), 0)


if __name__ == "__main__":
    unittest.main()
