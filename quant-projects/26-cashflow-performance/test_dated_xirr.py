import math
import unittest
from datetime import date
from dated_xirr import xirr

class DatedXirrTests(unittest.TestCase):
    def test_one_year_gain(self):
        self.assertAlmostEqual(xirr(['2024-01-01','2024-12-31'],[-100,110]),.1,places=8)
    def test_one_year_loss(self):
        self.assertAlmostEqual(xirr(['2024-01-01','2024-12-31'],[-100,90]),-.1,places=8)
    def test_break_even(self):
        self.assertAlmostEqual(xirr(['2024-01-01','2024-12-31'],[-100,100]),0,places=8)
    def test_midyear_contribution(self):
        r=xirr(['2024-01-01','2024-07-01','2024-12-31'],[-100,-50,165])
        self.assertTrue(0<r<.2)
    def test_timing_sensitivity(self):
        early=xirr(['2024-01-01','2024-03-01','2024-12-31'],[-100,-50,165])
        late=xirr(['2024-01-01','2024-10-01','2024-12-31'],[-100,-50,165])
        self.assertLess(early,late)
    def test_dates_as_objects(self):
        self.assertAlmostEqual(xirr([date(2024,1,1),date(2024,12,31)],[-100,110]),.1)
    def test_withdrawal_suppressed(self):
        self.assertIsNone(xirr(['2024-01-01','2024-07-01','2024-12-31'],[-100,20,110]))
    def test_bad_dates(self):
        for ds in [['2024-01-01','2024-01-01'],['2025-01-01','2024-01-01'],['bad','2024-12-31']]:
            with self.subTest(ds=ds),self.assertRaises(ValueError):
                xirr(ds,[-100,110])
    def test_bad_values(self):
        for flows in [[-100,float('nan')],[-100,True],[-100,math.inf]]:
            with self.subTest(flows=flows),self.assertRaises(ValueError):
                xirr(['2024-01-01','2024-12-31'],flows)
    def test_bad_length_and_daycount(self):
        with self.assertRaises(ValueError):
            xirr(['2024-01-01'],[-100])
        with self.assertRaises(ValueError):
            xirr(['2024-01-01','2024-12-31'],[-100,110],day_count=0)
    def test_future_mutation_isolated(self):
        dates=['2024-01-01','2024-07-01','2024-12-31']
        original=xirr(dates,[-100,-50,165])
        self.assertNotEqual(original,xirr(dates,[-100,-50,200]))
        self.assertEqual(original,xirr(dates,[-100,-50,165]))

if __name__ == '__main__':
    unittest.main()
