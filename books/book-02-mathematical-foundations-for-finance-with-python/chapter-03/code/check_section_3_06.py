"""Reference checks for Section 3.6."""
from fractions import Fraction as F
from section_3_06 import rational,profit,all_units_revenue,analyze,bounded_profit

def raises(exc,fn,*args):
    try: fn(*args)
    except exc: return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=analyze([1,2,2,4])
    assert a["nondecreasing"] and not a["strictly_increasing"]
    assert a["minimum"]==1 and a["maximum"]==4
    assert a["argmin"]==(0,) and a["argmax"]==(3,)
    assert analyze([4,3,2])["strictly_decreasing"]
    assert analyze([3,3,3])["nondecreasing"]
    assert analyze([3,3,3])["nonincreasing"]
    assert not analyze([3,3,3])["strictly_increasing"]
    assert analyze([7])["minimum"]==7
    b=bounded_profit(20,12,40,6)
    assert b["minimum"]==-40 and b["maximum"]==8
    assert b["strictly_increasing"]
    c=bounded_profit(5,8,40,6)
    assert c["maximum"]==-40 and c["minimum"]==-58
    assert c["strictly_decreasing"]
    d=bounded_profit(8,8,40,6)
    assert d["minimum"]==d["maximum"]==-40
    assert d["argmax"]==tuple(range(7))
    assert all_units_revenue(9)==108 and all_units_revenue(10)==100
    assert not analyze(all_units_revenue(q) for q in range(12))["nondecreasing"]
    assert profit(6,20,12,40)==8
    raises(ValueError,analyze,[])
    raises(ValueError,bounded_profit,20,12,40,-1)
    raises(ValueError,profit,"1/2",20,12,40)
    raises(TypeError,rational,0.1)
    raises(TypeError,rational,True)
    print("PASS: Section 3.6 reference checks")

if __name__=="__main__":
    run()
