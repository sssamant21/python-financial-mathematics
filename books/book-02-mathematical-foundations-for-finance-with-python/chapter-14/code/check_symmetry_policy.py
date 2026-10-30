"""Adjacent symmetry-policy and averaging references for Chapter 14."""
import math
from fractions import Fraction as F
from section_14_01 import eigenpairs_symmetric_2x2 as eigenpairs
from section_14_02 import decompose
from section_14_05 import cholesky_2x2

def rejected(fn,matrix):
    try:
        fn(matrix)
    except ValueError as exc:
        assert "symmetric" in str(exc)
    else:
        raise AssertionError("asymmetry accepted")

def run():
    accepted=denied=0
    for scale in (1.0,2.0**20,2.0**-20):
        threshold=1e-12*max(1.0,scale)
        for delta in (math.nextafter(threshold,0.0),threshold,math.nextafter(threshold,math.inf)):
            matrix=((scale,0.0),(delta,scale))
            # Exact represented comparison isolates the inclusive float threshold.
            if F(delta)>F(threshold):
                rejected(eigenpairs,matrix)
                rejected(decompose,matrix)
                denied+=1
            else:
                off=float(F(delta)/2)
                symmetrized=((scale,off),(off,scale))
                result=eigenpairs(matrix)
                assert result == eigenpairs(symmetrized)
                assert result == eigenpairs(((scale,delta),(0.0,scale)))
                for actual,expected in zip(result["eigenvalues"],(scale+off,scale-off)):
                    assert math.isclose(actual,expected,rel_tol=5e-16)
                report=decompose(matrix)
                # Diagnostics measure error against ORIGINAL entries, including
                # the intentional symmetrization displacement.
                assert report["reconstruction_error_frobenius"] >= delta/math.sqrt(2)*(1-1e-3)
                accepted+=1
            rejected(cholesky_2x2,matrix)
    assert (accepted,denied)==(6,3)
    for b,c in ((math.ulp(0.0),math.ulp(0.0)),(math.ulp(0.0),0.0),
                (math.ulp(0.0),2*math.ulp(0.0))):
        off=float((F(b)+F(c))/2)
        result=eigenpairs(((0.0,b),(c,0.0)))
        assert result["eigenvalues"] == (off,-off)
    print("PASS: nine adjacent symmetry cases, exact-symmetry contrast and three subnormal averages")

if __name__ == "__main__":
    run()
