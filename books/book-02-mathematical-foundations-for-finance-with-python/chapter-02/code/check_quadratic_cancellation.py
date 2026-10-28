"""Regression checks for cancellation in approximate quadratic roots."""
import unittest
from decimal import Decimal, localcontext, getcontext
from section_2_05 import approximate_roots


class QuadraticCancellation(unittest.TestCase):
    def test_separated_irrational_roots(self):
        for a in (1, -1):
            for b in ("1e50", "-1e50"):
                for c in (1, -1):
                    with self.subTest(a=a, b=b, c=c):
                        before = getcontext().copy()
                        actual = approximate_roots(a=a, b=b, c=c, precision=40)
                        self.assertEqual(getcontext().prec, before.prec)
                        with localcontext() as ctx:
                            ctx.prec = 160
                            A, B, C = Decimal(a), Decimal(b), Decimal(c)
                            disc = (B*B - 4*A*C).sqrt()
                            expected = sorted(((-B-disc)/(2*A), (-B+disc)/(2*A)))
                            for x, reference in zip(actual, expected):
                                self.assertNotEqual(x, 0)
                                self.assertLessEqual(abs((x-reference)/reference), Decimal("1e-38"))
                                scale = abs(A*x*x) + abs(B*x) + abs(C)
                                self.assertLessEqual(abs(A*x*x+B*x+C)/scale, Decimal("1e-38"))

    def test_symmetric_and_exact_classifications(self):
        roots = approximate_roots(a=1, b=0, c=-2)
        self.assertLessEqual(abs(roots[0] + roots[1]), Decimal("1e-38"))
        self.assertEqual(approximate_roots(a=1, b=-2, c=1), (Decimal(1),))
        self.assertEqual(approximate_roots(a=1, b=0, c=1), ())


if __name__ == "__main__":
    unittest.main()
