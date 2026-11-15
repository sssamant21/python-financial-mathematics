"""Independent numerical integration probes for Project 35 (synthetic GBM).

Uses midpoint quadrature of the absorbed log-price density, rather than
the closed-form truncated-normal CDF evaluation in analytical.py.
This is an independent numerical implementation, not external model review.
"""
import math
import unittest

from analytical import up_and_out_call


def quadrature_call(spot=100., strike=100., barrier=130., years=1.,
                    rate=0.02, vol=0.2, bins=8192):
    if strike >= barrier:
        return 0.0
    m = (rate - vol * vol / 2) * years
    v = vol * vol * years
    a = math.log(barrier / spot)
    lo = math.log(strike / spot)
    width = (a - lo) / bins
    # The reflection density is nonnegative. expm1 avoids cancellation
    # in 1-exp(-epsilon) for paths ending close to the barrier.
    prefactor = math.exp(-rate * years) / math.sqrt(2 * math.pi * v)
    total = 0.0
    for i in range(bins):
        x = lo + (i + 0.5) * width
        z = (x - m) ** 2 / (2 * v)
        survival_factor = -math.expm1(-2 * a * (a - x) / v)
        density = math.exp(-z) * survival_factor
        payoff = spot * math.expm1(x - lo)
        total += payoff * density
    return prefactor * width * total


class NumericalReferenceTests(unittest.TestCase):
    def test_independent_midpoint_quadrature(self):
        for barrier in (105., 110., 120., 130., 150., 200.):
            with self.subTest(barrier=barrier):
                expected = quadrature_call(barrier=barrier)
                actual = up_and_out_call(barrier=barrier)
                self.assertAlmostEqual(actual, expected, delta=0.0002)

    def test_near_spot_barrier(self):
        for barrier in (100.01, 100.1, 101.):
            with self.subTest(barrier=barrier):
                actual = up_and_out_call(barrier=barrier)
                self.assertTrue(math.isfinite(actual))
                self.assertGreaterEqual(actual, 0.)
                self.assertAlmostEqual(actual, quadrature_call(barrier=barrier),
                                       delta=0.0002)

    def test_strike_near_barrier(self):
        for strike in (129., 129.9, 129.99):
            with self.subTest(strike=strike):
                actual = up_and_out_call(strike=strike)
                self.assertGreaterEqual(actual, 0.)
                self.assertAlmostEqual(actual, quadrature_call(strike=strike),
                                       delta=0.0002)


if __name__ == "__main__":
    unittest.main()
