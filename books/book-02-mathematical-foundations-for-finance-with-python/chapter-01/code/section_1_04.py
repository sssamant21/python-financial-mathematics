from math import fsum, isclose, isfinite


def finite_float(value):
    """Return a supported finite float, or None for an excluded input."""
    if type(value) not in (int, float):
        return None
    try:
        result = float(value)
    except OverflowError:
        return None
    return result if isfinite(result) else None


def interval_contains(value, lower, upper, *, left_closed=True, right_closed=True):
    """Finite bounds only; invalid configuration raises; excluded value returns False."""
    lo, hi = finite_float(lower), finite_float(upper)
    if lo is None or hi is None or lo > hi:
        raise ValueError("finite bounds with lower <= upper required")
    if type(left_closed) is not bool or type(right_closed) is not bool:
        raise TypeError("endpoint flags must be bool")
    x = finite_float(value)
    if x is None:
        return False
    left = x >= lo if left_closed else x > lo
    right = x <= hi if right_closed else x < hi
    return left and right


def discount_rate_member(value):
    """Finite real representation and strictly positive growth factor."""
    rate = finite_float(value)
    return rate is not None and rate > -1


def growth_domain_member(principal, rate, periods):
    amount = finite_float(principal)
    return (amount is not None and amount >= 0
            and discount_rate_member(rate)
            and type(periods) is int and periods >= 0)


def long_only_pair_member(first, second, *, budget_tol=1e-12):
    """Exact represented [0,1] bounds; approximate absolute budget check only."""
    tol = finite_float(budget_tol)
    if tol is None or tol < 0:
        raise ValueError("budget_tol must be finite and nonnegative")
    if not (interval_contains(first, 0, 1) and interval_contains(second, 0, 1)):
        return False
    total = fsum((finite_float(first), finite_float(second)))
    return isclose(total, 1.0, rel_tol=0.0, abs_tol=tol)


def main():
    first = {"USD", "EUR"}
    second = {"EUR", "JPY"}
    print(f"Intersection: {sorted(first & second)}")
    print(f"Union: {sorted(first | second)}")
    for rate in (-1.0, -0.05, 0.0):
        print(f"Discount rate {rate}: {discount_rate_member(rate)}")
    print(f"[0,1] contains 0: {interval_contains(0, 0, 1)}")
    print(f"(0,1) contains 0: {interval_contains(0, 0, 1, left_closed=False, right_closed=False)}")
    print(f"Growth triple (1000,0.05,2): {growth_domain_member(1000, 0.05, 2)}")
    print(f"Weights (0.4,0.6): {long_only_pair_member(0.4, 0.6)}")
    print(f"Weights (0.8,0.8): {long_only_pair_member(0.8, 0.8)}")
    assert interval_contains(1, 1, 1)
    assert not interval_contains(1, 1, 1, left_closed=False)
    assert not long_only_pair_member(-1e-15, 1.0)


if __name__ == "__main__":
    main()
