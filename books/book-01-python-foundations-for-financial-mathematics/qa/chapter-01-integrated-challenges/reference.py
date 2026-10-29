"""Supplemental challenge policies; applies only to new operations/refactored example."""
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_UP


def parse_decimal(text):
    if len(text.strip()) > 64:
        raise ValueError('Numeric text exceeds 64 characters')
    try:
        value = Decimal(text.strip())
    except InvalidOperation:
        raise ValueError('Enter decimal numeric text') from None
    if not value.is_finite():
        raise ValueError('Financial input must be finite')
    if value.copy_abs() > Decimal('1e18') or value.as_tuple().exponent < -12:
        raise ValueError('Input exceeds teaching precision/magnitude bounds')
    return value


def parse_periods(text):
    if len(text.strip()) > 4:
        raise ValueError('Periods outside 0..100')
    try:
        periods = int(text.strip())
    except ValueError:
        raise ValueError('Periods must be whole integer text') from None
    if not 0 <= periods <= 100:
        raise ValueError('Periods outside 0..100')
    return periods


def money(value):
    with localcontext() as context:
        context.prec = 40
        return value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)


def present_value(future_text, percent_text, periods_text):
    future = parse_decimal(future_text)
    percent = parse_decimal(percent_text)
    periods = parse_periods(periods_text)
    if future < 0:
        raise ValueError('Future receipt must be nonnegative')
    if not Decimal('-100') < percent <= Decimal('1000'):
        raise ValueError('Effective rate percent must be in (-100, 1000]')
    with localcontext() as context:
        context.prec = 40
        result = future / (1 + percent / 100) ** periods
        if result > Decimal("1e24"):
            raise ValueError("Present value exceeds teaching output bound 1e24")
        return result


def discount_amount(original_text, final_text):
    original, final = map(parse_decimal, (original_text, final_text))
    if not 0 <= final <= original:
        raise ValueError('Price reduction requires 0 <= final <= original')
    with localcontext() as context:
        context.prec = 40
        return original - final


def basis_points(text):
    bps = parse_decimal(text)
    with localcontext() as context:
        context.prec = 40
        return bps / 10000, bps / 100


def simple_interest(principal_text, percent_text, years_text):
    # Input parsing and model validation precede raw calculation.
    principal, percent, years = map(parse_decimal, (principal_text, percent_text, years_text))
    if principal <= 0 or not 0 <= years <= 100 or percent.copy_abs() > 1000:
        raise ValueError('Require principal > 0, years in [0,100], |rate percent| <= 1000')
    with localcontext() as context:
        context.prec = 40
        rate = percent / 100
        return principal * rate * years


def simple_interest_report(principal_text, percent_text, years_text):
    raw = simple_interest(principal_text, percent_text, years_text)
    posted = money(raw)  # Explicit final-only half-up cents policy.
    return raw, f'Interest: USD {posted:,.2f}'
