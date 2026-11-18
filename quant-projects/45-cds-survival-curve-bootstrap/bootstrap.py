"""Synthetic CDS survival-curve bootstrap; educational, not market-standard."""
import math


def survival(t, hazards, maturities):
    if not math.isfinite(t) or t < 0 or len(hazards) != len(maturities):
        raise ValueError("invalid survival inputs")
    previous = cumulative = 0.0
    for h, end in zip(hazards, maturities):
        if not math.isfinite(h) or h < 0 or not math.isfinite(end) or end <= previous:
            raise ValueError("invalid hazard curve")
        cumulative += h * max(0.0, min(t, end) - previous)
        previous = end
    if t > previous:
        cumulative += hazards[-1] * (t - previous)
    return math.exp(-cumulative)


def par_spread(maturity, hazards, maturities, recovery=0.4, rate=0.02, frequency=4):
    if not (math.isfinite(maturity) and maturity > 0 and math.isfinite(rate)
            and -0.1 <= rate <= 1 and math.isfinite(recovery)
            and 0 <= recovery < 1 and isinstance(frequency, int)
            and 1 <= frequency <= 24):
        raise ValueError("invalid contract")
    steps = round(maturity * frequency)
    if abs(steps / frequency - maturity) > 1e-10 or steps < 1:
        raise ValueError("maturity must align with coupon grid")
    annuity = protection = 0.0
    prev = 1.0
    for i in range(1, steps + 1):
        t = i / frequency
        q = survival(t, hazards, maturities)
        df = math.exp(-rate * t)
        annuity += df * q / frequency
        protection += df * (prev - q) * (1 - recovery)
        prev = q
    if annuity <= 0:
        raise ValueError("zero premium annuity")
    return protection / annuity


def bootstrap(maturities, spreads, recovery=0.4, rate=0.02, frequency=4, max_hazard=5.0):
    if not maturities or len(maturities) != len(spreads):
        raise ValueError("mismatched quotes")
    hazards = []
    for i, (m, s) in enumerate(zip(maturities, spreads)):
        if (not math.isfinite(m) or m <= (maturities[i-1] if i else 0)
                or not math.isfinite(s) or s < 0):
            raise ValueError("invalid ordered quotes")
        def model(h):
            return par_spread(m, hazards + [h], maturities[:i+1],
                              recovery, rate, frequency)
        lo, hi = 0.0, max_hazard
        if model(lo) > s + 1e-12 or model(hi) < s - 1e-12:
            raise ValueError("quotes infeasible for nonnegative bounded hazards")
        for _ in range(80):
            mid = (lo + hi) / 2
            if model(mid) < s:
                lo = mid
            else:
                hi = mid
        hazards.append((lo + hi) / 2)
    return hazards


if __name__ == "__main__":
    tenors = [1, 2, 3]
    truth = [0.01, 0.025, 0.04]
    quotes = [par_spread(t, truth[:i+1], tenors[:i+1])
              for i, t in enumerate(tenors)]
    print("Synthetic tenors:", tenors)
    print("Synthetic quotes (bp):", [round(s * 10000, 3) for s in quotes])
    print("Recovered hazards:", [round(h, 6) for h in bootstrap(tenors, quotes)])
