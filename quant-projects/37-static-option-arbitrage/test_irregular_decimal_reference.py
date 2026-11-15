"""Independent Decimal point-quote reference for irregular strike grids.

Only exact bid=ask grids are compared. This is not a general LP oracle for
nonzero bid/ask spreads and is not an independent model certification.
"""
import unittest
from decimal import Decimal, localcontext
from joint_feasibility import joint_feasible


def exact_point_reference(strikes, calls, discount=1):
    """Check exact rational-decimal monotonicity, spread bounds and convexity."""
    with localcontext() as ctx:
        ctx.prec = 70
        k = [Decimal(str(x)) for x in strikes]
        c = [Decimal(str(x)) for x in calls]
        d = Decimal(str(discount))
        if len(k) != len(c) or len(k) < 3:
            raise ValueError("aligned grid of at least three required")
        slopes = []
        for i in range(len(k) - 1):
            gap = k[i + 1] - k[i]
            if gap <= 0:
                raise ValueError("strikes must strictly increase")
            slope = (c[i + 1] - c[i]) / gap
            if not -d <= slope <= 0:
                return False
            slopes.append(slope)
        return all(x <= y for x, y in zip(slopes, slopes[1:]))


class IrregularGridReferenceTests(unittest.TestCase):
    def check_case(self, strikes, prices, expected):
        self.assertEqual(exact_point_reference(strikes, prices), expected)
        self.assertEqual(
            joint_feasible(strikes, prices, prices, tolerance=0)["joint_feasible"],
            expected,
        )

    def test_irregular_feasible_three_strikes(self):
        self.check_case([90, 90.25, 130], [20, 19.8, 8], True)

    def test_irregular_nonconvex_three_strikes(self):
        self.check_case([90, 90.25, 130], [20, 19.9, 2], False)

    def test_irregular_five_strike_feasible(self):
        self.check_case([80, 80.5, 90, 130, 131],
                        [35, 34.6, 27, 11, 10.8], True)

    def test_irregular_five_strike_violation(self):
        self.check_case([80, 80.5, 90, 130, 131],
                        [35, 34.6, 27, 11, 10.5], False)

    def test_common_unit_scaling(self):
        for factor in (0.01, 1, 100):
            with self.subTest(factor=factor):
                k = [90 * factor, 90.25 * factor, 130 * factor]
                c = [20 * factor, 19.8 * factor, 8 * factor]
                self.check_case(k, c, True)


if __name__ == "__main__":
    unittest.main()
