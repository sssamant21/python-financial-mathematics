"""Section 3.10 cumulative Chapter 03 reference assessment."""
from fractions import Fraction as F
from section_3_09 import explore, number
from section_3_08 import present_value
from section_3_07 import quadratic, discrete_shape

def rejects(exc, fn, *args, **kwargs):
    try: fn(*args, **kwargs)
    except exc: return
    raise AssertionError("expected " + exc.__name__)

def run():
    assert tuple(12*q-30 for q in range(6)) == (-30,-18,-6,6,18,30)
    assert F(2*10+5,2) == F(25,2)
    assert 2*F(10,2)+5 == 15
    assert F(24+40,8) == 8 and F(20+40,8) == F(15,2)
    assert 9*15 == 135 and 10*12 == 120 and 11*12 == 132
    assert quadratic(5,-1,10,-20) == 5
    assert discrete_shape([3,6,11,18,27])["strictly_convex_on_grid"]
    assert present_value(110,"1/10") == 100
    model = explore(price=25,unit_cost=15,fixed_cost=40,capacity=8,
                    expansion_after=5,expansion_cost=30)
    expected = ((0,0,40,-40),(1,25,55,-30),(2,50,70,-20),
                (3,75,85,-10),(4,100,100,0),(5,125,115,10),
                (6,150,160,-10),(7,175,175,0),(8,200,190,10))
    assert model["rows"] == expected
    assert model["break_even"] == (4,7)
    assert model["argmax"] == (5,8)
    assert model["maximum_profit"] == 10
    assert not model["nondecreasing"]
    for i,(_,revenue,cost,profit) in enumerate(model["rows"]):
        assert revenue-cost == profit
        if i: assert profit-model["rows"][i-1][3] == model["increments"][i-1]
    rejects(ValueError,explore,price=25,unit_cost=15,fixed_cost=40,capacity=-1)
    rejects(TypeError,number,0.1)
    print("PASS: Section 3.10 cumulative assessment")

if __name__ == "__main__": run()
