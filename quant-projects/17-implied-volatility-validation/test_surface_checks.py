import unittest
from implied_vol import price
from surface_checks import check_call_strikes, check_call_calendar

class SurfaceTests(unittest.TestCase):
    def setUp(self):
        self.strikes=[(k,price("call",100,k,1,.05,.2)-.01,price("call",100,k,1,.05,.2)+.01) for k in (90.,100.,110.)]
        self.calendar=[(t,price("call",100,100,t,.05,.2)-.01,price("call",100,100,t,.05,.2)+.01) for t in (.5,1.,2.)]
    def test_strikes(self): self.assertTrue(check_call_strikes(self.strikes,100,1,.05)["passed"])
    def test_calendar(self): self.assertTrue(check_call_calendar(self.calendar,100,100,.05)["passed"])
    def test_monotonic(self):
        self.assertIn("monotonic",[x[0] for x in check_call_strikes([(90,15,16),(100,17,18)],100,1)["violations"]])
    def test_vertical(self):
        self.assertIn("vertical_spread",[x[0] for x in check_call_strikes([(90,50,51),(100,1,2)],100,1)["violations"]])
    def test_butterfly(self):
        self.assertIn("butterfly",[x[0] for x in check_call_strikes([(90,20,21),(100,18,19),(110,1,2)],100,1)["violations"]])
    def test_calendar_violation(self):
        self.assertIn("calendar",[x[0] for x in check_call_calendar([(.5,20,21),(1.,10,11)],100,100)["violations"]])
    def test_dividend_guard(self):
        with self.assertRaises(ValueError): check_call_calendar(self.calendar,100,100,.05,.01)
    def test_rate_guard(self):
        with self.assertRaises(ValueError): check_call_calendar(self.calendar,100,100,-.01)
    def test_crossed(self):
        with self.assertRaises(ValueError): check_call_strikes([(90,3,2),(100,1,2)],100,1)
    def test_duplicate(self):
        with self.assertRaises(ValueError): check_call_strikes([(90,1,2),(90,1,2)],100,1)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): check_call_strikes([(90,float("nan"),2),(100,1,2)],100,1)
    def test_short(self):
        with self.assertRaises(ValueError): check_call_calendar([(1,1,2)],100,100)

if __name__=="__main__": unittest.main()
