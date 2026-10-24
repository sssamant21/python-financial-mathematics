"""Section 3.9: Financial Function Explorer; standard-library, exact arithmetic."""
from fractions import Fraction

def number(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use int, rational string, or Fraction")
    return Fraction(value)

def whole_nonnegative(value, name):
    x = number(value)
    if x < 0 or x.denominator != 1:
        raise ValueError(f"{name} must be a nonnegative whole number")
    return int(x)

def explore(*, price, unit_cost, fixed_cost, capacity, expansion_after=None,
            expansion_cost=0):
    """Explore quantities 0..capacity; optional additional fixed cost after threshold.

    Parameters are nonnegative. expansion_after is an integer quantity threshold:
    additional cost applies only when q > expansion_after.
    Returns exact coordinates, bounds, extrema, differences and break-even points.
    """
    p, v, f, extra = map(number, (price, unit_cost, fixed_cost, expansion_cost))
    if min(p, v, f, extra) < 0:
        raise ValueError("prices and costs must be nonnegative")
    cap = whole_nonnegative(capacity, "capacity")
    threshold = None if expansion_after is None else whole_nonnegative(
        expansion_after, "expansion_after")
    rows = []
    for quantity in range(cap + 1):
        revenue = p * quantity
        cost = f + v * quantity + (extra if threshold is not None and quantity > threshold else 0)
        rows.append((quantity, revenue, cost, revenue - cost))
    profits = [row[3] for row in rows]
    increments = tuple(profits[i+1] - profits[i] for i in range(cap))
    minimum, maximum = min(profits), max(profits)
    return {
        "rows": tuple(rows),
        "minimum_profit": minimum,
        "maximum_profit": maximum,
        "argmin": tuple(i for i, x in enumerate(profits) if x == minimum),
        "argmax": tuple(i for i, x in enumerate(profits) if x == maximum),
        "break_even": tuple(i for i, x in enumerate(profits) if x == 0),
        "nonnegative_profit": tuple(i for i, x in enumerate(profits) if x >= 0),
        "increments": increments,
        "nondecreasing": all(x >= 0 for x in increments),
        "nonincreasing": all(x <= 0 for x in increments),
        "convex_on_grid": all(increments[i+1] >= increments[i] for i in range(len(increments)-1)),
        "concave_on_grid": all(increments[i+1] <= increments[i] for i in range(len(increments)-1))
    }

def table(result):
    lines = ["q | revenue | cost | profit", "---|---------|------|-------"]
    lines.extend(f"{q} | {r} | {c} | {p}" for q, r, c, p in result["rows"])
    return "\n".join(lines)

def main():
    baseline = explore(price=25, unit_cost=15, fixed_cost=40, capacity=8)
    print("BASELINE\n" + table(baseline))
    print("Break-even:", baseline["break_even"])
    print("Maximum:", baseline["maximum_profit"], "at", baseline["argmax"])
    stepped = explore(price=25, unit_cost=15, fixed_cost=40, capacity=8,
                      expansion_after=5, expansion_cost=30)
    print("\nCAPACITY EXPANSION\n" + table(stepped))
    print("Nondecreasing:", stepped["nondecreasing"])

if __name__ == "__main__":
    main()
