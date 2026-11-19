"""Synthetic analytical diagnostics regression tests."""
import math
import unittest
from diagnostics import brownian_epe, brownian_pfe, epe_standard_error

class DiagnosticsTests(unittest.TestCase):
    def test_zero_threshold_epe_closed_form(self):
        self.assertAlmostEqual(brownian_epe(notional=100, volatility=.2, year=4), 40/math.sqrt(2*math.pi))
    def test_zero_volatility(self):
        self.assertEqual(brownian_epe(notional=100, volatility=0, year=3), 0)
        self.assertEqual(brownian_pfe(notional=100, volatility=0, year=3), 0)
    def test_threshold_monotonic(self):
        a = brownian_epe(notional=100, volatility=.3, year=2)
        b = brownian_epe(notional=100, volatility=.3, year=2, threshold=10)
        self.assertGreater(a,b)
        self.assertGreater(b,0)
    def test_pfe_formula(self):
        self.assertAlmostEqual(brownian_pfe(notional=100, volatility=.2, year=1), 20*1.6448536269514722)
        self.assertEqual(brownian_pfe(notional=100, volatility=.2, year=1, threshold=100), 0)
    def test_standard_error(self):
        self.assertAlmostEqual(epe_standard_error([0,2]),1)
        self.assertEqual(epe_standard_error([5,5,5]),0)
    def test_reject_invalid(self):
        for kwargs in ({'notional':True}, {'year':0}, {'volatility':-1}, {'threshold':float('nan')}, {'notional':float('inf')}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                brownian_epe(**{**dict(notional=100, volatility=.2, year=1), **kwargs})
        for c in (0,1,float('nan'),True):
            with self.assertRaises(ValueError):
                brownian_pfe(notional=100,volatility=.2,year=1,confidence=c)
        for values in ([1], [0,float('nan')],[-1,2]):
            with self.assertRaises(ValueError):
                epe_standard_error(values)

if __name__ == '__main__':
    unittest.main()
