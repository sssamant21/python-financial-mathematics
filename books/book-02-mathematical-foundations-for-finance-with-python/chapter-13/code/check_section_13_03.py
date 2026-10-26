"""Independent reference checks for Book 02 Section 13.3."""
import math
from section_13_03 import finite,labels,analyze,achieved,assessment

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    result=assessment()
    spaces=result["spaces"]
    assert spaces["rank"]==2 and spaces["nullity"]==1
    assert spaces["column_space_basis_instruments"]==["BOND_A","BOND_B"]
    z=spaces["null_space_basis"][0]
    assert math.isclose(z["BOND_A"],-2,abs_tol=1e-10)
    assert math.isclose(z["BOND_B"],0,abs_tol=1e-10)
    assert math.isclose(z["BOND_C"],1,abs_tol=1e-10)
    factors=("RATE","CREDIT")
    instruments=("BOND_A","BOND_B","BOND_C")
    matrix=((2,1,4),(1,-1,2))
    assert achieved(matrix,factors,instruments,z)=={"RATE":0.0,"CREDIT":0.0}
    assert result["allocation_one"]==result["allocation_two"]=={"RATE":5.0,"CREDIT":1.0}
    assert result["rank_one"]["rank"]==1 and result["rank_one"]["nullity"]==1
    assert analyze(((0,0),(0,0)),factors,("A","B"))["nullity"]==2
    assert analyze(((1,0),(0,1)),factors,("A","B"))["nullity"]==0
    rejects(ValueError,labels,("RATE","RATE"),"factors")
    rejects(ValueError,analyze,((1,2),(3,)),factors,("A","B"))
    rejects(ValueError,achieved,((1,0),(0,1)),factors,("A","B"),{"A":1,"WRONG":2})
    rejects(ValueError,analyze,((1,0),(0,float("nan"))),factors,("A","B"))
    rejects(TypeError,finite,True,"value")
    assert not spaces["runtime_certified"]
    print("PASS: Section 13.3 independent reference checks")

if __name__=="__main__":
    run()
