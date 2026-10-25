"""Independent reference checks for Section 11.3."""
import math
from section_11_03 import (Vector,finite,dot,market_value,gross_notional,
                           weighted_return,factor_pnl,assessment)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-9),(a,b)

def run():
    x=Vector(("A","B","C"),(2,3,4),"unit")
    y=Vector(("C","A","B"),(2,5,-1),"unit")
    close(dot(x,y),15)
    close(dot(x,y),dot(y,x))
    close(dot(x,x),29)
    z=Vector(("A","B","C"),(1,1,1),"unit")
    summed=Vector(x.labels,tuple(a+b for a,b in zip(x.values,y.align(x.labels).values)),"unit")
    close(dot(summed,z),dot(x,z)+dot(y,z))
    p=Vector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    q=Vector(("GAMMA","ALPHA","BETA"),(10,2,4),"shares")
    close(market_value(p,q),650)
    short=Vector(p.labels,(2,-4,10),"shares")
    close(market_value(p,short),250)
    close(gross_notional(p,short),650)
    w=Vector(p.labels,(0.5,0.3,0.2),"weight")
    returns=Vector(("GAMMA","ALPHA","BETA"),(0.04,0.02,-0.01),"simple_return")
    close(weighted_return(w,returns),0.015)
    s=Vector(("F1","F2"),(10000,-5000),"USD/factor_unit","factor")
    shocks=Vector(("F2","F1"),(-0.02,0.01),"factor_unit","factor")
    close(factor_pnl(s,shocks),200)
    rejects(ValueError,dot,x,Vector(("A","B","D"),(1,2,3),"unit"))
    rejects(ValueError,dot,x,Vector(x.labels,(1,2,3),"unit","time"))
    rejects(ValueError,weighted_return,Vector(p.labels,(0.5,0.3,0.1),"weight"),returns)
    rejects(ValueError,market_value,p,Vector(p.labels,(1,2,3),"USD"))
    rejects(ValueError,Vector,("A","A"),(1,2),"unit")
    rejects(TypeError,finite,True,"component")
    report=assessment()
    close(report["portfolio_value_USD"],650)
    close(report["weighted_simple_return"],0.015)
    close(report["linear_factor_pnl_USD"],200)
    assert report["runtime_certified"] is False
    print("PASS: Section 11.3 independent reference checks")

if __name__=="__main__":
    run()
