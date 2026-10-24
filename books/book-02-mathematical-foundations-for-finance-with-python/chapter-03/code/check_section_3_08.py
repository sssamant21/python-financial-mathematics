"""Section 3.8: executable contract and invariant checks."""
from fractions import Fraction
from section_3_08 import rational, present_value, profit

def rejects(error, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")

def run():
    assert present_value(110, "1/10") == 100
    assert present_value(0, 0) == 0
    assert present_value(100, "-1/2") == 200
    assert profit(4, price=25, variable_cost=15, fixed_cost=40) == 0
    assert profit(0, price=25, variable_cost=15, fixed_cost=40) == -40
    for cash in (0, 1, 100, 110):
        for rate in ("-1/2", 0, "1/10", 2):
            assert present_value(cash, rate) * (1 + Fraction(rate)) == cash
            assert present_value(cash, 0) == cash
    for a in (0, 10, 110):
        for b in (0, 20, 100):
            assert present_value(a+b, "1/10") == (
                present_value(a, "1/10") + present_value(b, "1/10"))
    for quantity in range(0, 20):
        kw = dict(price=25, variable_cost=15, fixed_cost=40)
        p = profit(quantity, **kw)
        assert p + 40 == 10 * quantity
        assert profit(quantity+1, **kw) - p == 10
    rejects(ValueError, present_value, -1, 0)
    rejects(ValueError, present_value, 100, -1)
    rejects(ValueError, present_value, 100, -2)
    rejects(ValueError, profit, -1, price=25, variable_cost=15, fixed_cost=40)
    rejects(ValueError, profit, "1/2", price=25, variable_cost=15, fixed_cost=40)
    rejects(ValueError, profit, 1, price=25, variable_cost=15, fixed_cost=-1)
    rejects(TypeError, rational, 0.1)
    rejects(TypeError, rational, True)
    print("PASS: Section 3.8 reference checks")

if __name__ == "__main__":
    run()
