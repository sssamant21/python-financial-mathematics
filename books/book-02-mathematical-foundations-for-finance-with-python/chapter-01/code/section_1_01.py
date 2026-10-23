from math import isclose, isfinite


def compound_value(principal, period_rate, periods):
    """Fixed effective period rate; whole periods; no intermediate cash flows.

    Built-in int/float money and rate inputs only; bool is rejected.
    This is a teaching kernel, not a contractual rounding implementation.
    """
    for name, value in (("principal", principal), ("period_rate", period_rate)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a built-in real numeric input")
        try:
            finite = isfinite(value)
        except OverflowError as exc:
            raise ValueError(f"{name} exceeds the supported range") from exc
        if not finite:
            raise ValueError(f"{name} must be finite")
    if type(periods) is not int:
        raise TypeError("periods must be a built-in integer, excluding bool")
    if principal < 0 or period_rate <= -1 or periods < 0:
        raise ValueError("require principal>=0, period_rate>-1, periods>=0")
    if principal == 0:
        return 0.0
    try:
        factor = (1 + period_rate)**periods
        result = principal * factor
    except OverflowError as exc:
        raise ArithmeticError("result exceeds supported numeric range") from exc
    if not isfinite(result) or result == 0:
        raise ArithmeticError("nonzero value overflowed or underflowed")
    return result


def main():
    principal, rate, periods = 1000.0, 0.05, 2
    compound = compound_value(principal, rate, periods)
    simple = principal * (1 + rate * periods)
    recovered = compound / (1 + rate)**periods
    end_fee = compound_value(1000, rate, 1) - 10
    upfront_fee = compound_value(990, rate, 1)
    assert isclose(compound, 1102.5, rel_tol=1e-12)
    assert isclose(simple, 1100.0, rel_tol=1e-12)
    assert isclose(recovered, principal, rel_tol=1e-12)
    assert isclose(end_fee, 1040.0, rel_tol=1e-12)
    assert isclose(upfront_fee, 1039.5, rel_tol=1e-12)
    print(f"Compound value: {compound:.2f}")
    print(f"Simple-interest value: {simple:.2f}")
    print(f"Recovered principal: {recovered:.2f}")
    print(f"Fee at year end: {end_fee:.2f}")
    print(f"Fee before growth: {upfront_fee:.2f}")


if __name__ == "__main__":
    main()
