from math import fsum, isclose, isfinite


def finite_amount(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be a built-in int or float, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds supported range") from exc
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def dated_payments(*, periods, amounts):
    """Finite iterables; nonnegative integer dates; signed, single-currency amounts."""
    records = []
    for period, amount in zip(periods, amounts, strict=True):
        if type(period) is not int:
            raise TypeError("period labels must be built-in integers, excluding bool")
        if period < 0:
            raise ValueError("period labels must be nonnegative")
        records.append((period, finite_amount(amount, "amount")))
    return tuple(records)


def periodic_payments(amounts, *, first_period=1):
    """Consecutive whole periods; preserve amount order and repeated amounts."""
    if type(first_period) is not int:
        raise TypeError("first_period must be a built-in integer, excluding bool")
    if first_period < 0:
        raise ValueError("first_period must be nonnegative")
    records = tuple(enumerate(amounts, start=first_period))
    return dated_payments(periods=(t for t, _ in records),
                          amounts=(c for _, c in records))


def present_value(*, periods, amounts, period_rate):
    """Constant effective period rate; empty schedule has value zero."""
    rate = finite_amount(period_rate, "period_rate")
    if rate <= -1:
        raise ValueError("period_rate must be greater than -1")
    records = dated_payments(periods=periods, amounts=amounts)
    terms = []
    for t, cash in records:
        if cash == 0:
            terms.append(0.0)
            continue
        try:
            factor = (1 + rate)**t
            if not isfinite(factor) or factor == 0:
                raise ArithmeticError("discount denominator outside supported range")
            value = cash / factor
        except OverflowError as exc:
            raise ArithmeticError("discount calculation exceeds supported range") from exc
        if not isfinite(value) or value == 0:
            raise ArithmeticError("nonzero payment overflowed or underflowed")
        terms.append(value)
    try:
        total = fsum(terms)
    except OverflowError as exc:
        raise ArithmeticError("schedule total exceeds supported range") from exc
    if not isfinite(total):
        raise ArithmeticError("schedule total must be finite")
    return total


def main():
    records = periodic_payments([100, 120], first_period=1)
    for position, (time, amount) in enumerate(records):
        print(f"Position {position} -> period {time}: {amount:.2f}")
    end_value = present_value(periods=[1, 2], amounts=[100, 120], period_rate=0.1)
    early_value = present_value(periods=[0, 1], amounts=[100, 120], period_rate=0.1)
    assert isclose(early_value, 1.1 * end_value, rel_tol=1e-12)
    print(f"End-period PV: {end_value:.6f}")
    print(f"One-period-earlier PV: {early_value:.6f}")
    repeated = dated_payments(periods=[1, 1, 2], amounts=[100, -5, 120])
    assert len(repeated) == 3
    print(f"Repeated-date records retained: {len(repeated)}")
    holdings, prices = {"A": 2, "B": 3}, {"B": 20, "A": 10}
    if holdings.keys() != prices.keys():
        raise ValueError("instrument labels do not match")
    labelled_value = fsum(holdings[label] * prices[label] for label in holdings)
    assert labelled_value == 80
    print(f"Value matched by instrument label: {labelled_value:.2f}")


if __name__ == "__main__":
    main()
