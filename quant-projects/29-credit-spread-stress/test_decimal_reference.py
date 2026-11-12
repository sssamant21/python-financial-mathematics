"""Independent Decimal arithmetic benchmark for synthetic periodic bond discounting."""
import unittest
from decimal import Decimal, localcontext
from convention_check import periodic_price, nominal_to_continuous


def decimal_coupon_price(face: str, coupon_rate: str, nominal_yield: str, periods: int, frequency: int) -> Decimal:
    """Direct periodic cash-flow sum, without calling production pricing helpers."""
    if periods <= 0 or frequency <= 0:
        raise ValueError('periods and frequency must be positive')
    with localcontext() as ctx:
        ctx.prec = 45
        principal = Decimal(face)
        coupon = principal * Decimal(coupon_rate) / Decimal(frequency)
        base = Decimal(1) + Decimal(nominal_yield) / Decimal(frequency)
        if principal <= 0 or base <= 0:
            raise ValueError('invalid principal or discount base')
        total = sum((coupon + (principal if i == periods else Decimal(0))) / (base ** i)
                    for i in range(1, periods + 1))
        return +total


class DecimalReferenceTests(unittest.TestCase):
    def test_par_bond(self):
        expected = decimal_coupon_price('100', '.05', '.05', 10, 2)
        self.assertAlmostEqual(float(expected), 100.0, places=11)

    def test_independent_periodic_prices(self):
        for nominal in ('.00', '.03', '.05', '.12', '-.01'):
            for frequency in (1, 2, 4):
                with self.subTest(nominal=nominal, frequency=frequency):
                    periods = 5 * frequency
                    flows = [(i / frequency, 100 * .05 / frequency + (100 if i == periods else 0))
                             for i in range(1, periods + 1)]
                    expected = decimal_coupon_price('100', '.05', nominal, periods, frequency)
                    actual = periodic_price(flows, float(nominal), frequency)
                    self.assertAlmostEqual(actual, float(expected), places=9)

    def test_negative_rate_boundary(self):
        self.assertAlmostEqual(float(decimal_coupon_price('100', '0', '-.5', 1, 1)), 200.0)
        self.assertAlmostEqual(periodic_price([(1.0, 100)], -.5, 1), 200.0)

    def test_invalid_reference_base(self):
        with self.assertRaises(ValueError):
            decimal_coupon_price('100', '.05', '-2', 2, 2)

    def test_nominal_continuous_roundtrip(self):
        from math import exp
        for m in (1, 2, 4, 12):
            with self.subTest(m=m):
                cc = nominal_to_continuous(.05, m)
                self.assertAlmostEqual(m * (exp(cc / m) - 1), .05, places=12)


if __name__ == '__main__':
    unittest.main()
