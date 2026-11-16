"""Deterministic independent algebraic checks; no market data."""
import math
import unittest

from fra import forward_rate, fra_value


class FRATests(unittest.TestCase):
    def test_forward_ratio(self):
        self.assertAlmostEqual(forward_rate(0.99, 0.97, 0.5),
                               (0.99 / 0.97 - 1) / 0.5)

    def test_at_market_zero(self):
        f = forward_rate(0.99, 0.97, 0.5)
        result = fra_value(1e6, f, 0.99, 0.97, 0.5)
        self.assertAlmostEqual(result["pv_t0"], 0.0, places=7)

    def test_independent_pv_identity(self):
        # Discounted terminal cash flow identity, independent of settlement code.
        n, k, d1, d2, a = 2e6, 0.03, 0.985, 0.96, 0.25
        actual = fra_value(n, k, d1, d2, a)
        expected = n * (d1 - d2 * (1 + k * a))
        self.assertAlmostEqual(actual["pv_t0"], expected, places=7)
        self.assertAlmostEqual(actual["settlement_t1"] * d1,
                               actual["pv_t0"], places=7)

    def test_direction_symmetry(self):
        args = (1e6, 0.035, 0.99, 0.97, 0.5)
        receive = fra_value(*args)
        pay = fra_value(*args, receive_float=False)
        self.assertAlmostEqual(receive["pv_t0"], -pay["pv_t0"])
        self.assertAlmostEqual(receive["settlement_t1"], -pay["settlement_t1"])

    def test_strike_monotonicity(self):
        low = fra_value(1e6, 0.03, 0.99, 0.97, 0.5)["pv_t0"]
        high = fra_value(1e6, 0.04, 0.99, 0.97, 0.5)["pv_t0"]
        self.assertGreater(low, high)

    def test_invalid_inputs(self):
        cases = [
            (0, .03, .99, .97, .5),
            (1e6, math.nan, .99, .97, .5),
            (1e6, .03, 0, .97, .5),
            (1e6, .03, .99, -1, .5),
            (1e6, .03, .99, .97, 0),
            (1e6, .03, .99, .97, math.inf),
        ]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                fra_value(*args)

    def test_negative_forward_is_supported(self):
        result = fra_value(1e6, -0.02, 0.98, 0.99, 0.5)
        self.assertLess(result["forward"], 0)
        self.assertTrue(math.isfinite(result["pv_t0"]))


if __name__ == "__main__":
    unittest.main()
