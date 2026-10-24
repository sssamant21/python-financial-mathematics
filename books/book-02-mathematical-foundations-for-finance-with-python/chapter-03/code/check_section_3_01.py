"""Exact reference checks for Book 02 Section 3.1."""
from fractions import Fraction as F
from section_3_01 import (q, profit, discounted_value, attainable_profits,
                          classify_profit_range)


def raises(error, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def run():
    assert profit(12, price=20, unit_cost=8, fixed_cost=60) == 84
    assert profit(0, price=20, unit_cost=8, fixed_cost=60) == -60
    assert attainable_profits(price=20, unit_cost=8, fixed_cost=60,
                              capacity=4) == (-60, -48, -36, -24, -12)
    assert discounted_value(110, "0.10") == 100
    assert discounted_value(-110, "0.10") == -100
    assert classify_profit_range(price=20, unit_cost=8, fixed_cost=60) == {
        "kind": "discrete_increasing", "first": F(-60), "step": F(12)}
    assert classify_profit_range(price=8, unit_cost=8, fixed_cost=60) == {
        "kind": "singleton", "value": F(-60)}
    assert classify_profit_range(price=5, unit_cost=8, fixed_cost=60) == {
        "kind": "discrete_decreasing", "first": F(-60), "step": F(-3)}
    raises(ValueError, profit, -1, price=20, unit_cost=8, fixed_cost=60)
    raises(ValueError, profit, "1/2", price=20, unit_cost=8, fixed_cost=60)
    assert profit("1/2", price=20, unit_cost=8, fixed_cost=60,
                  whole_units=False) == -54
    raises(ValueError, discounted_value, 100, -1)
    raises(ValueError, discounted_value, 100, -2)
    raises(ValueError, attainable_profits, price=20, unit_cost=8,
           fixed_cost=60, capacity="3/2")
    raises(TypeError, q, True)
    raises(TypeError, q, 0.1)
    print("PASS: Section 3.1 reference checks")


if __name__ == "__main__":
    run()
