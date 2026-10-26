"""Independent reference checks for Book 02 Section 13.2."""
import math
from section_13_02 import finite,checked_labels,pivot_basis,achieved,assessment

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    report=assessment()
    basis=report["basis"]
    assert basis["rank"]==2 and basis["dimension"]==2
    assert basis["basis_instruments"]==["BOND_A","BOND_B"]
    assert basis["redundant_instruments"]==["BOND_C"]
    assert report["allocation_one"]==report["allocation_two"]=={"RATE":5.0,"CREDIT":1.0}
    assert not basis["runtime_certified"]
    factors=("RATE","CREDIT")
    reordered=pivot_basis(((4,2,1),(2,1,-1)),factors,("BOND_C","BOND_A","BOND_B"))
    assert reordered["rank"]==2
    assert pivot_basis(((1,2),(2,4)),factors,("A","B"))["rank"]==1
    assert pivot_basis(((0,0),(0,0)),factors,("A","B"))["rank"]==0
    assert pivot_basis(((1,0),(0,1)),factors,("A","B"))["rank"]==2
    rejects(ValueError,checked_labels,("A","A"),"instruments")
    rejects(ValueError,pivot_basis,((1,2),(3,)),factors,("A","B"))
    rejects(ValueError,achieved,((1,0),(0,1)),factors,("A","B"),{"A":1,"WRONG":2})
    rejects(ValueError,pivot_basis,((1,0),(0,float("nan"))),factors,("A","B"))
    rejects(TypeError,finite,True,"value")
    print("PASS: Section 13.2 independent reference checks")

if __name__=="__main__":
    run()
