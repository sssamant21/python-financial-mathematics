import unittest
from implied_vol import price
from quote_validation import validate_quotes, iv_intervals

class QuoteTests(unittest.TestCase):
    def setUp(self):
        self.a=(100.,100.,1.,.05)
        self.c=price("call",*self.a,.2)
        self.p=price("put",*self.a,.2)
    def test_consistent(self):
        d=validate_quotes(*self.a,self.c-.02,self.c+.02,self.p-.02,self.p+.02)
        self.assertLessEqual(d["parity_interval"][0],d["parity"])
        self.assertGreaterEqual(d["parity_interval"][1],d["parity"])
    def test_iv_intervals(self):
        d=iv_intervals(*self.a,self.c-.02,self.c+.02,self.p-.02,self.p+.02)
        for lo,hi in d["iv_intervals"].values():
            self.assertLess(lo,.2)
            self.assertGreater(hi,.2)
    def test_crossed(self):
        with self.assertRaises(ValueError):
            validate_quotes(*self.a,self.c+.1,self.c-.1,self.p-.1,self.p+.1)
    def test_parity_violation(self):
        with self.assertRaises(ValueError):
            validate_quotes(*self.a,self.c+1,self.c+1.01,self.p-.01,self.p+.01)
    def test_negative(self):
        with self.assertRaises(ValueError):
            validate_quotes(*self.a,-1,1,self.p-.01,self.p+.01)
    def test_nonfinite(self):
        with self.assertRaises(ValueError):
            validate_quotes(*self.a,float("nan"),self.c+.02,self.p-.02,self.p+.02)
    def test_bounds(self):
        with self.assertRaises(ValueError):
            validate_quotes(*self.a,self.c-.02,200,self.p-.02,self.p+.02)
    def test_limiting_iv_refused(self):
        with self.assertRaises(ValueError):
            iv_intervals(*self.a,0,self.c+.02,self.p-.02,self.p+.02)
if __name__=="__main__": unittest.main()
