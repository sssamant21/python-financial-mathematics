"""Final assessment computed-helper and injected-fault checks."""
from copy import deepcopy
import math
from unittest.mock import patch
import section_14_10 as report
from section_14_01 import eigenpairs_symmetric_2x2
from section_14_05 import cholesky_2x2
from section_14_06 import diagonal_exposure_svd
from section_14_07 import low_rank_diagonal_exposure

def validate(value):
    assert value["eigenvalues"] == (3.0,1.0)
    assert value["eigen_reconstruction_error"] <= 1e-12
    assert value["cholesky_reconstruction_error"] <= 1e-12
    assert value["exposure_singular_values"] == (4.0,2.0)
    assert value["least_squares_positions"] == (2.0,2.0)
    assert math.isclose(value["rank_one_frobenius_error"],2,abs_tol=1e-12)
    assert value["calculation_source"]=="computed_teaching_helpers"

def run():
    helpers=(("eigenpairs_symmetric_2x2",eigenpairs_symmetric_2x2),
             ("cholesky_2x2",cholesky_2x2),("diagonal_exposure_svd",diagonal_exposure_svd),
             ("low_rank_diagonal_exposure",low_rank_diagonal_exposure))
    for name,helper in helpers:
        with patch.object(report,name,wraps=helper,create=True) as called:
            result=report.assessment()
            assert called.call_count==1,name
            validate(result)
    faults=(
        ("eigenpairs_symmetric_2x2",eigenpairs_symmetric_2x2,"eigenvalues",(4.,1.)),
        ("cholesky_2x2",cholesky_2x2,"factor",((1.,0.),(0.,1.))),
        ("diagonal_exposure_svd",diagonal_exposure_svd,"positions",(0.,0.)),
        ("diagonal_exposure_svd",diagonal_exposure_svd,"singular_values",(5.,2.)),
        ("low_rank_diagonal_exposure",low_rank_diagonal_exposure,"approximation",((0.,0.),(0.,0.),(0.,0.))),
    )
    for name,helper,key,bad in faults:
        def corrupt(*args,helper=helper,key=key,bad=bad,**kwargs):
            value=deepcopy(helper(*args,**kwargs));value[key]=bad;return value
        with patch.object(report,name,side_effect=corrupt):
            try:
                validate(report.assessment())
            except AssertionError:
                pass
            else:
                raise AssertionError("undetected final-assessment corruption: "+key)
    print("PASS: final assessment four helper calls and five corrupted-output detections")

if __name__=="__main__":
    run()
