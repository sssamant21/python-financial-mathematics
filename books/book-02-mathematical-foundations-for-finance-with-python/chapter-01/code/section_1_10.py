"""Exact rate normalization and two declared simple-interest day counts."""
from datetime import date
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def decimal_rate(value, *, representation):
    divisors = {"decimal": 1, "percent": 100, "basis_points": 10000}
    if representation not in divisors:
        raise ValueError("unknown rate representation")
    return rational(value) / divisors[representation]


def year_fraction(start, end, *, convention):
    if type(start) is not date or type(end) is not date:
        raise TypeError("use date objects, not timestamps or strings")
    if end < start:
        raise ValueError("end must not precede start")
    denominators = {"ACT/360": 360, "ACT/365F": 365}
    if convention not in denominators:
        raise ValueError("unsupported day-count convention")
    return Fraction((end - start).days, denominators[convention])


def simple_accrual(*, principal, currency, rate, representation,
                   start, end, convention):
    if (type(currency) is not str or len(currency) != 3
            or any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in currency)):
        raise ValueError("currency must be an uppercase three-letter label")
    p = rational(principal)
    if p < 0:
        raise ValueError("this lab requires nonnegative principal")
    r = decimal_rate(rate, representation=representation)
    alpha = year_fraction(start, end, convention=convention)
    return {"currency": currency, "decimal_rate": r,
            "year_fraction": alpha, "interest": p * r * alpha}


def main():
    print("Equivalent rate quotations:",
          decimal_rate("0.06", representation="decimal"),
          decimal_rate(6, representation="percent"),
          decimal_rate(600, representation="basis_points"))
    for convention in ("ACT/360", "ACT/365F"):
        report = simple_accrual(
            principal=10000, currency="USD", rate=6,
            representation="percent", start=date(2025, 1, 1),
            end=date(2025, 1, 31), convention=convention)
        print(f"{convention}: fraction={report['year_fraction']}, "
              f"interest={report['interest']} {report['currency']}")
    print("Leap interval:", year_fraction(date(2024, 2, 28),
          date(2024, 3, 1), convention="ACT/365F"))


if __name__ == "__main__":
    main()
