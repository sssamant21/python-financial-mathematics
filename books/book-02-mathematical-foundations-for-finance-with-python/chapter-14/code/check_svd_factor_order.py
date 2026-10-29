"""Selected factor-order reconstruction checks for the restricted 3x2 SVD."""
import math
from section_14_06 import diagonal_exposure_svd

def run():
    count = 0
    for first,second in ((3,2),(2,3),(2,2),(3,0),(0,3),(0,0)):
        for tolerance in (0.0,2.0):
            result = diagonal_exposure_svd(first,second,(6,4,5),tolerance)
            assert result["singular_values"] == tuple(sorted((first,second),reverse=True))
            left = result["left_singular_directions"]
            right = result["right_singular_directions"]
            # Directions stay in factor order: pair with original magnitudes,
            # never blindly zip them with the separately sorted value summary.
            for directions in (left,right):
                for i,u in enumerate(directions):
                    for j,v in enumerate(directions):
                        assert sum(x*y for x,y in zip(u,v)) == float(i==j)
            reconstructed = tuple(tuple(sum(magnitude*u[i]*v[j]
                                    for magnitude,u,v in zip((first,second),left,right))
                                    for j in range(2)) for i in range(3))
            assert reconstructed == result["matrix"]
            expected_positions = (6/first if first>tolerance else 0.0,
                                  4/second if second>tolerance else 0.0)
            assert result["positions"] == expected_positions
            expected_achieved = (first*expected_positions[0],second*expected_positions[1],0.0)
            assert result["achieved_exposure"] == expected_achieved
            residual = tuple(b-a for b,a in zip((6,4,5),expected_achieved))
            assert result["signed_residual"] == residual
            assert result["half_squared_residual"] == sum(x*x for x in residual)/2
            assert result["rank_at_tolerance"] == sum(x>tolerance for x in (first,second))
            expected_condition = max(first,second)/min(first,second) if min(first,second)>0 else None
            assert result["condition_number_full_column_rank"] == expected_condition
            count += 1
    assert count == 12
    print("PASS: twelve restricted SVD factor-order and truncation cases")

if __name__ == "__main__":
    run()
