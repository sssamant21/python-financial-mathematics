"""Section 3.3: exact composition of financial functions."""
from fractions import Fraction


def q(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use int, rational string, or Fraction")
    return Fraction(value)


def gross_after_fee(gross, fee):
    gross, fee = q(gross), q(fee)
    if gross < 0 or fee < 0 or fee > gross:
        raise ValueError("require gross >= fee >= 0")
    return gross-fee


def discount(cash_flow, rate):
    cash_flow, rate = q(cash_flow), q(rate)
    if rate <= -1:
        raise ValueError("discount rate must be greater than -1")
    return cash_flow/(1+rate)


def net_present_value(gross, fee, rate):
    """discount(gross_after_fee(gross, fee), rate)."""
    return discount(gross_after_fee(gross, fee), rate)


def discounted_gross_minus_fee(gross, fee, rate):
    """A different order: discount(gross, rate) minus fee paid now."""
    gross, fee = q(gross), q(fee)
    if gross < 0 or fee < 0 or fee > gross:
        raise ValueError("require gross >= fee >= 0")
    return discount(gross, rate)-fee


def compose(f, g):
    """Return f∘g; function contracts remain the responsibility of f and g."""
    return lambda x: f(g(x))


def affine(a, b):
    a, b = q(a), q(b)
    return lambda x: a*q(x)+b


def main():
    print("Net then discount:", net_present_value(110, 10, "0.10"))
    print("Discount gross then subtract current fee:",
          discounted_gross_minus_fee(110, 10, "0.10"))
    f, g = affine(2, 3), affine(4, 5)
    print("f(g(1)):", compose(f, g)(1))
    print("g(f(1)):", compose(g, f)(1))


if __name__ == "__main__":
    main()
