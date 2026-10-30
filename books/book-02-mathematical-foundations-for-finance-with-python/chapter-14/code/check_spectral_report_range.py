"""Spectral report integration, iterator and tiny-diagnostic references."""
from decimal import Decimal, localcontext
import math
from section_14_02 import decompose

def run():
    # Section 14.2 delegates to Section 14.1, so retain the corrected tiny roots.
    for sign in (1,-1):
        for small in (2.0**-60,2.0**-200,math.ulp(0.0)):
            matrix=((sign,0),(0,sign*small))
            result=decompose(matrix)
            assert result["eigenvalues"] == tuple(sorted((sign,sign*small),reverse=True))
            assert result["reconstructed_matrix"] == matrix
    reference=decompose(((2,1),(1,2)))
    assert decompose(iter(((2,1),(1,2)))) == reference
    assert decompose((iter(row) for row in ((2,1),(1,2)))) == reference
    for invalid in (iter(((1,2),)),(iter(row) for row in ((1,2),(3,)))):
        try:
            decompose(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("malformed iterator accepted")
    # The unresolved-gap fallback has a small but nonzero reconstruction error.
    # Decimal sums squared represented differences without float underflow.
    for scale in (1.0,1e-100,1e-200):
        off=scale*1e-15
        matrix=((scale,off),(off,scale))
        result=decompose(matrix)
        differences=[matrix[i][j]-result["reconstructed_matrix"][i][j]
                     for i in range(2) for j in range(2)]
        with localcontext() as ctx:
            ctx.prec=100
            expected=float(sum((Decimal.from_float(x)**2 for x in differences),Decimal(0)).sqrt())
        assert expected > 0
        assert math.isclose(result["reconstruction_error_frobenius"],expected,rel_tol=3e-15,abs_tol=0)
    print("PASS: six tiny-root integrations, iterator guards and three Decimal diagnostic cases")

if __name__ == "__main__":
    run()
