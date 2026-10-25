"""Independent reference checks for Section 11.8."""
import math
from section_11_08 import Vector,Matrix,finite,broadcast_shape,market_value,portfolio_returns,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-10),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    assert broadcast_shape((4,3),(3,))==(4,3)
    assert broadcast_shape((4,1),(1,3))==(4,3)
    assert broadcast_shape((3,1),(3,))==(3,3)
    assert broadcast_shape((),(3,))==(3,)
    rejects(ValueError,broadcast_shape,(4,3),(4,))
    rejects(ValueError,broadcast_shape,(2,-1),(2,1))
    p=Vector(("A","B","C"),(100,50,25),"USD/share")
    q=Vector(("C","A","B"),(10,2,4),"shares")
    close(market_value(p,q),650)
    rejects(ValueError,market_value,p,Vector(("A","B","D"),(2,4,10),"shares"))
    rejects(ValueError,Vector,("A","A"),(1,2),"shares")
    rejects(TypeError,finite,True,"component")
    rejects(ValueError,Matrix,("D1",),("A","B"),((1,),),"simple_return")
    matrix=Matrix(("D1","D2"),("C","A","B"),
                  ((0.03,0.01,-0.02),(-0.01,0.02,0.01)),"simple_return")
    w=Vector(("A","B","C"),(0.5,0.3,0.2),"weight")
    returns=portfolio_returns(matrix,w)
    close(returns["D1"],0.005)
    close(returns["D2"],0.011)
    rejects(ValueError,portfolio_returns,matrix,Vector(("A","B","D"),(0.5,0.3,0.2),"weight"))
    report=assessment()
    close(report["market_value_USD"],650)
    close(report["portfolio_returns"]["DAY1"],0.005)
    close(report["portfolio_returns"]["DAY2"],0.011)
    assert report["runtime_certified"] is False
    print("PASS: Section 11.8 independent reference checks")

if __name__=="__main__":
    run()
