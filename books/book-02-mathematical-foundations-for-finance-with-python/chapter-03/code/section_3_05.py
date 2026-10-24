"""Section 3.5: exact piecewise fee and threshold models."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use int, rational string, or Fraction")
    return Fraction(value)


def nonnegative(value):
    value = rational(value)
    if value < 0:
        raise ValueError("input must be nonnegative")
    return value


def flat_tier_fee(amount):
    """Whole-transaction fee: 2 for amount <=100, else 5."""
    amount = nonnegative(amount)
    return Fraction(2) if amount <= 100 else Fraction(5)


def marginal_tier_fee(amount):
    """1% on first 100 currency units; 2% on excess above 100."""
    amount = nonnegative(amount)
    return amount*Fraction(1,100) if amount <= 100 else (
        Fraction(1)+ (amount-100)*Fraction(2,100))


def unit_price(quantity):
    """All-units volume price: 12 for 0..9 items, 10 for 10+ items."""
    quantity = nonnegative(quantity)
    if quantity.denominator != 1:
        raise ValueError("quantity must be a whole number")
    return Fraction(12) if quantity < 10 else Fraction(10)


def volume_revenue(quantity):
    quantity = nonnegative(quantity)
    return unit_price(quantity)*quantity


def step_fixed_cost(quantity):
    """Fixed cost 40 through 10 units, 70 for 11+ units."""
    quantity = nonnegative(quantity)
    if quantity.denominator != 1:
        raise ValueError("quantity must be a whole number")
    return Fraction(40) if quantity <= 10 else Fraction(70)


def step_profit(quantity, *, price=12, variable_cost=5):
    quantity = nonnegative(quantity)
    price, variable_cost = rational(price), rational(variable_cost)
    if price < 0 or variable_cost < 0:
        raise ValueError("price and variable cost must be nonnegative")
    return (price-variable_cost)*quantity-step_fixed_cost(quantity)


def main():
    for amount in ("99.99", "100", "100.01"):
        print("Amount", amount, "flat fee", flat_tier_fee(amount),
              "marginal fee", marginal_tier_fee(amount))
    for units in (9, 10, 11):
        print("Units", units, "revenue", volume_revenue(units),
              "step profit", step_profit(units))


if __name__ == "__main__":
    main()
