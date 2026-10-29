"""Unequal-spectrum regression and independent Decimal root references."""
from decimal import Decimal, localcontext
import math
from section_14_01 import eigenpairs_symmetric_2x2

def run():
    # Every diagonal result is representable, including the smallest subnormal.
    count = 0
    for large in (1.0, 2.0**100, 2.0**-100):
        for small in (2.0**-60*large, math.ulp(0.0)):
            for sign in (1,-1):
                for swapped in (False,True):
                    diagonal = (sign*large,sign*small)
                    if swapped:
                        diagonal = diagonal[::-1]
                    result = eigenpairs_symmetric_2x2(((diagonal[0],0),(0,diagonal[1])))
                    assert result["eigenvalues"] == tuple(sorted(diagonal,reverse=True))
                    count += 1
    assert count == 24
    # Nonzero coupling and both trace signs; Decimal quadratic roots use
    # precision sufficient to resolve the small root independently.
    for sign in (1,-1):
        for scale in (1.0,2.0**80,2.0**-80):
            a,b,d = sign*scale, scale*2.0**-35, sign*scale*2.0**-60
            result = eigenpairs_symmetric_2x2(((a,b),(b,d)))
            with localcontext() as ctx:
                ctx.prec = 100
                aa,bb,dd = map(Decimal.from_float,(a,b,d))
                gap = ((aa-dd)**2+4*bb*bb).sqrt()
                expected = (float((aa+dd+gap)/2),float((aa+dd-gap)/2))
            for actual,reference in zip(result["eigenvalues"],expected):
                assert math.isclose(actual,reference,rel_tol=3e-15,abs_tol=0),(actual,reference)
            for value,vector in zip(result["eigenvalues"],result["eigenvectors"]):
                x,y=vector
                residual=math.hypot(a*x+b*y-value*x,b*x+d*y-value*y)
                assert residual/scale <= 2e-15
    print("PASS: 24 exact diagonal and six Decimal unequal-spectrum cases")

if __name__ == "__main__":
    run()
