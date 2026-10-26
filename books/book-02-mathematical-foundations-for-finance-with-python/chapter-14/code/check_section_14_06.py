"""Independent checks for Book 02 Section 14.6."""
import math
from section_14_06 import diagonal_exposure_svd,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    result=assessment()
    p=result["reference"]
    assert p["rank_at_tolerance"]==2
    close(p["singular_values"][0],3)
    close(p["singular_values"][1],2)
    close(p["condition_number_full_column_rank"],1.5)
    for got,expected in zip(p["positions"],(2,2)):
        close(got,expected)
    for got,expected in zip(p["achieved_exposure"],(6,4,0)):
        close(got,expected)
    for got,expected in zip(p["signed_residual"],(0,0,5)):
        close(got,expected)
    close(p["half_squared_residual"],12.5)
    q=result["rank_deficient"]
    assert q["rank_at_tolerance"]==1
    assert q["condition_number_full_column_rank"] is None
    close(q["positions"][1],0)
    close(q["half_squared_residual"],20.5)
    small=diagonal_exposure_svd(3,1e-9,(6,4,5),rank_tolerance=1e-8)
    assert small["rank_at_tolerance"]==1
    close(small["positions"][1],0)
    zero=diagonal_exposure_svd(0,0,(0,0,5))
    assert zero["rank_at_tolerance"]==0
    close(zero["half_squared_residual"],12.5)
    rejects(ValueError,diagonal_exposure_svd,-1,2,(6,4,5))
    rejects(ValueError,diagonal_exposure_svd,3,2,(6,4))
    rejects(ValueError,diagonal_exposure_svd,3,2,(6,4,5),-0.1)
    rejects(ValueError,diagonal_exposure_svd,3,float("nan"),(6,4,5))
    assert not p["runtime_certified"]
    print("PASS: Section 14.6 independent reference checks")

if __name__=="__main__":
    run()
