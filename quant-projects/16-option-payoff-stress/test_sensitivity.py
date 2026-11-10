import math
import unittest
from sensitivity import sensitivity_grid

class SensitivityTests(unittest.TestCase):
    def test_grid_size_and_order(self):
        rows=sensitivity_grid()
        self.assertEqual(len(rows),9)
        self.assertEqual((rows[0]['years'],rows[0]['volatility']),(0.25,0.1))
    def test_call_increases_with_volatility(self):
        rows=sensitivity_grid(maturities=(1.0,))
        self.assertTrue(all(a['value']<b['value'] for a,b in zip(rows,rows[1:])))
    def test_put_increases_with_volatility(self):
        rows=sensitivity_grid(kind='put',maturities=(1.0,))
        self.assertTrue(all(a['value']<b['value'] for a,b in zip(rows,rows[1:])))
    def test_atm_call_increases_with_maturity_for_nonnegative_rate(self):
        rows=sensitivity_grid(volatilities=(0.2,))
        self.assertTrue(all(a['value']<b['value'] for a,b in zip(rows,rows[1:])))
    def test_parity(self):
        self.assertTrue(all(abs(x['parity_residual'])<1e-10 for x in sensitivity_grid()))
    def test_invalid_inputs(self):
        for kwargs in ({'volatilities':()}, {'maturities':(0,)}, {'volatilities':(float('nan'),)}, {'kind':'straddle'}, {'volatilities':tuple([.2]*101)}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                sensitivity_grid(**kwargs)
    def test_no_mutation(self):
        vols=[.1,.2]; years=[.5,1.]
        sensitivity_grid(volatilities=vols,maturities=years)
        self.assertEqual(vols,[.1,.2]); self.assertEqual(years,[.5,1.])
    def test_repeatability(self):
        self.assertEqual(sensitivity_grid(),sensitivity_grid())
    def test_deep_out_of_money_finite(self):
        rows=sensitivity_grid(spot=10,strike=200,volatilities=(.01,),maturities=(.01,))
        self.assertTrue(math.isfinite(rows[0]['value']))
        self.assertGreaterEqual(rows[0]['value'],0)

if __name__=='__main__': unittest.main()
