"""Independent symmetric-quadratic references for covariance consumers."""
from fractions import Fraction as F
import math
from section_15_04 import covariance, portfolio_variance, portfolio_gradient
from section_15_06 import portfolio_hessian

def run():
    matrices=(((1e-12,0.0),(1e-14,1e-12)),
              ((0.04,0.01),(math.nextafter(0.01,1.0),0.09)),
              ((2.0,0.25),(0.25,3.0)))
    for matrix in matrices:
        a,b=matrix[0];c,d=matrix[1]
        off=float((F(b)+F(c))/2)
        sym=((a,off),(off,d))
        assert covariance(matrix)==sym
        hessian=portfolio_hessian(matrix)
        assert hessian[0][1]==hessian[1][0]
        assert hessian==tuple(tuple(2*v for v in row) for row in sym)
        for weights in ((1.,1.),(2.,-1.),(0.6,0.4)):
            w=tuple(map(F,weights))
            expected_gradient=tuple(float(2*sum((F(sym[i][j])*w[j] for j in range(2)),F(0))) for i in range(2))
            expected_variance=float(sum((w[i]*F(sym[i][j])*w[j] for i in range(2) for j in range(2)),F(0)))
            for actual,expected in zip(portfolio_gradient(matrix,weights),expected_gradient):
                assert math.isclose(actual,expected,rel_tol=2e-15,abs_tol=0)
            assert math.isclose(portfolio_variance(matrix,weights),expected_variance,rel_tol=2e-15,abs_tol=0)
    for matrix in (((1,0),(0,0)),((1,2),(2,1)),((1,0),(1e-10,1)),((1e308,0),(0,1e308))):
        for fn in (covariance,portfolio_hessian):
            try:
                fn(matrix)
            except ValueError:
                pass
            else:
                raise AssertionError("invalid or out-of-range covariance accepted")
    print("PASS: three symmetric-normalization cases, nine exact-quadratic references and shared PD/range rejection")

if __name__=="__main__":
    run()
