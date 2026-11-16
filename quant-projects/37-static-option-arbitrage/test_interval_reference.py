"""Independent exact-rational vertex feasibility reference for three call strikes.

Finite bid/ask bounds imply a compact polytope; if nonempty it has a vertex.
Enumerating triples of active planes is independent of Fourier-Motzkin.
"""
import itertools
import unittest
from fractions import Fraction
from joint_feasibility import joint_feasible


def reference_three_strikes(strikes, bids, asks, discount=1):
    if len(strikes) != 3 or len(bids) != 3 or len(asks) != 3:
        raise ValueError("three aligned quotes required")
    k, b, a = [[Fraction(str(v)) for v in seq] for seq in (strikes, bids, asks)]
    d = Fraction(str(discount))
    if not 0 < k[0] < k[1] < k[2] or d <= 0 or any(x < 0 or y < x for x, y in zip(b, a)):
        raise ValueError("invalid strikes, quotes or discount")
    rows = []
    for i in range(3):
        e = [Fraction(0)] * 3
        e[i] = 1
        rows.extend(((e, a[i]), ([-v for v in e], -b[i])))
    for i in range(2):
        e = [Fraction(0)] * 3
        e[i], e[i + 1] = -1, 1
        rows.extend(((e, Fraction(0)), ([-v for v in e], d * (k[i + 1] - k[i]))))
    left, right = k[1] - k[0], k[2] - k[1]
    rows.append(([-right, left + right, -left], Fraction(0)))

    def solve(triple):
        matrix = [list(coeff) + [rhs] for coeff, rhs in triple]
        for col in range(3):
            pivot = next((i for i in range(col, 3) if matrix[i][col]), None)
            if pivot is None:
                return None
            matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
            factor = matrix[col][col]
            matrix[col] = [v / factor for v in matrix[col]]
            for i in range(3):
                if i != col:
                    factor = matrix[i][col]
                    matrix[i] = [v - factor * w for v, w in zip(matrix[i], matrix[col])]
        return [matrix[i][3] for i in range(3)]

    for triple in itertools.combinations(rows, 3):
        candidate = solve(triple)
        if candidate is not None and all(
            sum(x * y for x, y in zip(coeff, candidate)) <= rhs for coeff, rhs in rows
        ):
            return True
    return False


class IntervalReferenceTests(unittest.TestCase):
    def compare(self, strikes, bids, asks, expected):
        self.assertEqual(reference_three_strikes(strikes, bids, asks), expected)
        self.assertEqual(
            joint_feasible(strikes, bids, asks, tolerance=0)["joint_feasible"], expected
        )

    def test_point_feasible(self):
        self.compare([90, 100, 110], [15, 10, 6], [15, 10, 6], True)

    def test_interval_feasible(self):
        self.compare([90, 100, 110], [15, 8, 5], [16, 12, 6], True)

    def test_interval_infeasible(self):
        self.compare([90, 100, 110], [15, 12, 1], [16, 13, 2], False)

    def test_irregular_strikes(self):
        self.compare([90, 90.25, 130], [20, 19.7, 7.8], [20.2, 19.9, 8.2], True)

    def test_invalid_strikes(self):
        with self.assertRaises(ValueError):
            reference_three_strikes([90, 90, 110], [10, 9, 8], [11, 10, 9])


if __name__ == "__main__":
    unittest.main()
