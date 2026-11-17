"""Educational annual par-swap discount-factor bootstrap; standard library only."""
import argparse
import math


def bootstrap(par_rates):
    """Return annual D(1)..D(n) from annual-pay par rates and D(0)=1."""
    rates = tuple(par_rates)
    if not rates:
        raise ValueError("at least one annual par rate required")
    discounts = []
    running = 0.0
    for rate in rates:
        if not isinstance(rate, (int, float)) or isinstance(rate, bool) or not math.isfinite(rate):
            raise ValueError("rates must be finite real numbers")
        denominator = 1.0 + rate
        if denominator <= 0:
            raise ValueError("rate must exceed -100%")
        discount = (1.0 - rate * running) / denominator
        if not math.isfinite(discount) or discount <= 0:
            raise ValueError("quotes imply nonpositive or nonfinite discount factors")
        discounts.append(discount)
        running += discount
        if not math.isfinite(running):
            raise ValueError("discount-factor sum overflow")
    return tuple(discounts)


def reprice(discounts):
    """Implied annual-pay par swap rates for each maturity."""
    result = []
    annuity = 0.0
    for d in discounts:
        if not math.isfinite(d) or d <= 0:
            raise ValueError("discount factors must be positive and finite")
        annuity += d
        if not math.isfinite(annuity):
            raise ValueError("annuity overflow")
        result.append((1.0 - d) / annuity)
    return tuple(result)


def forwards(discounts):
    """One-year simple forwards for successive annual periods."""
    prev = 1.0
    result = []
    for d in discounts:
        if not math.isfinite(d) or d <= 0:
            raise ValueError("discount factors must be positive and finite")
        f = prev / d - 1.0
        if not math.isfinite(f):
            raise ValueError("forward overflow")
        result.append(f)
        prev = d
    return tuple(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rates", nargs="+", type=float, default=[0.03, 0.035, 0.04],
                        help="annual par swap quotes as decimals")
    args = parser.parse_args()
    ds = bootstrap(args.rates)
    for year, (d, f, s) in enumerate(zip(ds, forwards(ds), reprice(ds)), 1):
        print(f"year={year} discount={d:.9f} forward={f:.6%} repriced_par={s:.6%}")


if __name__ == "__main__":
    main()
