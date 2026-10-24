"""Reference checks for Section 3.7."""
from fractions import Fraction as F
from section_3_07 import (q,quadratic,chord_gap,second_differences,
                          discrete_shape,total_cost,profit,best_integer_profit)

def rejects(error,fn,*args):
    try: fn(*args)
    except error: return
    raise AssertionError("expected "+error.__name__)

def run():
    assert quadratic(3,2,5,40)==73
    assert chord_gap(0,2,"1/2",1,0,0)==1
    assert chord_gap(0,2,"1/2",-1,0,0)==-1
    assert chord_gap(0,2,"1/2",0,3,2)==0
    assert second_differences([0,1,4,9])==(F(2),F(2))
    assert discrete_shape([0,1,4,9])["strictly_convex_on_grid"]
    assert discrete_shape([0,-1,-4,-9])["strictly_concave_on_grid"]
    assert discrete_shape([1,3,5,7])["convex_on_grid"]
    assert discrete_shape([1,3,5,7])["concave_on_grid"]
    assert total_cost(0)==40 and total_cost(3)==73
    assert profit(4)==8 and profit(5)==10 and profit(6)==8
    assert best_integer_profit(12)=={"maximum":F(10),"quantities":(5,)}
    assert best_integer_profit(4)=={"maximum":F(8),"quantities":(4,)}
    assert discrete_shape(total_cost(i) for i in range(8))["strictly_convex_on_grid"]
    assert discrete_shape(profit(i) for i in range(8))["strictly_concave_on_grid"]
    rejects(ValueError,chord_gap,0,2,"3/2",1,0,0)
    rejects(ValueError,second_differences,[1,2])
    rejects(ValueError,total_cost,"1/2")
    rejects(ValueError,best_integer_profit,-1)
    rejects(TypeError,q,True)
    rejects(TypeError,q,0.1)
    print("PASS: Section 3.7 reference checks")

if __name__=="__main__": run()
