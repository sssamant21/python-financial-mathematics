"""Independent tiny Cholesky reconstruction-error references."""
from decimal import Decimal, localcontext
import math
from section_14_05 import cholesky_2x2, solve_2x2

def run():
    nonzero=0
    for scale in (1.0,1e-100,1e-180,1e-200,1e-250):
        matrix=((4*scale,2*scale),(2*scale,3*scale))
        result=cholesky_2x2(matrix)
        with localcontext() as ctx:
            ctx.prec=100
            differences=[Decimal.from_float(matrix[i][j])-Decimal.from_float(result["reconstructed_matrix"][i][j])
                         for i in range(2) for j in range(2)]
            expected=float(sum((x*x for x in differences),Decimal(0)).sqrt())
        assert math.isclose(result["reconstruction_error_frobenius"],expected,rel_tol=3e-15,abs_tol=0)
        if expected>0:
            nonzero+=1
            assert result["reconstruction_error_frobenius"]>0
        # The solve embeds the same factorization diagnostic.
        report=solve_2x2(matrix,(6*scale,5*scale))
        assert report["factorization"]==result
        for x in report["solution"]:
            assert math.isclose(x,1.0,rel_tol=3e-15)
    assert nonzero>=2
    print("PASS: five Decimal Cholesky norm cases and solve-report propagation")

if __name__=="__main__":
    run()
