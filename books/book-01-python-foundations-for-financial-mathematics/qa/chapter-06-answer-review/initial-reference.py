"""Standalone acceptance checks for all twenty Chapter 6 problems."""
import unittest
import numpy as np


class ChapterSixSolutions(unittest.TestCase):
    def test_problem_01(self):
        a=np.array([100,102,99],dtype=np.float64)
        self.assertEqual(a.shape,(3,))
        self.assertEqual(a.ndim,1)
        self.assertEqual(a.dtype,np.float64)

    def test_problem_02(self):
        a=np.array([1,2]); a[0]=1.75
        self.assertEqual(a[0],1)
        b=np.array([1,2],dtype=np.float64); b[0]=1.75
        self.assertEqual(b[0],1.75)

    def test_problem_03(self):
        a=np.array([100.,101.,102.]); b=a[1:]; b[0]=0
        self.assertEqual(a[1],0)
        c=a[1:].copy(); c[0]=9
        self.assertEqual(a[1],0)
        self.assertFalse(np.shares_memory(a,c))

    def test_problem_04(self):
        q=np.array([10,-5,0.]); p0=np.array([100,80,50.]); p1=np.array([105,76,52.])
        np.testing.assert_array_equal(q*(p1-p0),[50,20,0])

    def test_problem_05(self):
        p=np.array([[110,95],[80,105.]])
        r=p/np.array([100,100.])-1
        np.testing.assert_allclose(r,[[.1,-.05],[-.2,.05]],rtol=0,atol=1e-12)

    def test_problem_06(self):
        r=np.array([[.1,-.05],[-.2,.05]])
        np.testing.assert_allclose(r.mean(axis=1),[.025,-.075],rtol=0,atol=1e-12)
        np.testing.assert_allclose(r.mean(axis=0),[-.05,0],rtol=0,atol=1e-12)

    def test_problem_07(self):
        c=np.array([100,100,1100.]); t=np.array([1,2,3])
        pv=np.sum(c/1.05**t)
        expected=100/1.05+100/1.05**2+1100/1.05**3
        self.assertAlmostEqual(pv,expected,places=10)

    def test_problem_08(self):
        p=np.array([100.,110.,99.]); r=p[1:]/p[:-1]-1
        np.testing.assert_allclose(r,[.1,-.1],rtol=0,atol=1e-12)
        self.assertAlmostEqual(np.prod(1+r)-1,-.01)

    def test_problem_09(self):
        v=np.array([600.,300.,100.]); w=v/v.sum()
        np.testing.assert_allclose(w,[.6,.3,.1],rtol=0,atol=1e-12)
        self.assertAlmostEqual(w@np.array([.1,-.05,0]),.045)

    def test_problem_10(self):
        r=np.array([[.1,-.05,0],[-.2,.05,0]])
        w=np.array([[.6,.3,.1],[0,1,0]])
        np.testing.assert_allclose(r@w.T,[[.045,-.05],[-.105,.05]],rtol=0,atol=1e-12)

    def test_problem_11(self):
        a=np.array([[2.,1.],[1.,3.]]); b=np.array([5.,5.])
        x=np.linalg.solve(a,b)
        np.testing.assert_allclose(x,[2,1],rtol=0,atol=1e-12)
        np.testing.assert_allclose(a@x,b,rtol=0,atol=1e-12)

    def test_problem_12(self):
        with self.assertRaises(np.linalg.LinAlgError):
            np.linalg.solve([[1.,2.],[2.,4.]],[3.,6.])

    def test_problem_13(self):
        a=np.random.Generator(np.random.PCG64(42)); b=np.random.Generator(np.random.PCG64(42))
        x=a.standard_normal(5); y=b.standard_normal(5)
        np.testing.assert_array_equal(x,y)
        self.assertFalse(np.array_equal(x,a.standard_normal(5)))

    def test_problem_14(self):
        r=np.full(3,1e-17)
        self.assertEqual(np.prod(1+r)-1,0)
        self.assertAlmostEqual(float(np.expm1(np.log1p(r).sum()))/3e-17,1,places=14)

    def test_problem_15(self):
        a=np.ones((2,1)); b=np.ones(2)
        self.assertTrue(np.allclose(a,b))
        self.assertNotEqual(a.shape,b.shape)

    def test_problem_16(self):
        a=np.array([1.,np.nan,np.inf])
        np.testing.assert_array_equal(np.isfinite(a),[True,False,False])
        self.assertFalse(np.isfinite(a).all())

    def test_problem_17(self):
        a=np.zeros((1000,20),dtype=np.float64)
        self.assertEqual(a.nbytes,160000)

    def test_problem_18(self):
        q=[10.,-5.,0.]; a=[100.,80.,50.]; b=[105.,76.,52.]
        python_result=[x*(z-y) for x,y,z in zip(q,a,b)]
        numpy_result=(np.asarray(q)*(np.asarray(b)-np.asarray(a))).tolist()
        np.testing.assert_allclose(python_result,numpy_result,rtol=0,atol=1e-12)

    def test_problem_19(self):
        q=np.array([6.,3.,1.]); p0=np.full(3,100.); p1=np.array([[110,95,100],[80,105,100],[100,100,100.]])
        v=q*p0; total=v.sum(); ends=p1@q; r=(p1/p0-1)@(v/total)
        np.testing.assert_allclose(ends,[1045,895,1000],rtol=0,atol=1e-10)
        np.testing.assert_allclose(ends-total,total*r,rtol=1e-12,atol=1e-10)

    def test_problem_20(self):
        r=np.array([.1,-.05,0]); w=np.array([.6,.3,.1]); order=[2,0,1]
        self.assertAlmostEqual(r[order]@w[order],r@w)
        self.assertAlmostEqual(r@w[::-1],-.005)
        self.assertFalse(np.isclose(r@w[::-1],r@w))


if __name__ == "__main__":
    unittest.main()
