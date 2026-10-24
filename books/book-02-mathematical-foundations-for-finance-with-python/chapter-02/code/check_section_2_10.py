"""Chapter 02 Section 2.10 exact exercise acceptance checks."""
from fractions import Fraction as F
from section_2_09 import model, profit, solve_quantity, minimum_quantity, solve_price


def run():
    assert 3*(2*(-2)-5)-2*((-2)+4) == 4*(-2)-23
    assert 5*(2*5-3) == 3*5+20
    x = F(7, 2)
    assert (x+1)/(x-2) == 3
    assert {r for r in (-7, 7) if r*r == 49} == {-7, 7}
    assert F(9)**3 == 27**2
    assert all(q*q-7*q+12 == 0 for q in (3, 4))
    assert all(t*t+4*t+8 > 0 for t in (-2, 0, 2))
    assert -3*4+12 == 0 and -3*5+12 < 0
    assert abs(95-100) == abs(105-100) == 5
    assert 20+30 == 50 and 2*20+3*30 == 130
    assert -50+150 == 100 and F(4,100)*(-50)+F(6,100)*150 == 7
    m = model(price=25, variable_cost=15, fixed_cost=1200)
    assert solve_quantity(m)["quantity"] == 120
    assert solve_quantity(m, 255)["quantity"] == F(291, 2)
    assert solve_quantity(m, 255, whole_units=True)["kind"] == "no_integer_solution"
    assert minimum_quantity(m, 255)["quantity"] == 146
    assert profit(m, 145) < 255 <= profit(m, 146)
    assert solve_price(quantity=150, variable_cost=15, fixed_cost=1200,
                       target_profit=300)["price"] == 25
    assert 12*100-50 == 1150
    assert F(2)*0+F(3)*0-13 == -13
    assert F(1,1000)*(F(2)*0+F(3)*0-13) == F(-13,1000)
    case = model(price=18, variable_cost=12, fixed_cost=900)
    assert solve_quantity(case)["quantity"] == 150
    assert minimum_quantity(case, 125)["quantity"] == 171
    assert profit(case, 170) == 120 and profit(case, 171) == 126
    assert solve_price(quantity=200, variable_cost=12, fixed_cost=900,
                       target_profit=300)["price"] == 18
    assert solve_quantity(model(price=18, variable_cost=18, fixed_cost=900))["kind"] == "none"
    print("PASS: Section 2.10 reference checks")


if __name__ == "__main__":
    run()
