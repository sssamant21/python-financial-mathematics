"""Boundary regressions for Chapter 18 educational solvers."""
import unittest
import section_18_03 as s03
import section_18_04 as s04
import section_18_08 as s08
import section_18_09 as s09
import section_18_10 as s10

class SolverBoundaries(unittest.TestCase):
    def test_unrepresentable_width(self):
        for fn in (lambda: s03.bisection(lambda x:x,-1e308,1e308),
                   lambda: s04.safeguarded_newton(lambda x:x,lambda x:1,-1e308,1e308),
                   lambda: s08.audited_bisection(lambda x:x,-1e308,1e308),
                   lambda: s09.solve(lambda x:x,lambda x:1,-1e308,1e308),
                   lambda: s10.bisect(lambda x:x,-1e308,1e308)):
            with self.subTest(solver=fn), self.assertRaises(OverflowError): fn()

    def test_tiny_opposite_values(self):
        result=s10.bisect(lambda x: 5e-324*x, -1, 1)
        self.assertEqual(result['root'], 0)
        self.assertEqual(result['status'], 'exact_root')

    def test_midpoint_root_without_derivative(self):
        def unavailable(x): raise AssertionError('derivative should not be evaluated')
        result=s04.safeguarded_newton(lambda x:x, unavailable, -1, 1)
        self.assertEqual(result['status'], 'exact_root')
        self.assertEqual(result['root'], 0)

    def test_tolerance_overflow(self):
        with self.assertRaises(OverflowError):
            s03.bisection(lambda x:x+5e307, -1e308, 0.0, atol=1e308, rtol=2)

if __name__ == '__main__': unittest.main()
