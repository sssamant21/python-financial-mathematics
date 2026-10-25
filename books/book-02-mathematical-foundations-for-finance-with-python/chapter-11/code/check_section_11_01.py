"""Independent reference checks for Book 02 Section 11.1."""
import math
from section_11_01 import LabeledVector,finite,market_values,assessment

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    p=LabeledVector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    q=LabeledVector(("GAMMA","ALPHA","BETA"),(10,2,4),"shares")
    assert q.align(p.labels).values==(2,4,10)
    assert q.labels==("GAMMA","ALPHA","BETA")
    values=market_values(p,q)
    assert values.values==(200,200,250)
    assert math.fsum(values.values)==650
    assert sum(a*b for a,b in zip(p.values,q.values))==1200
    assert q.align(("BETA","GAMMA","ALPHA")).values==(4,10,2)
    rejects(ValueError,LabeledVector,("A","A"),(1,2),"USD")
    rejects(ValueError,LabeledVector,("A","B"),(1,),"USD")
    rejects(ValueError,LabeledVector,("A",),(float("nan"),),"USD")
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,q.align,("GAMMA","ALPHA","DELTA"))
    rejects(ValueError,market_values,p,LabeledVector(("ALPHA","BETA","GAMMA"),(2,4,10),"USD"))
    report=assessment()
    assert report["portfolio_total_USD"]==650
    assert report["invalid_positional_total_USD"]==1200
    assert report["runtime_certified"] is False
    print("PASS: Section 11.1 independent reference checks")

if __name__=="__main__":
    run()
