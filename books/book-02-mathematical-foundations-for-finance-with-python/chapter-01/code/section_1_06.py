from fractions import Fraction


def rational(value):
    """Exact rational input policy; numeric strings are parsed explicitly."""
    if type(value) is int or isinstance(value, Fraction):
        return Fraction(value)
    if type(value) is str:
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("invalid rational text") from exc
    raise TypeError("use int, Fraction, or rational text; bool/float are excluded")


def solve_linear_equation(*, a, b, c, d):
    """Classify a*x+b=c*x+d over the reals, with rational coefficients.

    Return ('unique', rational_solution), ('all', None), or ('none', None).
    Financial domains must be applied separately.
    """
    a, b, c, d = (rational(value) for value in (a, b, c, d))
    coefficient, target = a - c, d - b
    if coefficient == 0:
        return ("all", None) if target == 0 else ("none", None)
    return "unique", target / coefficient


def equation_residual(*, a, b, c, d, x):
    a, b, c, d, x = (rational(value) for value in (a, b, c, d, x))
    return (a*x + b) - (c*x + d)


def original_quotient(x):
    """Evaluate (x*x-1)/(x-1) without removing the original exclusion."""
    x = rational(x)
    if x == 1:
        raise ValueError("original quotient excludes x=1")
    return (x*x - 1) / (x - 1)


def main():
    principal, rate = Fraction(1000), Fraction("0.05")
    value = principal * (1 + rate)**2
    print(f"Evaluated two-period expression: {float(value):.2f}")
    kind, solution = solve_linear_equation(a=100, b=100, c=0, d=110)
    assert kind == "unique" and solution == Fraction(1, 10)
    residual = equation_residual(a=100, b=100, c=0, d=110, x=solution)
    assert residual == 0 and solution > -1
    print(f"One-period rate solution: {solution}")
    print(f"Original-equation residual: {residual}")
    identity = solve_linear_equation(a=3, b=6, c=3, d=6)
    inconsistent = solve_linear_equation(a=3, b=6, c=3, d=7)
    print(f"Identical linear expressions: {identity[0]}")
    print(f"Inconsistent linear equation: {inconsistent[0]}")
    near_residual = equation_residual(a=100, b=100, c=0, d=110, x="0.0999")
    print(f"Residual at rate 0.0999: {near_residual}")
    assert near_residual == Fraction(-1, 100)
    for r in (Fraction(-1, 10), Fraction(0), Fraction(1, 20)):
        assert (1 + r)**2 == 1 + 2*r + r*r
    assert original_quotient(2) == 3


if __name__ == "__main__":
    main()
