"""Deterministic reference checks for the Chapter 02 break-even project."""
from fractions import Fraction
from section_2_09 import (rational, model, profit, solve_quantity,
                          minimum_quantity, solve_price)


def run():
    m = model(price=25, variable_cost=15, fixed_cost=1200)
    assert m["contribution"] == 10
    assert solve_quantity(m) == {"kind": "unique", "quantity": Fraction(120),
                                 "residual": Fraction(0)}
    assert profit(m, 120) == 0
    assert profit(m, 145) == 250
    result = minimum_quantity(m, 255)
    assert result["quantity"] == 146
    assert profit(m, 145) < 255 <= profit(m, 146)
    assert solve_quantity(m, 255, whole_units=True)["kind"] == "no_integer_solution"
    assert solve_quantity(m, 255)["quantity"] == Fraction(291, 2)
    assert solve_price(quantity=150, variable_cost=15, fixed_cost=1200,
                       target_profit=300)["price"] == 25
    assert solve_price(quantity=0, variable_cost=15, fixed_cost=1200,
                       target_profit=-1200)["kind"] == "all"
    assert solve_price(quantity=0, variable_cost=15, fixed_cost=1200,
                       target_profit=0)["kind"] == "none"
    zero = model(price=10, variable_cost=10, fixed_cost=0)
    assert solve_quantity(zero)["kind"] == "all"
    assert minimum_quantity(zero)["quantity"] == 0
    zero_cost = model(price=10, variable_cost=10, fixed_cost=100)
    assert solve_quantity(zero_cost)["kind"] == "none"
    assert minimum_quantity(zero_cost)["kind"] == "none"
    negative = model(price=5, variable_cost=8, fixed_cost=10)
    assert solve_quantity(negative)["kind"] == "outside_domain"
    assert minimum_quantity(negative)["kind"] == "none"
    assert minimum_quantity(negative, -10)["quantity"] == 0
    assert solve_quantity(m, -1300)["kind"] == "outside_domain"
    assert minimum_quantity(m, -1300)["quantity"] == 0
    assert solve_price(quantity=1, variable_cost=0, fixed_cost=10,
                       target_profit=-20)["kind"] == "outside_domain"
    for bad in (True, 0.1):
        try:
            rational(bad)
        except TypeError:
            pass
        else:
            raise AssertionError("invalid type accepted")
    for bad in (-1, "-1/2"):
        try:
            model(price=bad, variable_cost=0, fixed_cost=0)
        except ValueError:
            pass
        else:
            raise AssertionError("negative input accepted")
    # Invariant: all unique exact results satisfy the original equation.
    for price in (10, 20, 30):
        for cost in (0, 5, 15):
            mm = model(price=price, variable_cost=cost, fixed_cost=100)
            result = solve_quantity(mm)
            if result["kind"] == "unique":
                assert profit(mm, result["quantity"]) == 0
    print("PASS: Section 2.9 reference checks")


if __name__ == "__main__":
    run()
