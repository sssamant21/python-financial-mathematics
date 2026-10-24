"""Exact two-equation systems and synthetic one-period allocation."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use int, rational string, or Fraction")
    return Fraction(value)


def row(values):
    values = tuple(values)
    if len(values) != 3:
        raise ValueError("a row must contain a, b, c")
    return tuple(rational(value) for value in values)


def residuals(first, second, point):
    first, second = row(first), row(second)
    point = tuple(point)
    if len(point) != 2:
        raise ValueError("a point must contain x, y")
    x, y = map(rational, point)
    return tuple(a*x + b*y - c for a, b, c in (first, second))


def solve_system(first, second):
    a, b, c = row(first)
    d, e, f = row(second)
    determinant = a*e - d*b
    if determinant:
        point = ((c*e - f*b)/determinant,
                 (a*f - d*c)/determinant)
        return {"kind": "unique", "point": point}
    if (a == b == 0 and c != 0) or (d == e == 0 and f != 0):
        return {"kind": "none"}
    if a == b == d == e == 0:
        return {"kind": "all_pairs"}
    if a == b == 0:
        a, b, c, d, e, f = d, e, f, a, b, c
    if a*f != d*c or b*f != e*c:
        return {"kind": "none"}
    zero = Fraction(0)
    base = (zero, c/b) if b else (c/a, zero)
    return {"kind": "line", "base": base, "direction": (b, -a)}


def allocation(*, budget, rate_one, rate_two, interest):
    budget, r1, r2, interest = map(
        rational, (budget, rate_one, rate_two, interest))
    if budget < 0:
        raise ValueError("nonnegative allocation requires budget >= 0")
    first, second = (1, 1, budget), (r1, r2, interest)
    algebraic = solve_system(first, second)
    if algebraic["kind"] == "unique":
        point = algebraic["point"]
        feasible = "unique" if all(value >= 0 for value in point) else "empty"
        return {"algebraic": algebraic, "feasible": feasible,
                "residuals": residuals(first, second, point)}
    if algebraic["kind"] == "none":
        return {"algebraic": algebraic, "feasible": "empty"}
    # The nonzero budget row means the remaining case is a line.
    if budget == 0:
        return {"algebraic": algebraic, "feasible": "unique",
                "point": (Fraction(0), Fraction(0))}
    return {"algebraic": algebraic, "feasible": "segment",
            "x_interval": (Fraction(0), budget), "y_rule": "budget - x"}


def show(point):
    return "(" + ", ".join(str(value) for value in point) + ")"


def main():
    unique = solve_system((1, 1, 10), (2, -1, 2))
    print("Unique pair:", show(unique["point"]))
    line = solve_system((1, 1, 10), (2, 2, 20))
    print("Line: base", show(line["base"]),
          "direction", show(line["direction"]))
    print("Contradictory:", solve_system((1, 1, 10), (2, 2, 21))["kind"])
    print("Zero equations:", solve_system((0, 0, 0), (0, 0, 0))["kind"])
    for target in (52, 70):
        result = allocation(budget=1000, rate_one=".04",
                            rate_two=".06", interest=target)
        print(f"Interest {target}: {show(result['algebraic']['point'])}; "
              f"feasible={result['feasible']}; "
              f"residuals={show(result['residuals'])}")
    equal = allocation(budget=1000, rate_one=".05",
                       rate_two=".05", interest=50)
    print("Equal rates: feasible=" + equal["feasible"] +
          "; x in " + show(equal["x_interval"]) + "; y = budget - x")
    zero = allocation(budget=0, rate_one=".05", rate_two=".05", interest=0)
    print("Zero budget: algebraic=" + zero["algebraic"]["kind"] +
          "; feasible=" + zero["feasible"] + "; point=" + show(zero["point"]))


if __name__ == "__main__":
    main()
