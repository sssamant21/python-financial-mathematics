"""Selected exact-PD versus restricted float determinant-screen cases."""
from fractions import Fraction as F
import math
from section_15_04 import covariance
from section_15_06 import portfolio_hessian

def run():
    rejected=(
        ((2.0**-600,0.0),(0.0,2.0**-600)),
        ((2.0**600,0.0),(0.0,2.0**600)),
        ((math.nextafter(1.0,math.inf),1.0),(1.0,math.nextafter(1.0,0.0))),
    )
    for matrix in rejected:
        a,b=matrix[0];c,d=matrix[1]
        exact=F(a)*F(d)-F(b)*F(c)
        assert a>0 and exact>0
        determinant=a*d-b*c
        assert determinant==0 or not math.isfinite(determinant)
        for fn in (covariance,portfolio_hessian):
            try:
                fn(matrix)
            except ValueError:
                pass
            else:
                raise AssertionError("restricted determinant screen contract changed")
    for delta in (2.0**-20,2.0**-40,2.0**-52):
        matrix=((1.0,1.0),(1.0,1.0+delta))
        exact=F(matrix[0][0])*F(matrix[1][1])-F(1)
        assert exact==F(delta)>0
        assert covariance(matrix)==matrix
        assert portfolio_hessian(matrix)==tuple(tuple(2*x for x in row) for row in matrix)
    for diagonal in (1.0,math.nextafter(1.0,0.0)):
        matrix=((1.0,1.0),(1.0,diagonal))
        assert F(diagonal)-1<=0
        for fn in (covariance,portfolio_hessian):
            try:
                fn(matrix)
            except ValueError:
                pass
            else:
                raise AssertionError("singular/indefinite matrix accepted")
    print("PASS: three exact-PD range/cancellation exclusions, three accepted near-PD and two non-PD cases")

if __name__=="__main__":
    run()
