"""Chapter 02 project: exact break-even and formula-rearrangement analyzer."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("expected int, rational string, or Fraction")
    return Fraction(value)


def model(*, price, variable_cost, fixed_cost):
    p, v, f = map(rational, (price, variable_cost, fixed_cost))
    if p < 0 or v < 0 or f < 0:
        raise ValueError("prices and costs must be nonnegative")
    return {"price": p, "variable_cost": v, "fixed_cost": f,
            "contribution": p-v}


def profit(m, quantity):
    q = rational(quantity)
    if q < 0:
        raise ValueError("quantity must be nonnegative")
    return m["contribution"]*q-m["fixed_cost"]


def solve_quantity(m, target_profit=0, *, whole_units=False):
    """Solve (price-variable_cost)*q-fixed_cost=target_profit."""
    target = rational(target_profit)
    margin, required = m["contribution"], m["fixed_cost"]+target
    if margin == 0:
        return {"kind": "all" if required == 0 else "none"}
    q = required/margin
    if q < 0:
        return {"kind": "outside_domain", "algebraic_quantity": q}
    if whole_units:
        # Exact equality with integer quantity; no rounding of target equations.
        if q.denominator != 1:
            return {"kind": "no_integer_solution", "algebraic_quantity": q}
    return {"kind": "unique", "quantity": q,
            "residual": profit(m, q)-target}


def minimum_quantity(m, target_profit=0, *, whole_units=True):
    """Find minimum nonnegative quantity achieving profit >= target."""
    target = rational(target_profit)
    margin, required = m["contribution"], m["fixed_cost"]+target
    if margin == 0:
        return {"kind": "minimum", "quantity": Fraction(0)} if required <= 0 else {"kind": "none"}
    if margin < 0:
        # Profit decreases as quantity rises; q=0 is the best feasible value.
        return {"kind": "minimum", "quantity": Fraction(0)} if required <= 0 else {"kind": "none"}
    q = max(Fraction(0), required/margin)
    if whole_units:
        q = Fraction(-(-q.numerator // q.denominator))
    return {"kind": "minimum", "quantity": q, "profit": profit(m, q)}


def solve_price(*, quantity, variable_cost, fixed_cost, target_profit=0):
    q, v, f, target = map(rational, (quantity, variable_cost, fixed_cost, target_profit))
    if q < 0 or v < 0 or f < 0:
        raise ValueError("quantity and costs must be nonnegative")
    if q == 0:
        return {"kind": "all" if target == -f else "none"}
    p = v+(f+target)/q
    if p < 0:
        return {"kind": "outside_domain", "algebraic_price": p}
    return {"kind": "unique", "price": p,
            "residual": (p-v)*q-f-target}


def show(value):
    return str(value)


def main():
    m = model(price=25, variable_cost=15, fixed_cost=1200)
    print("Contribution per unit:", show(m["contribution"]))
    print("Break-even:", solve_quantity(m))
    print("Minimum whole units for profit >= 255:", minimum_quantity(m, 255))
    print("Price for 150 units and profit 300:",
          solve_price(quantity=150, variable_cost=15,
                      fixed_cost=1200, target_profit=300))


if __name__ == "__main__":
    main()
