"""Fault-detection checks for Section 14.8 computed-helper integration."""
from copy import deepcopy
import math
from unittest.mock import patch
import section_14_08 as report
from section_14_01 import eigenpairs_symmetric_2x2
from section_14_05 import solve_2x2
from section_14_06 import diagonal_exposure_svd
from section_14_07 import low_rank_diagonal_exposure

def validate(value):
    for key in ("eigen_reconstruction_error","eigen_orthogonality_error",
                "cholesky_reconstruction_error","cholesky_solve_residual","svd_reconstruction_error"):
        assert abs(value[key]) <= 1e-12,key
    assert math.isclose(value["low_rank_frobenius_error"],2,abs_tol=1e-12)
    assert value["calculation_source"]=="computed_teaching_helpers"

def run():
    for name,helper in (("eigenpairs_symmetric_2x2",eigenpairs_symmetric_2x2),
                        ("solve_2x2",solve_2x2),("diagonal_exposure_svd",diagonal_exposure_svd),
                        ("low_rank_diagonal_exposure",low_rank_diagonal_exposure)):
        with patch.object(report,name,wraps=helper,create=True) as called:
            result=report.assessment()
            assert called.call_count==1,name
            validate(result)
    faults=(
        ("eigenpairs_symmetric_2x2",eigenpairs_symmetric_2x2,"eigenvectors",((1.,0.),(0.,1.))),
        ("solve_2x2",solve_2x2,"solution",(0.,0.)),
        ("diagonal_exposure_svd",diagonal_exposure_svd,"right_singular_directions",((2.,0.),(0.,1.))),
        ("low_rank_diagonal_exposure",low_rank_diagonal_exposure,"approximation",((0.,0.),(0.,0.),(0.,0.))),
    )
    for name,helper,key,bad in faults:
        def corrupt(*args,helper=helper,key=key,bad=bad,**kwargs):
            result=deepcopy(helper(*args,**kwargs));result[key]=bad;return result
        with patch.object(report,name,side_effect=corrupt):
            try:
                validate(report.assessment())
            except AssertionError:
                pass
            else:
                raise AssertionError("undetected wrong helper output: "+name)
    def corrupt_factor(*args,**kwargs):
        result=deepcopy(solve_2x2(*args,**kwargs))
        result["factorization"]["factor"]=((1.,0.),(0.,1.))
        return result
    with patch.object(report,"solve_2x2",side_effect=corrupt_factor):
        try:
            validate(report.assessment())
        except AssertionError:
            pass
        else:
            raise AssertionError("undetected wrong Cholesky factor")
    print("PASS: four computed-helper calls and five corrupted-output detections")

if __name__=="__main__":
    run()
