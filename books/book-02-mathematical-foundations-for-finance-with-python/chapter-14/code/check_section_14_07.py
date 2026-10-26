"""Independent reference checks for Book 02 Section 14.7."""
import math
from section_14_07 import low_rank_diagonal_exposure,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    reports=assessment()
    r0,r1,r2=(reports["rank_"+str(i)] for i in range(3))
    close(r0["frobenius_error"],math.sqrt(20))
    close(r0["spectral_error"],4)
    close(r0["retained_squared_energy_fraction"],0)
    close(r1["frobenius_error"],2)
    close(r1["spectral_error"],2)
    close(r1["retained_squared_energy_fraction"],0.8)
    assert r1["approximation"]==((4.0,0.0),(0.0,0.0),(0.0,0.0))
    close(r2["frobenius_error"],0)
    close(r2["spectral_error"],0)
    close(r2["retained_squared_energy_fraction"],1)
    assert r2["actual_rank"]==2
    swapped=low_rank_diagonal_exposure(2,4,1)
    assert swapped["approximation"]==((0.0,0.0),(0.0,4.0),(0.0,0.0))
    tie=low_rank_diagonal_exposure(3,3,1)
    close(tie["frobenius_error"],3)
    zero=low_rank_diagonal_exposure(0,0,1)
    assert zero["retained_squared_energy_fraction"] is None
    assert zero["actual_rank"]==0
    rejects(ValueError,low_rank_diagonal_exposure,-1,2,1)
    rejects(ValueError,low_rank_diagonal_exposure,4,2,3)
    rejects(ValueError,low_rank_diagonal_exposure,4,2,True)
    rejects(ValueError,low_rank_diagonal_exposure,float("nan"),2,1)
    assert not r1["runtime_certified"]
    print("PASS: Section 14.7 independent reference checks")

if __name__=="__main__":
    run()
