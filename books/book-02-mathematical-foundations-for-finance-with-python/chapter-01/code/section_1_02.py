from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP, localcontext
from fractions import Fraction
from math import isclose, isfinite


def payment_count(value):
    """Whole count only; bool and 3.0 are outside this interface."""
    if type(value) is not int:
        raise TypeError("count must be a built-in int, excluding bool")
    if value < 0:
        raise ValueError("count must be nonnegative")
    return value


def split_minor_units(total, recipients):
    """Nonnegative total; positive recipient count; earliest positions get remainder."""
    total = payment_count(total)
    recipients = payment_count(recipients)
    if recipients == 0:
        raise ValueError("at least one recipient required")
    base, remainder = divmod(total, recipients)
    return [base + (index < remainder) for index in range(recipients)]


def main():
    exact_third = Fraction(1, 3)
    assert 3 * exact_third == 1
    quoted_rate = Fraction("0.035")
    assert quoted_rate == Fraction(7, 200)
    rational_balance = Fraction(1000) * (1 + quoted_rate)
    assert rational_balance == 1035
    assert Fraction(0.1) != Fraction("0.1")
    assert isclose(0.1 + 0.2, 0.3, rel_tol=1e-12)
    assert isfinite(0.05) and not isfinite(float("nan"))
    assert isinstance(True, int)  # explains the explicit count policy
    with localcontext() as context:
        context.prec = 28
        context.rounding = ROUND_HALF_EVEN
        decimal_total = Decimal("0.1") + Decimal("0.2")
        assert decimal_total == Decimal("0.3")
        assert Decimal(0.1) != Decimal("0.1")
        rounded_third = Decimal(1) / Decimal(3)
        half_even = Decimal("2.685").quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        half_up = Decimal("2.685").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        assert half_even == Decimal("2.68")
        assert half_up == Decimal("2.69")
    allocation = split_minor_units(105, 2)
    assert allocation == [53, 52] and sum(allocation) == 105
    print(f"Exact rational third: {exact_third}")
    print(f"Quoted rate as fraction: {quoted_rate}")
    print(f"One-period rational balance: {rational_balance}")
    print(f"Decimal sum: {decimal_total}")
    print(f"Decimal third at precision 28: {rounded_third}")
    print(f"Half-even / half-up: {half_even} / {half_up}")
    print(f"Minor-unit allocation: {allocation}")


if __name__ == "__main__":
    main()
