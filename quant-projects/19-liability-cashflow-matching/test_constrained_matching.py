import unittest
from constrained_matching import solve, rate_stress

L = {1: 100.0, 2: 100.0}
B = [("short", 95.0, {1: 100.0}, 2), ("long", 90.0, {2: 100.0}, 2)]


class MatchingTests(unittest.TestCase):
    def test_feasible_minimum_cost(self):
        x = solve(L, B, 400)
        self.assertTrue(x["feasible"])
        self.assertEqual(x["cost"], 185)
        self.assertEqual(x["lots"], {"short": 1, "long": 1})
        self.assertTrue(all(v >= 0 for _, v in x["coverage"]))

    def test_infeasible_budget(self):
        x = solve(L, B, 180)
        self.assertFalse(x["feasible"])
        self.assertGreater(x["minimum_max_cumulative_shortfall"], 0)

    def test_no_supply(self):
        self.assertFalse(solve(L, [("short", 1, {1: 100}, 0)], 100)["feasible"])

    def test_no_borrowing(self):
        self.assertFalse(solve(L, [("late", 1, {2: 250}, 1)], 10)["feasible"])

    def test_fixed_rate_stress(self):
        x = solve(L, B, 400)
        self.assertEqual(len(rate_stress(L, B, x)), 3)
        self.assertAlmostEqual(rate_stress(L, B, x, (0,))[0][1], 0)

    def test_duplicate_names(self):
        with self.assertRaises(ValueError):
            solve(L, [B[0], B[0]], 400)

    def test_nonfinite_cost(self):
        with self.assertRaises(ValueError):
            solve(L, [("x", float("nan"), {1: 1}, 1)], 400)

    def test_invalid_limit(self):
        with self.assertRaises(ValueError):
            solve(L, [("x", 1, {1: 1}, True)], 400)

    def test_complexity_guard(self):
        with self.assertRaises(ValueError):
            solve(L, B, 400, max_combinations=8)

    def test_input_immutable(self):
        solve(L, B, 400)
        self.assertEqual(L, {1: 100.0, 2: 100.0})
        self.assertEqual(B[0][2], {1: 100.0})

    def test_bad_rate(self):
        with self.assertRaises(ValueError):
            solve(L, B, 400, annual_rate=-0.01)


if __name__ == "__main__":
    unittest.main()
