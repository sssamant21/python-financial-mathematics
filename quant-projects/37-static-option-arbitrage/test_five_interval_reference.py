"""Independent five-strike exact-rational bid/ask feasibility reference.

A bounded feasible polytope has a vertex. Enumerate all five-plane intersections,
using Fraction Gaussian elimination rather than Fourier-Motzkin elimination.
This is deliberately a small synthetic test oracle, not a production solver.
"""
import itertools
import unittest
from fractions import Fraction
from joint_feasibility import joint_feasible


def exact_five_feasible(strikes, bids, asks, discount=1):
    if not (len(strikes) == len(bids) == len(asks) == 5):
        raise ValueError("five aligned quotes required")
    k, b, a = ([Fraction(str(x)) for x in seq] for seq in (strikes, bids, asks))
    d = Fraction(str(discount))
    if not (d > 0 and all(x > 0 for x in k)
            and all(x < y for x, y in zip(k, k[1:]))
            and all(0 <= x <= y for x, y in zip(b, a))):
        raise ValueError("invalid quote grid")
    n = 5
    rows = []
    for i in range(n):
        e = [Fraction(0)] * n
        e[i] = 1
        rows.append((tuple(e), a[i]))
        rows.append((tuple(-v for v in e), -b[i]))
    for i in range(n-1):
        e = [Fraction(0)] * n
        e[i], e[i+1] = -1, 1
        rows.append((tuple(e), Fraction(0)))
        rows.append((tuple(-v for v in e), d * (k[i+1]-k[i])))
    for i in range(1, n-1):
        left, right = k[i]-k[i-1], k[i+1]-k[i]
        e = [Fraction(0)] * n
        e[i-1], e[i], e[i+1] = -right, left+right, -left
        rows.append((tuple(e), Fraction(0)))

    def intersection(active):
        m = [list(coeff) + [rhs] for coeff, rhs in active]
        for col in range(n):
            pivot = next((r for r in range(col, n) if m[r][col]), None)
            if pivot is None:
                return None
            m[col], m[pivot] = m[pivot], m[col]
            div = m[col][col]
            m[col] = [x / div for x in m[col]]
            for r in range(n):
                if r != col and m[r][col]:
                    f = m[r][col]
                    m[r] = [x-f*y for x, y in zip(m[r], m[col])]
        return [m[i][-1] for i in range(n)]

    for active in itertools.combinations(rows, n):
        candidate = intersection(active)
        if candidate is not None and all(
            sum(c*x for c, x in zip(coeff, candidate)) <= rhs
            for coeff, rhs in rows
        ):
            return True
    return False


class FiveStrikeReferenceTests(unittest.TestCase):
    def compare(self, strikes, bids, asks, expected):
        self.assertIs(exact_five_feasible(strikes, bids, asks), expected)
        self.assertIs(
            joint_feasible(strikes, bids, asks, tolerance=0)["joint_feasible"],
            expected,
        )

    def test_feasible_intervals(self):
        self.compare([80, 90, 100, 110, 120],
                     [21, 15, 10, 6, 3], [23, 17, 12, 8, 5], True)

    def test_infeasible_intervals(self):
        self.compare([80, 90, 100, 110, 120],
                     [21, 15, 10, 11, 3], [23, 17, 12, 12, 5], False)

    def test_irregular_strike_feasible_point_quotes(self):
        # Exact slopes -0.7, -0.5, -0.3, -0.1: valid and convex.
        self.compare([80, 85, 100, 110, 130],
                     [40, 36.5, 29, 26, 24],
                     [40, 36.5, 29, 26, 24], True)

    def test_irregular_strike_infeasible_convexity(self):
        # Slopes -0.7, -0.5, -0.9, -0.1 violate convexity.
        self.compare([80, 85, 100, 110, 130],
                     [40, 36.5, 29, 20, 18],
                     [40, 36.5, 29, 20, 18], False)

    def test_invalid_grid(self):
        with self.assertRaises(ValueError):
            exact_five_feasible([80, 90, 90, 110, 120], [1]*5, [2]*5)


if __name__ == "__main__":
    unittest.main()
