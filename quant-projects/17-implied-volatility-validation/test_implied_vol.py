import unittest
from implied_vol import bounds,price,implied_vol
class Tests(unittest.TestCase):
    def test_call(self):
        self.assertAlmostEqual(implied_vol("call",100,100,1,.05,price("call",100,100,1,.05,.2)),.2,places=6)
    def test_put(self):
        self.assertAlmostEqual(implied_vol("put",90,100,.5,.03,price("put",90,100,.5,.03,.35,.02),.02),.35,places=6)
    def test_bounds(self):
        self.assertEqual(bounds("call",100,100,1,0),(0,100))
    def test_lower_rejected(self):
        with self.assertRaises(ValueError): implied_vol("put",100,100,1,0,0)
    def test_upper_rejected(self):
        with self.assertRaises(ValueError): implied_vol("call",100,100,1,0,100)
    def test_bracket_rejected(self):
        with self.assertRaises(ValueError): implied_vol("call",100,100,1,0,price("call",100,100,1,0,.8),high=.2)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): implied_vol("call",100,100,1,0,float("nan"))
    def test_iteration_limit(self):
        with self.assertRaises(ArithmeticError): implied_vol("call",100,100,1,0,price("call",100,100,1,0,.237),iterations=1,tol=1e-12)
if __name__=="__main__": unittest.main()
