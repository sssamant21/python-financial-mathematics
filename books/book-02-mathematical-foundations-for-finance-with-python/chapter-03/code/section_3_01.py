"""Chapter 03 Section 3.1: exact function domain and range examples."""
from fractions import Fraction


def q(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("expected integer, rational string, or Fraction")
    return Fraction(value)


def profit(quantity, *, price, unit_cost, fixed_cost, whole_units=True):
    n, p, v, f = map(q, (quantity, price, unit_cost, fixed_cost))
    if n < 0 or p < 0 or v < 0 or f < 0:
        raise ValueError("quantity, price and costs must be nonnegative")
    if whole_units and n.denominator != 1:
        raise ValueError("quantity must be a whole number of items")
    return (p-v)*n-f


def discounted_value(cash_flow, rate):
    c, r = q(cash_flow), q(rate)
    if r <= -1:
        raise ValueError("one-period discount factor must be positive: rate > -1")
    return c/(1+r)


def attainable_profits(*, price, unit_cost, fixed_cost, capacity):
    cap = q(capacity)
    if cap < 0 or cap.denominator != 1:
        raise ValueError("capacity must be a nonnegative integer")
    return tuple(profit(n, price=price, unit_cost=unit_cost,
                        fixed_cost=fixed_cost) for n in range(int(cap)+1))


def classify_profit_range(*, price, unit_cost, fixed_cost):
    p, v, f = map(q, (price, unit_cost, fixed_cost))
    if min(p, v, f) < 0:
        raise ValueError("prices and costs must be nonnegative")
    margin = p-v
    if margin > 0:
        return {"kind": "discrete_increasing", "first": -f, "step": margin}
    if margin == 0:
        return {"kind": "singleton", "value": -f}
    return {"kind": "discrete_decreasing", "first": -f, "step": margin}


def main():
    print("Profit at 12 units:", profit(12, price=20, unit_cost=8, fixed_cost=60))
    print("Capacity-limited range:", attainable_profits(
        price=20, unit_cost=8, fixed_cost=60, capacity=4))
    print("Discounted value:", discounted_value(110, "0.10"))
    print("Unbounded-quantity range structure:",
          classify_profit_range(price=20, unit_cost=8, fixed_cost=60))


if __name__ == "__main__":
    main()
