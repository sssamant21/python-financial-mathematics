"""Independent reference checks for Section 12.5 rank classification."""
from section_12_05 import Matrix,Vector,finite,classify,assessment

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def rank_regressions():
    # Identity has exact rank two for every target; its unique solution is b.
    identity=Matrix(("E1","E2"),("X","Y"),((1,0),(0,1)),"standardized_sensitivity")
    for magnitude in (0,1e-200,1,1e200):
        r=classify(identity,Vector(("E1","E2"),(magnitude,-magnitude),"standardized_exposure"))
        assert (r["rank_A"],r["rank_augmented"],r["classification"])==(2,2,"unique")

    # Column 2 is twice column 1. Attainability requires b2=2*b1,
    # independent of the target magnitude or sign.
    dependent=Matrix(("E1","E2"),("X","Y"),((1,2),(2,4)),"standardized_sensitivity")
    for magnitude in (-1e200,-1,-1e-200,1e-200,1,1e200):
        for ratio,expected in ((2,"infinitely_many"),(3,"no_solution")):
            r=classify(dependent,Vector(("E1","E2"),(magnitude,ratio*magnitude),"standardized_exposure"))
            assert r["rank_A"]==1
            assert r["rank_augmented"]==(1 if ratio==2 else 2)
            assert r["classification"]==expected

    zero=Matrix(("E1","E2"),("X","Y"),((0,0),(0,0)),"standardized_sensitivity")
    for values,aug,status in (((0,0),0,"infinitely_many"),((0,1e-200),1,"no_solution")):
        r=classify(zero,Vector(("E1","E2"),values,"standardized_exposure"))
        assert (r["rank_A"],r["rank_augmented"],r["classification"])==(0,aug,status)

    # A deliberately chosen tolerance transition, not an exact-rank proof.
    near=Matrix(("E1","E2"),("X","Y"),((1,1),(1,1+1e-10)),"standardized_sensitivity")
    b=Vector(("E1","E2"),(0,0),"standardized_exposure")
    assert classify(near,b,1e-8)["rank_A"]==1
    assert classify(near,b,1e-12)["rank_A"]==2

    # Independently rescaling nonzero columns preserves their directions.
    scaled=Matrix(("E1","E2"),("X","Y"),((1e-200,0),(0,1e200)),"standardized_sensitivity")
    assert classify(scaled,b)["rank_A"]==2

def run():
    rank_regressions()
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
