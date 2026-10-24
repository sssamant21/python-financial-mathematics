"""Exact algebraic scaling and validation, using rational arithmetic."""
from fractions import Fraction


def q(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use int, rational string, or Fraction")
    return Fraction(value)


def equation(a, b, c):
    """Represent ax + by = c."""
    return (q(a), q(b), q(c))


def scale(row, factor):
    """Scale an equation by a nonzero factor, preserving its solution set."""
    factor = q(factor)
    if factor == 0:
        raise ValueError("zero scaling destroys equation information")
    return tuple(factor * value for value in row)


def residual(row, x, y):
    a, b, c = row
    return a * q(x) + b * q(y) - c


def normalized_residual(row, x, y):
    """Dimensionless backward-error indicator, not a forward-error guarantee."""
    a, b, c = row
    x, y = q(x), q(y)
    denominator = abs(a*x) + abs(b*y) + abs(c)
    r = abs(residual(row, x, y))
    return r / denominator if denominator else Fraction(0)


def solve_one(a, b):
    """Solve ax=b exactly, including degenerate cases."""
    a, b = q(a), q(b)
    if a:
        return ("unique", b/a)
    return ("all", None) if b == 0 else ("none", None)


def cash_flow_balance(price, quantity, fee, revenue):
    """Residual in currency units: price*quantity - fee = revenue."""
    price, quantity, fee, revenue = map(q, (price, quantity, fee, revenue))
    return price*quantity - fee - revenue


def main():
    row = equation(2, 3, 13)
    point = (2, 3)
    print("Original residual:", residual(row, *point))
    print("Scaled residual:", residual(scale(row, "1/1000"), *point))
    print("Normalized residual:", normalized_residual(row, *point))
    print("Solve 4x=20:", solve_one(4, 20))
    print("Solve 0x=0:", solve_one(0, 0)[0])
    print("Cash-flow residual:", cash_flow_balance(12, 100, 50, 1150))


if __name__ == "__main__":
    main()
