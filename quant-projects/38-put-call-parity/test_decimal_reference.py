"""Independent Decimal parity reference on deterministic synthetic quotes."""
from decimal import Decimal, localcontext
import math
import unittest
from parity import parity_bounds


def reference(spot, strike, years, rate, dividend_yield):
    """High-precision reference; convert decimal *strings*, not binary floats."""
    with localcontext() as ctx:
        ctx.prec = 60
        s, k, t, r, q = map(Decimal, (spot, strike, years, rate, dividend_yield))
        return s * (-q * t).exp() - k * (-r * t).exp()


class DecimalReferenceTests(unittest.TestCase):
    def test_discount_sensitivity_grid(self):
        for r, q, t in [('0', '0', '1'), ('0.03', '0.01', '1'),
                        ('-0.02', '0.04', '2.5'), ('0.08', '-0.01', '0.25')]:
            with self.subTest(rate=r, yield_=q, years=t):
                expected = reference('100', '105', t, r, q)
                actual = parity_bounds(100, 105, float(t), float(r), float(q), 10, 20, 10, 20)
                self.assertTrue(math.isclose(actual['theoretical_call_minus_put'],
                                             float(expected), rel_tol=1e-12, abs_tol=2e-12))

    def test_discount_direction(self):
        def value(r, q):
            return parity_bounds(100, 100, 1, r, q, 5, 30, 5, 30)['theoretical_call_minus_put']
        self.assertGreater(value(0.04, 0.01), value(0.02, 0.01))
        self.assertLess(value(0.02, 0.03), value(0.02, 0.01))

    def test_boundary_with_explicit_margin(self):
        expected = float(reference('100', '100', '1', '0.03', '0.01'))
        # Quoted interval is [call_bid - put_ask, call_ask - put_bid].
        # Margin is deliberately much larger than the float/Decimal difference.
        for margin, compatible in [(1e-6, True), (-1e-6, False)]:
            with self.subTest(margin=margin):
                lower = expected - margin
                result = parity_bounds(100, 100, 1, 0.03, 0.01,
                                       10 + lower, 10 + lower + 1, 10, 10)
                self.assertEqual(result['compatible'], compatible)
                self.assertAlmostEqual(result['gap'], max(-margin, 0), delta=2e-12)

    def test_zero_rate_zero_yield_exact_integer_case(self):
        result = parity_bounds(110, 100, 1, 0, 0, 15, 15, 5, 5)
        self.assertEqual(result['theoretical_call_minus_put'], 10)
        self.assertTrue(result['compatible'])
        self.assertEqual(result['gap'], 0)


if __name__ == '__main__':
    unittest.main()
