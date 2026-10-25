"""Independent reference checks for Section 12.5 rank classification."""
from section_12_05 import Matrix,Vector,finite,classify,assessment

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    result=assessment()
    assert (result["unique"]["rank_A"],result["unique"]["rank_augmented"])==(2,2)
    assert result["unique"]["classification"]=="unique"
    assert result["unique"]["free_variables"]==0
    assert (result["redundant_consistent"]["rank_A"],result["redundant_consistent"]["rank_augmented"])==(1,1)
    assert result["redundant_consistent"]["classification"]=="infinitely_many"
    assert result["redundant_consistent"]["free_variables"]==1
    assert (result["redundant_inconsistent"]["rank_A"],result["redundant_inconsistent"]["rank_augmented"])==(1,2)
    assert result["redundant_inconsistent"]["classification"]=="no_solution"
    a=Matrix(("E1","E2"),("X","Y"),((1,2),(2,4)),"standardized_sensitivity")
    b=Vector(("E1","E2"),(3,6),"standardized_exposure")
    c=Vector(("E2","E1"),(6,3),"standardized_exposure")
    assert classify(a,b)==classify(a,c)
    under=Matrix(("E1",),("X","Y"),((1,1),),"standardized_sensitivity")
    assert classify(under,Vector(("E1",),(4,),"standardized_exposure"))["classification"]=="infinitely_many"
    over=Matrix(("E1","E2"),("X",),((1,),(2,)),"standardized_sensitivity")
    assert classify(over,Vector(("E1","E2"),(2,4),"standardized_exposure"))["classification"]=="unique"
    assert classify(over,Vector(("E1","E2"),(2,5),"standardized_exposure"))["classification"]=="no_solution"
    rejects(ValueError,classify,a,Vector(("E1","WRONG"),(3,6),"standardized_exposure"))
    rejects(ValueError,classify,a,b,0)
    rejects(ValueError,Matrix,("E1","E1"),("X","Y"),((1,2),(2,4)),"standardized_sensitivity")
    rejects(ValueError,Matrix,("E1","E2"),("X","Y"),((1,2),(2,)),"standardized_sensitivity")
    rejects(ValueError,Vector,("E1",),(float("inf"),),"standardized_exposure")
    rejects(TypeError,finite,True,"value")
    assert result["unique"]["runtime_certified"] is False
    print("PASS: Section 12.5 independent reference checks")

if __name__=="__main__":
    run()
