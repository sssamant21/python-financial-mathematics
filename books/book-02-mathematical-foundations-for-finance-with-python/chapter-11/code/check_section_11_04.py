"""Independent reference checks for Section 11.4."""
import math
from section_11_04 import Vector,finite,norm,difference,distance,relative_distance,assessment

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_relative_distance_contract():
    expected={"l1":0.7,"l2":5/math.sqrt(52),"linf":2/3}
    reversed_expected={"l1":7/3,"l2":5/math.sqrt(5),"linf":2}
    for scale in (1,2,-2,1e100,1e-100):
        actual=Vector(("A","B"),(scale,2*scale),"USD")
        benchmark=Vector(("B","A"),(6*scale,4*scale),"USD")
        zero=Vector(actual.labels,(0,0),"USD")
        for kind in ("l1","l2","linf"):
            close(relative_distance(actual,benchmark,kind),expected[kind])
            close(relative_distance(benchmark,actual,kind),reversed_expected[kind])
            assert relative_distance(actual,actual,kind)==0
            assert relative_distance(zero,benchmark,kind)==1
            rejects(ValueError,relative_distance,actual,zero,kind)
            rejects(ValueError,relative_distance,zero,zero,kind)
    # Smallest nonzero reference is not treated as a zero denominator.
    tiny=Vector(("A",),(5e-324,),"USD")
    zero=Vector(("A",),(0,),"USD")
    assert relative_distance(zero,tiny)==1
    rejects(ValueError,relative_distance,Vector(("A",),(1e308,),"USD"),
            Vector(("A",),(1e-308,),"USD"))
    actual=Vector(("A","B"),(1,2),"USD")
    rejects(ValueError,relative_distance,actual,Vector(actual.labels,(4,6),"EUR"))
    rejects(ValueError,relative_distance,actual,Vector(actual.labels,(4,6),"USD","factor"))
    rejects(ValueError,relative_distance,actual,Vector(("A","C"),(4,6),"USD"))
    rejects(ValueError,relative_distance,actual,actual,"unknown")
    report=assessment()
    assert report["deviation_USD"]=={"ALPHA":10000,"BETA":-10000,"GAMMA":-10000}
    close(report["relative_l2_distance"],math.sqrt(3/107))

def run():
    check_relative_distance_contract()
    v=Vector(("A","B","C"),(3,-4,12),"USD")
    close(norm(v,"l1"),19)
    close(norm(v,"l2"),13)
    close(norm(v,"linf"),12)
    zero=Vector(v.labels,(0,0,0),"USD")
    close(norm(zero),0)
    w=Vector(("C","A","B"),(12,3,-4),"USD")
    close(distance(v,w),0)
    x=Vector(("A","B"),(1,2),"USD")
    y=Vector(("B","A"),(6,4),"USD")
    close(distance(x,y,"l1"),7)
    close(distance(x,y,"l2"),5)
    close(distance(x,y,"linf"),4)
    scaled=Vector(v.labels,tuple(2*z for z in v.values),"USD")
    close(norm(scaled),2*norm(v))
    close(norm(difference(v,zero)),norm(v))
    rejects(ValueError,relative_distance,v,zero)
    rejects(ValueError,distance,v,Vector(v.labels,(1,2,3),"EUR"))
    rejects(ValueError,distance,v,Vector(("A","B","D"),(1,2,3),"USD"))
    rejects(ValueError,norm,v,"unknown")
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,Vector,("A","A"),(1,2),"USD")
    result=assessment()
    close(result["l1_distance_USD"],30000)
    close(result["l2_distance_USD"],10000*math.sqrt(3))
    close(result["linf_distance_USD"],10000)
    assert result["per_asset_limit_10000_USD_satisfied"]
    assert result["runtime_certified"] is False
    print("PASS: Section 11.4 independent reference checks")

if __name__=="__main__":
    run()
