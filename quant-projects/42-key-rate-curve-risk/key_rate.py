"""Educational key-rate PV01 with synthetic discount factors; standard library only."""
import argparse
import math

TENORS = (1.0, 2.0, 3.0, 4.0, 5.0)
ZERO_RATES = (0.025, 0.028, 0.030, 0.032, 0.034)
CASHFLOWS = (3.0, 3.0, 3.0, 3.0, 103.0)


def validate(tenors, rates, cashflows):
    if not (len(tenors) == len(rates) == len(cashflows)) or not tenors:
        raise ValueError("nonempty equal-length vectors required")
    if any(not math.isfinite(float(x)) for seq in (tenors, rates, cashflows) for x in seq):
        raise ValueError("all inputs must be finite")
    if any(t <= 0 or (i and t <= tenors[i - 1]) for i, t in enumerate(tenors)):
        raise ValueError("tenors must be strictly increasing and positive")
    if any(abs(r) > 1 for r in rates):
        raise ValueError("rates outside educational +/-100% bound")


def present_value(tenors, rates, cashflows):
    validate(tenors, rates, cashflows)
    terms = [cf * math.exp(-r * t) for t, r, cf in zip(tenors, rates, cashflows)]
    result = math.fsum(terms)
    if not math.isfinite(result):
        raise ValueError("PV overflow")
    return result


def key_rate_pv01(tenors, rates, cashflows, bump=0.0001):
    validate(tenors, rates, cashflows)
    if not math.isfinite(bump) or bump <= 0 or bump > 0.01:
        raise ValueError("bump must be in (0, 0.01]")
    sensitivities = []
    for i in range(len(rates)):
        up, down = list(rates), list(rates)
        up[i] += bump
        down[i] -= bump
        # Positive PV01 means PV falls when the corresponding zero rate rises.
        sensitivities.append((present_value(tenors, down, cashflows) -
                              present_value(tenors, up, cashflows)) / 2)
    return sensitivities


def parallel_pv01(tenors, rates, cashflows, bump=0.0001):
    validate(tenors, rates, cashflows)
    if not math.isfinite(bump) or bump <= 0 or bump > 0.01:
        raise ValueError("invalid bump")
    up = [r + bump for r in rates]
    down = [r - bump for r in rates]
    return (present_value(tenors, down, cashflows) -
            present_value(tenors, up, cashflows)) / 2


def main():
    parser = argparse.ArgumentParser(description="Synthetic key-rate PV01 demonstration")
    parser.add_argument("--bump-bp", type=float, default=1.0)
    args = parser.parse_args()
    bump = args.bump_bp / 10000
    pv = present_value(TENORS, ZERO_RATES, CASHFLOWS)
    buckets = key_rate_pv01(TENORS, ZERO_RATES, CASHFLOWS, bump)
    parallel = parallel_pv01(TENORS, ZERO_RATES, CASHFLOWS, bump)
    print(f"PV: {pv:.6f}")
    for tenor, value in zip(TENORS, buckets):
        print(f"{tenor:g}Y key-rate PV01: {value:.6f}")
    print(f"Parallel PV01: {parallel:.6f}; bucket sum: {sum(buckets):.6f}")


if __name__ == "__main__":
    main()
