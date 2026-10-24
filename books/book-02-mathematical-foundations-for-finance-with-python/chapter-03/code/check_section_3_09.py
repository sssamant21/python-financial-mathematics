"""Reference checks for Section 3.9 Financial Function Explorer."""
from fractions import Fraction as F
from section_3_09 import number, whole_nonnegative, explore, table

def rejects(error, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    baseline = explore(price=25, unit_cost=15, fixed_cost=40, capacity=8)
    assert len(baseline["rows"]) == 9
    assert baseline["rows"][0] == (0, 0, 40, -40)
    assert baseline["rows"][4] == (4, 100, 100, 0)
    assert baseline["rows"][8] == (8, 200, 160, 40)
    assert baseline["break_even"] == (4,)
    assert baseline["argmax"] == (8,)
    assert baseline["maximum_profit"] == 40
    assert baseline["minimum_profit"] == -40
    assert baseline["nondecreasing"] and baseline["concave_on_grid"]
    assert baseline["convex_on_grid"]
    assert baseline["increments"] == (F(10),)*8
    assert "4 | 100 | 100 | 0" in table(baseline)
    stepped = explore(price=25, unit_cost=15, fixed_cost=40, capacity=8,
                      expansion_after=5, expansion_cost=30)
    assert stepped["rows"][5] == (5, 125, 115, 10)
    assert stepped["rows"][6] == (6, 150, 160, -10)
    assert stepped["increments"][5] == -20
    assert not stepped["nondecreasing"]
    assert stepped["break_even"] == (4, 7)
    assert stepped["argmax"] == (5, 8)
    assert stepped["maximum_profit"] == 10
    assert not stepped["convex_on_grid"]
    assert not stepped["concave_on_grid"]
    assert explore(price=10, unit_cost=10, fixed_cost=0, capacity=2)["break_even"] == (0, 1, 2)
    assert explore(price=5, unit_cost=10, fixed_cost=20, capacity=2)["argmax"] == (0,)
    assert explore(price=10, unit_cost=5, fixed_cost=5, capacity=0)["rows"] == ((0, 0, 5, -5),)
    for result in (baseline, stepped):
        assert all(r - c == p for _, r, c, p in result["rows"])
        assert all(result["rows"][i+1][3]-result["rows"][i][3] == d
                   for i, d in enumerate(result["increments"]))
    rejects(ValueError, explore, price=-1, unit_cost=5, fixed_cost=0, capacity=2)
    rejects(ValueError, explore, price=10, unit_cost=5, fixed_cost=0, capacity="3/2")
    rejects(ValueError, explore, price=10, unit_cost=5, fixed_cost=0, capacity=2,
            expansion_after=-1)
    rejects(TypeError, number, 0.1)
    rejects(TypeError, number, True)
    print("PASS: Section 3.9 reference checks")

if __name__ == "__main__":
    run()
