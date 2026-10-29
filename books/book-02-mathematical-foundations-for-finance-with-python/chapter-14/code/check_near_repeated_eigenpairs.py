"""Selected repeated/near-repeated symmetric eigenpair references."""
import math
from section_14_01 import eigenpairs_symmetric_2x2

def run():
    for scale in (1.0, 1e100, 1e-100):
        for epsilon in (0.0, 2.0**-40, 2.0**-44, 2.0**-50):
            off = scale*epsilon
            matrix = ((scale,off),(off,scale))
            result = eigenpairs_symmetric_2x2(matrix)
            hi,lo = result["eigenvalues"]
            for actual,expected in zip((hi,lo),(scale+off,scale-off)):
                assert math.isclose(actual,expected,rel_tol=5e-16)
            vectors = result["eigenvectors"]
            assert math.isclose(sum(x*x for x in vectors[0]),1,abs_tol=1e-15)
            assert math.isclose(sum(x*x for x in vectors[1]),1,abs_tol=1e-15)
            assert abs(sum(x*y for x,y in zip(*vectors))) <= 1e-15
            for value,vector,reported in zip((hi,lo),vectors,result["eigenpair_residual_norms"]):
                x,y = vector
                direct = math.hypot(scale*x+off*y-value*x,off*x+scale*y-value*y)
                assert math.isclose(reported,direct,rel_tol=1e-15,abs_tol=0)
                assert direct/scale <= 1e-14
            # Above the documented gap cutoff, use sign-invariant projectors.
            if epsilon >= 2.0**-44:
                x,y = vectors[0]
                assert math.isclose(x*x,0.5,abs_tol=1e-15)
                assert math.isclose(y*y,0.5,abs_tol=1e-15)
                assert math.isclose(x*y,0.5,abs_tol=1e-15)
            else:
                # The implementation deliberately uses coordinate directions
                # for repeated or numerically unresolved gaps.
                assert vectors == ((1.0,0.0),(0.0,1.0))
            reconstructed = tuple(tuple(sum(value*v[i]*v[j] for value,v in zip((hi,lo),vectors))
                                        for j in range(2)) for i in range(2))
            assert max(abs(reconstructed[i][j]-matrix[i][j])/scale
                       for i in range(2) for j in range(2)) <= 1e-14
    print("PASS: twelve selected repeated/near-repeated eigenpair cases")

if __name__ == "__main__":
    run()
