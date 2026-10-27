"""Regression cases for Chapter 19 small-rate account limits."""
import unittest
import section_19_01 as s01
import section_19_03 as s03
import section_19_05 as s05
import section_19_06 as s06
import section_19_07 as s07
import section_19_08 as s08
import section_19_09 as s09
import section_19_10 as s10

class SmallRateChecks(unittest.TestCase):
    def test_continuous_contributions(self):
        functions = (s01.account, s03.account, s05.exact_account,
                     s06.exact_account, s08.continuous_contributions,
                     s09.transition, s10.exact_account)
        for fn in functions:
            with self.subTest(module=fn.__module__):
                self.assertAlmostEqual(fn(0, 5e-324, 100, .5), 50)
        self.assertAlmostEqual(s07.account(100, 5e-324, 100, .5), 50)

    def test_depletion(self):
        for fn in (s03.depletion_time, s07.depletion_time,
                   s08.depletion_time, s10.depletion_time):
            with self.subTest(module=fn.__module__):
                self.assertAlmostEqual(fn(.5, 5e-324, 1), .5)
        self.assertAlmostEqual(s09.depletion_time(.5, 5e-324, -1), .5)

if __name__ == '__main__':
    unittest.main()
