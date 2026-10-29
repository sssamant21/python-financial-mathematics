"""Independent reference cases for section 20.6; runtime validation pending."""
import math
import unittest
from section_20_06 import pv, portfolio, cases, close

class Checks(unittest.TestCase):
    def test_boolean_inputs(self):
        for index in range(3):
            args=[100,.05,1]
            args[index]=True
            with self.subTest(index=index), self.assertRaises(TypeError):
                pv(*args)

    def test_invalid_numeric_types(self):
        for value in ("100",None,1+0j):
            with self.subTest(value=value), self.assertRaises(TypeError):
                pv(value,.05,1)
        with self.assertRaises(ValueError):
            pv(10**1000,.05,1)

    def test_nonfinite_each_input(self):
        for index in range(3):
            for value in (math.nan,math.inf,-math.inf):
                args=[100,.05,1]
                args[index]=value
                with self.subTest(index=index,value=value), self.assertRaises(ValueError):
                    pv(*args)

    def test_output_and_exponent_overflow(self):
        for args in ((1e308,-1,1),(1,-1000,1),(1,1e308,2),(1,-1e308,2)):
            with self.subTest(args=args), self.assertRaises(OverflowError):
                pv(*args)

    def test_underflow_policy(self):
        self.assertEqual(pv(1,1000,1),0)
        self.assertEqual(pv(0,0,1),0)

    def test_empty_portfolio_validates_rate(self):
        self.assertEqual(portfolio([],0),0)
        for value,exc in ((True,TypeError),(math.nan,ValueError),("0",TypeError)):
            with self.subTest(value=value), self.assertRaises(exc):
                portfolio([],value)

    def test_portfolio_range_and_generator(self):
        self.assertEqual(portfolio(((a,0) for a in (100,-25)),0),75)
        with self.assertRaises(OverflowError):
            portfolio([(1e308,0),(1e308,0)],0)
        with self.assertRaises(TypeError):
            portfolio([(True,0)],0)

    def test_zero_rate(self): self.assertEqual(pv(100, 0, 2), 100)
    def test_known_value(self): self.assertAlmostEqual(pv(100, math.log(2), 1), 50)
    def test_zero_time(self): self.assertEqual(pv(-40, .2, 0), -40)
    def test_split(self):
        self.assertTrue(close(portfolio([(40, 2), (60, 2)], .05), pv(100, .05, 2)))
    def test_permutation(self):
        flows = [(100, 1), (-20, 2), (75, 3)]
        self.assertTrue(close(portfolio(flows, .04), portfolio(flows[::-1], .04)))
    def test_scaling(self):
        for amount, rate, years, factor in cases():
            with self.subTest(amount=amount, rate=rate, years=years, factor=factor):
                self.assertTrue(close(pv(factor*amount, rate, years), factor*pv(amount, rate, years)))
    def test_monotonic_positive(self): self.assertLess(pv(100, .1, 2), pv(100, .05, 2))
    def test_monotonic_negative(self): self.assertGreater(pv(-100, .1, 2), pv(-100, .05, 2))
    def test_composition(self):
        self.assertTrue(close(pv(1, .04, 5), pv(1, .04, 2)*pv(1, .04, 3)))
    def test_repeatable_cases(self): self.assertEqual(list(cases()), list(cases()))
    def test_invalid_time(self):
        with self.assertRaises(ValueError): pv(100, .05, -1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): pv(math.nan, .05, 1)

if __name__ == "__main__": unittest.main()
