from fractions import Fraction


def rational(value):
    if type(value) is int or isinstance(value, Fraction):
        return Fraction(value)
    if type(value) is str:
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("invalid rational text") from exc
    raise TypeError("use int, Fraction, or rational text; bool/float are excluded")


def maximum_transaction_amount(*, fixed_fee, fee_rate, fee_budget, amount_cap):
    """Maximum feasible amount for nonnegative amounts and non-strict limits.

    Return None when the feasible set is empty. Zero is a valid maximum.
    """
    F, k, B, M = (rational(v) for v in
                  (fixed_fee, fee_rate, fee_budget, amount_cap))
    if min(F, k, B, M) < 0:
        raise ValueError("fee-policy parameters must be nonnegative")
    if F > B:
        return None
    if k == 0:
        return M
    return min(M, (B - F) / k)


def transaction_report(*, amount, fixed_fee, fee_rate, fee_budget, amount_cap):
    """Validate a proposal's domain, then report both policy constraints."""
    x = rational(amount)
    if x < 0:
        raise ValueError("transaction amount must be nonnegative")
    F, k, B, M = (rational(v) for v in
                  (fixed_fee, fee_rate, fee_budget, amount_cap))
    maximum = maximum_transaction_amount(fixed_fee=F, fee_rate=k,
                                          fee_budget=B, amount_cap=M)
    fee = F + k*x
    slacks = {"fee_budget": B - fee, "amount_cap": M - x}
    checks = {name: slack >= 0 for name, slack in slacks.items()}
    return {"fee": fee, "slacks": slacks, "checks": checks,
            "feasible": all(checks.values()), "maximum_amount": maximum}


def weight_band_member(*, weight, target, half_width):
    """Long-only scalar weight and exact policy band; not a full portfolio check."""
    w, a, epsilon = (rational(v) for v in (weight, target, half_width))
    if not 0 <= a <= 1 or epsilon < 0:
        raise ValueError("target must be in [0,1] and half_width nonnegative")
    return 0 <= w <= 1 and abs(w - a) <= epsilon


def main():
    policy = {"fixed_fee": 5, "fee_rate": "0.01",
              "fee_budget": 15, "amount_cap": 800}
    for amount in (800, 900):
        report = transaction_report(amount=amount, **policy)
        print(f"Amount {amount}: fee={report['fee']}, feasible={report['feasible']}")
        print(f"  fee slack={report['slacks']['fee_budget']}, "
              f"amount slack={report['slacks']['amount_cap']}")
    maximum = maximum_transaction_amount(**policy)
    assert maximum == 800
    print(f"Maximum feasible amount: {maximum}")
    empty = maximum_transaction_amount(fixed_fee=16, fee_rate="0.01",
                                        fee_budget=15, amount_cap=800)
    print(f"Fixed fee above budget: {empty}")
    boundary = weight_band_member(weight="0.6", target="0.5", half_width="0.1")
    outside = weight_band_member(weight="0.6001", target="0.5", half_width="0.1")
    assert boundary and not outside
    print(f"Weight 0.6 in band: {boundary}")
    print(f"Weight 0.6001 in band: {outside}")


if __name__ == "__main__":
    main()
