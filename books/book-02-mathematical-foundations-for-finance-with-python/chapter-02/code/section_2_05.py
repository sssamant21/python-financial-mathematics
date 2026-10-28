"""Exact quadratic classification and optional Decimal root approximations."""
from decimal import Decimal, localcontext
from fractions import Fraction
from math import isqrt


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def rational_sqrt(value):
    if value < 0:
        raise ValueError("square root requires a nonnegative rational")
    numerator, denominator = isqrt(value.numerator), isqrt(value.denominator)
    if numerator * numerator == value.numerator and denominator * denominator == value.denominator:
        return Fraction(numerator, denominator)
    return None


def solve_quadratic(*, a, b, c):
    a, b, c = map(rational, (a, b, c))
    if a == 0:
        raise ValueError("a must be nonzero; use linear classification otherwise")
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return {"kind": "no_real", "discriminant": discriminant,
                "center": None, "spread_squared": None, "exact_roots": ()}
    center = -b / (2 * a)
    spread_squared = discriminant / (4 * a * a)
    spread = rational_sqrt(spread_squared)
    roots = None if spread is None else tuple(sorted({center - spread, center + spread}))
    return {"kind": "repeated" if discriminant == 0 else "two_real",
            "discriminant": discriminant, "center": center,
            "spread_squared": spread_squared, "exact_roots": roots}


def approximate_roots(*, a, b, c, precision=40):
    if type(precision) is not int or not 16 <= precision <= 100:
        raise ValueError("precision must be an integer from 16 to 100")
    result = solve_quadratic(a=a, b=b, c=c)
    def decimal_value(value):
        return Decimal(value.numerator) / Decimal(value.denominator)
    with localcontext() as context:
        context.prec = precision
        if result["exact_roots"] is not None:
            return tuple(decimal_value(root) for root in result["exact_roots"])
        center = decimal_value(result["center"])
        spread = decimal_value(result["spread_squared"]).sqrt()
        # Compute the root whose terms reinforce, then use the exact
        # product c/a to recover the other without subtractive cancellation.
        far = center - spread if center < 0 else center + spread
        other = decimal_value(rational(c) / rational(a)) / far
        return tuple(sorted((far, other)))


def main():
    factored = solve_quadratic(a=1, b=-5, c=6)
    repeated = solve_quadratic(a=1, b=-4, c=4)
    absent = solve_quadratic(a=1, b=0, c=1)
    print("Factored roots:", ", ".join(map(str, factored["exact_roots"])))
    print("Repeated root:", ", ".join(map(str, repeated["exact_roots"])))
    print("Negative discriminant:", absent["kind"])
    irrational = approximate_roots(a=1, b=0, c=-2)
    print("Irrational root approximations:", ", ".join(f"{x:.6f}" for x in irrational))
    profit = solve_quadratic(a="-0.1", b=10, c=-160)
    print("Break-even quantities:", ", ".join(map(str, profit["exact_roots"])))
    growth = solve_quadratic(a=1, b=2, c="-0.21")
    print("Growth rate candidates:", ", ".join(map(str, growth["exact_roots"])))
    allowed = [rate for rate in growth["exact_roots"] if rate > -1]
    print("Admissible growth rates:", ", ".join(map(str, allowed)))


if __name__ == "__main__":
    main()
