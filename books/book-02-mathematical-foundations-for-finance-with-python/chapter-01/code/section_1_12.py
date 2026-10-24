"""Exact translation of a growth power and an indexed discounted sum."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def periodic_rate(value):
    rate = rational(value)
    if rate <= -1:
        raise ValueError("period rate must exceed -1")
    return rate


def compound_balance(*, principal, period_rate, periods):
    p = rational(principal)
    rate = periodic_rate(period_rate)
    if p < 0:
        raise ValueError("principal must be nonnegative")
    if type(periods) is not int:
        raise TypeError("periods must be an integer, excluding bool")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    growth_factor = 1 + rate
    return p * growth_factor ** periods


def present_value(*, cash_flows, period_rate):
    rate = periodic_rate(period_rate)
    if type(cash_flows) not in (list, tuple):
        raise TypeError("cash flows must be a list or tuple")
    if not cash_flows:
        raise ValueError("include at least the time-zero cash flow")
    flows = tuple(rational(value) for value in cash_flows)
    terms = tuple(cash_flow / (1 + rate) ** time
                  for time, cash_flow in enumerate(flows))
    return {"period_rate": rate, "cash_flows": flows,
            "discounted_terms": terms, "total": sum(terms, Fraction(0))}


def main():
    balance = compound_balance(principal=100, period_rate="0.10", periods=2)
    print(f"Compound balance: {balance}")
    report = present_value(cash_flows=(-100, 55, "60.5"), period_rate="0.10")
    for time, term in enumerate(report["discounted_terms"]):
        print(f"t={time}: discounted cash flow={term}")
    print(f"Time-zero value: {report['total']}")
    zero_rate = present_value(cash_flows=(-100, 55, "60.5"), period_rate=0)
    print(f"At zero rate: {zero_rate['total']}")
    print(f"Power versus XOR: {2 ** 3} versus {2 ^ 3}")


if __name__ == "__main__":
    main()
