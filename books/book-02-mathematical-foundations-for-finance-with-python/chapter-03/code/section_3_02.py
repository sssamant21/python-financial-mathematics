"""Section 3.2: exact graph coordinates and financial interpretation."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use integer, rational string, or Fraction")
    return Fraction(value)


def parameters(price, unit_cost, fixed_cost):
    p, v, f = map(rational, (price, unit_cost, fixed_cost))
    if min(p, v, f) < 0:
        raise ValueError("price and costs must be nonnegative")
    return p, v, f


def coordinates(price, unit_cost, fixed_cost, capacity):
    p, v, f = parameters(price, unit_cost, fixed_cost)
    n = rational(capacity)
    if n < 0 or n.denominator != 1:
        raise ValueError("capacity must be a nonnegative whole number")
    return tuple((q, p*q, f+v*q, (p-v)*q-f) for q in range(int(n)+1))


def break_even(price, unit_cost, fixed_cost):
    p, v, f = parameters(price, unit_cost, fixed_cost)
    m = p-v
    if m == 0:
        return ("all" if f == 0 else "none", None)
    quantity = f/m
    if quantity < 0:
        return ("outside_domain", quantity)
    return ("unique", quantity)


def slope_between(point_a, point_b):
    x1, y1 = map(rational, point_a)
    x2, y2 = map(rational, point_b)
    if x1 == x2:
        raise ValueError("vertical secant has undefined slope")
    return (y2-y1)/(x2-x1)


def render_ascii(price, unit_cost, fixed_cost, capacity):
    """Tabular graph coordinates: no plotting dependency or interpolated points."""
    rows = coordinates(price, unit_cost, fixed_cost, capacity)
    lines = ["q | revenue | cost | profit", "---|---------|------|-------"]
    lines += [f"{q} | {r} | {c} | {profit}" for q, r, c, profit in rows]
    return "\n".join(lines)


def main():
    print(render_ascii(25, 15, 40, 6))
    print("Break-even quantity:", break_even(25, 15, 40))
    print("Profit slope:", slope_between((0, -40), (4, 0)))


if __name__ == "__main__":
    main()
