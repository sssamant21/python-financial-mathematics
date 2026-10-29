"""Selected dyadic near-SPD Cholesky references for Section 14.5."""
import math
from fractions import Fraction as F
from section_14_05 import cholesky_2x2, solve_2x2

def run():
    for scale in (1.0, 2.0**40, 2.0**-40):
        for delta in (2.0**-20, 2.0**-40, 2.0**-52):
            matrix = ((scale,scale),(scale,scale*(1+delta)))
            # Exact represented determinant and Schur complement.
            determinant = F(matrix[0][0])*F(matrix[1][1])-F(matrix[0][1])**2
            assert determinant == F(scale)**2*F(delta) > 0
            result = cholesky_2x2(matrix)
            (a,zero),(b,c) = result["factor"]
            assert zero == 0
            assert a == b == math.sqrt(scale)
            assert math.isclose(c,math.sqrt(scale*delta),rel_tol=2e-15)
            assert math.isclose(result["determinant_from_factor"],float(determinant),rel_tol=2e-15)
            for i in range(2):
                for j in range(2):
                    assert math.isclose(result["reconstructed_matrix"][i][j],matrix[i][j],
                                        rel_tol=2e-15,abs_tol=0)
            # Known x=(1,-1) gives exactly represented rhs=(0,-scale*delta).
            solved = solve_2x2(matrix,(0,-scale*delta))
            for actual,expected in zip(solved["solution"],(1,-1)):
                assert math.isclose(actual,expected,rel_tol=2e-15)
            assert solved["forward_solution"][0] == 0
            assert math.isclose(solved["forward_solution"][1],-math.sqrt(scale*delta),rel_tol=2e-15)
            assert solved["solve_residual_norm"]/scale <= 2e-15
        for lower in (1.0,math.nextafter(1.0,0.0)):
            matrix = ((scale,scale),(scale,scale*lower))
            assert F(matrix[0][0])*F(matrix[1][1])-F(matrix[0][1])**2 <= 0
            for fn,args in ((cholesky_2x2,(matrix,)),(solve_2x2,(matrix,(0,0)))):
                try:
                    fn(*args)
                except ValueError as exc:
                    assert "second pivot" in str(exc)
                else:
                    raise AssertionError("nonpositive exact pivot accepted")
    print("PASS: nine near-SPD factorizations/solves and six non-SPD boundary matrices")

if __name__ == "__main__":
    run()
