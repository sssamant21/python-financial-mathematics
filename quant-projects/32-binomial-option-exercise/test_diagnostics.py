"""Deterministic synthetic regression tests for CRR diagnostics."""
import math
import unittest
from diagnostics import BENCHMARK, STEPS, convergence, exercise_boundary
from binomial import price_put


class DiagnosticsTests(unittest.TestCase):
    def test_predeclared_grid_and_benchmark(self):
        rows = convergence()
        self.assertEqual(tuple(n for n, *_ in rows), STEPS)
        self.assertAlmostEqual(BENCHMARK, 5.5735260223, delta=1e-9)
        self.assertLess(rows[-1][3], 0.02)
        self.assertLess(rows[-1][3], rows[0][3])

    def test_american_dominates_european(self):
        for _, european, american, _ in convergence():
            self.assertGreaterEqual(american + 1e-10, european)

    def test_boundary_has_valid_spots_and_layers(self):
        rows = exercise_boundary(steps=80)
        self.assertEqual(len(rows), 80)
        self.assertEqual(rows[0][0], 0.0)
        self.assertTrue(any(count > 0 for _, _, count in rows))
        for time, boundary, count in rows:
            self.assertTrue(math.isfinite(time))
            self.assertEqual(boundary is None, count == 0)
            if boundary is not None:
                self.assertGreater(boundary, 0)
                self.assertLess(boundary, 100)

    def test_boundary_no_exercise_at_initial_atm_node(self):
        self.assertEqual(exercise_boundary(steps=80)[0][2], 0)

    def test_deep_in_money_initial_exercise(self):
        rows = exercise_boundary(steps=80, spot=40)
        self.assertEqual(rows[0][2], 1)
        self.assertAlmostEqual(rows[0][1], 40)
        self.assertAlmostEqual(price_put(spot=40, american=True, steps=80), 60)

    def test_invalid_inputs(self):
        for steps in ((), (0,), (2001,), (True,), (10.0,)):
            with self.subTest(steps=steps), self.assertRaises(ValueError):
                convergence(steps)
        with self.assertRaises(ValueError):
            exercise_boundary(steps=0)


if __name__ == "__main__":
    unittest.main()
