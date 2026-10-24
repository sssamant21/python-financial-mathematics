"""Section 3.8: contracts for exact financial functions."""
from fractions import Fraction

def rational(value):
    """Convert int, rational string or Fraction; reject floats and booleans."""
    if type(value) not in (int, str, Fraction):
        raise TypeError("expected int, rational string, or Fraction")
    return Fraction(value)

def present_value(cash_flow, rate):
    """One-period PV; require cash_flow >= 0 and rate > -1."""
    cash_flow, rate = rational(cash_flow), rational(rate)
    if cash_flow < 0 or rate <= -1:
        raise ValueError("require cash_flow >= 0 and rate > -1")
    return cash_flow / (1 + rate)

def profit(quantity, *, price, variable_cost, fixed_cost):
    """Exact profit; require nonnegative whole units and nonnegative parameters."""
    quantity, price, variable_cost, fixed_cost = map(
        rational, (quantity, price, variable_cost, fixed_cost))
    if quantity < 0 or quantity.denominator != 1:
        raise ValueError("quantity must be a nonnegative integer")
    if min(price, variable_cost, fixed_cost) < 0:
        raise ValueError("price and costs must be nonnegative")
    return (price - variable_cost) * quantity - fixed_cost

if __name__ == "__main__":
    print("PV:", present_value(110, "1/10"))
    print("Profit:", profit(4, price=25, variable_cost=15, fixed_cost=40))
