import math
import unittest
from fx_forward import fair_forward, forward_value, quote_spread_screen


class FXForwardTests(unittest.TestCase):
    def test_zero_rate_differential(self):
        self.assertAlmostEqual(fair_forward(1.1, .03, .03, 2), 1.1)

    def test_closed_form(self):
        self.assertAlmostEqual(fair_forward(1.2, .05, .02, 1), 1.2 * math.exp(.03))

    def test_at_market_value_zero(self):
        k = fair_forward(1.1, .04, .02, 1.5)
        self.assertAlmostEqual(forward_value(1.1, .04, .02, 1.5, k, 1000), 0, places=9)

    def test_value_reconciles_discounted_forward_difference(self):
        s, rd, rf, t, k, n = 1.1, .04, .02, 2, 1.15, 500
        expected = n * math.exp(-rd * t) * (fair_forward(s, rd, rf, t) - k)
        self.assertAlmostEqual(forward_value(s, rd, rf, t, k, n), expected)

    def test_sign_and_notional(self):
        positive = forward_value(1.1, .04, .02, 1, 1.0, 10)
        self.assertGreater(positive, 0)
        self.assertAlmostEqual(forward_value(1.1, .04, .02, 1, 1.0, -10), -positive)

    def test_negative_rates(self):
        self.assertAlmostEqual(fair_forward(1, -.01, -.02, 1), math.exp(.01))

    def test_spread_overlap(self):
        f = fair_forward(1.1, .04, .02, 1)
        result = quote_spread_screen(1.09, 1.11, .04, .02, 1, f-.01, f+.01)
        self.assertFalse(result["disjoint"])

    def test_spread_disjoint(self):
        result = quote_spread_screen(1.09, 1.11, .04, .02, 1, 2.0, 2.1)
        self.assertTrue(result["disjoint"])

    def test_bad_inputs(self):
        for s, rd, rf, t in [(0, .02, .01, 1), (1, float("nan"), 0, 1),
                             (1, 0, 0, 0), (1, 2, 0, 1), (1, 1, -1, 100)]:
            with self.subTest(s=s, rd=rd, rf=rf, t=t):
                with self.assertRaises(ValueError):
                    fair_forward(s, rd, rf, t)
        with self.assertRaises(ValueError):
            forward_value(1, .02, .01, 1, -1)
        with self.assertRaises(ValueError):
            quote_spread_screen(1.2, 1.1, .02, .01, 1, 1.1, 1.2)


if __name__ == "__main__":
    unittest.main()
