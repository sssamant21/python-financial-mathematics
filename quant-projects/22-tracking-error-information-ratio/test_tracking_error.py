import math
import unittest
from tracking_error import diagnostics, rolling_diagnostics

class TrackingErrorTests(unittest.TestCase):
    def test_zero_active(self):
        r=diagnostics([.01,.02,.03],[.01,.02,.03])
        self.assertEqual(r["tracking_error"],0)
        self.assertIsNone(r["information_ratio"])
    def test_known_sample(self):
        r=diagnostics([.01,.03,.02],[.00,.01,.03],12)
        self.assertAlmostEqual(r["mean_active"],.006666666666666667)
        self.assertAlmostEqual(r["tracking_error"],math.sqrt(12)*math.sqrt(.00023333333333333333))
    def test_negative_ir(self):
        r=diagnostics([0,.01,-.01],[.02,.00,.01])
        self.assertLess(r["information_ratio"],0)
    def test_rolling_no_future_leak(self):
        p=[.01,.03,.02,.04,.01,.02]
        b=[0]*6
        a=rolling_diagnostics(p,b,3)
        p[-1]=.99
        c=rolling_diagnostics(p,b,3)
        self.assertEqual(a[:-1],c[:-1])
        self.assertNotEqual(a[-1],c[-1])
    def test_bad_lengths(self):
        with self.assertRaises(ValueError): diagnostics([.1,.2,.3],[.1,.2])
    def test_too_few(self):
        with self.assertRaises(ValueError): diagnostics([.1,.2],[.1,.2])
    def test_bad_values(self):
        for v in [float("nan"),float("inf"),-1.01]:
            with self.assertRaises(ValueError): diagnostics([v,0,0],[0,0,0])
    def test_bad_frequency(self):
        with self.assertRaises(ValueError): diagnostics([0,0,0],[0,0,0],0)
    def test_bad_window(self):
        with self.assertRaises(ValueError): rolling_diagnostics([0,0,0],[0,0,0],2)
if __name__=="__main__":
    unittest.main()
