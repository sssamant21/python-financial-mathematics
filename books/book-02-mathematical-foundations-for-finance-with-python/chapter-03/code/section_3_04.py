"""Section 3.4: exact inverse functions with explicit domains."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("expected int, rational string, or Fraction")
    return Fraction(value)


def affine_inverse(y, *, slope, intercept):
    y, a, b = map(rational, (y, slope, intercept))
    if a == 0:
        return {"kind": "all" if y == b else "none"}
    return {"kind": "unique", "x": (y-b)/a}


def profit(quantity, *, price, unit_cost, fixed_cost):
    n, p, v, f = map(rational, (quantity, price, unit_cost, fixed_cost))
    if n < 0 or min(p, v, f) < 0:
        raise ValueError("quantity, price and costs must be nonnegative")
    return (p-v)*n-f


def quantity_from_profit(target, *, price, unit_cost, fixed_cost,
                         whole_units=True):
    t, p, v, f = map(rational, (target, price, unit_cost, fixed_cost))
    if min(p, v, f) < 0:
        raise ValueError("price and costs must be nonnegative")
    result = affine_inverse(t, slope=p-v, intercept=-f)
    if result["kind"] != "unique":
        return result
    n = result["x"]
    if n < 0:
        return {"kind": "outside_domain", "algebraic_quantity": n}
    if whole_units and n.denominator != 1:
        return {"kind": "not_in_range", "algebraic_quantity": n}
    assert profit(n, price=p, unit_cost=v, fixed_cost=f) == t
    return {"kind": "unique", "quantity": n}


def present_value(future_cash_flow, rate):
    c, r = map(rational, (future_cash_flow, rate))
    if c <= 0 or r <= -1:
        raise ValueError("require future cash flow > 0 and rate > -1")
    return c/(1+r)


def rate_from_present_value(future_cash_flow, pv):
    c, v = map(rational, (future_cash_flow, pv))
    if c <= 0 or v <= 0:
        raise ValueError("require future cash flow > 0 and present value > 0")
    r = c/v-1
    assert present_value(c, r) == v
    return r


def restricted_square(x):
    x = rational(x)
    if x < 0:
        raise ValueError("restricted square domain is x >= 0")
    return x*x


def inverse_restricted_square(y):
    """Exact inverse on rational perfect squares; not a general sqrt."""
    y = rational(y)
    if y < 0:
        raise ValueError("square range is nonnegative")
    from math import isqrt
    n, d = isqrt(y.numerator), isqrt(y.denominator)
    if n*n != y.numerator or d*d != y.denominator:
        return {"kind": "irrational_or_unrepresented", "input": y}
    return {"kind": "unique", "x": Fraction(n, d)}


def main():
    print("Quantity for profit 80:",
          quantity_from_profit(80, price=20, unit_cost=10, fixed_cost=100))
    print("Rate recovered:", rate_from_present_value(110, 100))
    print("Restricted square inverse:", inverse_restricted_square("9/4"))


if __name__ == "__main__":
    main()
