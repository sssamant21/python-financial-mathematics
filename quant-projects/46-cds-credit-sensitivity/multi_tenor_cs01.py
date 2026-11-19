"""Synthetic multi-tenor quote CS01; simplified coupon-end settlement, not ISDA."""
import math


def _num(x, name, lo, hi):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or not lo <= x <= hi:
        raise ValueError(f"{name} outside [{lo}, {hi}]")
    return float(x)


def _validate(tenors, quotes, recovery, rate, frequency):
    if not isinstance(tenors, (tuple, list)) or not isinstance(quotes, (tuple, list)) or not tenors or len(tenors) != len(quotes) or len(tenors) > 20:
        raise ValueError("expected 1..20 matched tenors and quotes")
    rec = _num(recovery, "recovery", 0, .999999)
    r = _num(rate, "rate", -.1, 1)
    if isinstance(frequency, bool) or not isinstance(frequency, int) or not 1 <= frequency <= 24:
        raise ValueError("invalid coupon frequency")
    previous = 0.
    for t, q in zip(tenors, quotes):
        t = _num(t, "tenor", 1 / frequency, 30)
        _num(q, "quote_bp", 0, 100000)
        if t <= previous or abs(t * frequency - round(t * frequency)) > 1e-9:
            raise ValueError("tenors must increase and align to coupon dates")
        previous = t
    return rec, r


def survival(t, tenors, hazards):
    previous = integral = 0.
    for end, h in zip(tenors, hazards):
        integral += h * max(0., min(t, end) - previous)
        previous = end
    if t > previous:
        integral += hazards[-1] * (t - previous)
    return math.exp(-integral)


def legs(maturity, tenors, hazards, recovery=.4, rate=.02, frequency=4):
    a = p = 0.
    prior = 1.
    for k in range(1, round(maturity * frequency) + 1):
        t = k / frequency
        q = survival(t, tenors, hazards)
        d = math.exp(-rate * t)
        a += d * q / frequency
        p += d * (prior - q) * (1 - recovery)
        prior = q
    return a, p


def calibrate(tenors, quotes_bp, recovery=.4, rate=.02, frequency=4, max_hazard=5.):
    _validate(tenors, quotes_bp, recovery, rate, frequency)
    cap = _num(max_hazard, "max_hazard", 1e-12, 5)
    hazards = []
    for i, (t, q) in enumerate(zip(tenors, quotes_bp)):
        target = q / 10000
        def spread(h):
            a, p = legs(t, tenors[:i+1], hazards + [h], recovery, rate, frequency)
            return p / a
        if spread(0) > target + 1e-12 or spread(cap) < target - 1e-12:
            raise ValueError("infeasible quote curve")
        lo, hi = 0., cap
        for _ in range(65):
            mid = (lo + hi) / 2
            if spread(mid) < target:
                lo = mid
            else:
                hi = mid
        hazards.append((lo + hi) / 2)
    return hazards


def bucket_cs01(tenors=(1, 3, 5), quotes_bp=(60, 100, 140), maturity=5,
                coupon_bp=100, bump_bp=1, notional=1_000_000,
                recovery=.4, rate=.02, frequency=4):
    """Return PV and one-bp quote derivatives by rebootstrap of each tenor."""
    _validate(tenors, quotes_bp, recovery, rate, frequency)
    m = _num(maturity, "maturity", 1 / frequency, 30)
    if abs(m * frequency - round(m * frequency)) > 1e-9 or m > tenors[-1]:
        raise ValueError("maturity must align and not exceed last tenor")
    coupon = _num(coupon_bp, "coupon_bp", 0, 10000) / 10000
    bump = _num(bump_bp, "bump_bp", .001, 100)
    n = _num(notional, "notional", .01, 1e12)
    def value(quotes):
        h = calibrate(tenors, quotes, recovery, rate, frequency)
        a, p = legs(m, tenors, h, recovery, rate, frequency)
        return n * (p - coupon * a)
    base = value(quotes_bp)
    buckets = []
    for i, quote in enumerate(quotes_bp):
        up = list(quotes_bp)
        up[i] += bump
        if up[i] > 100000:
            raise ValueError("quote bump exceeds bound")
        upper = value(up)
        if quote >= bump:
            down = list(quotes_bp)
            down[i] -= bump
            delta = (upper - value(down)) / (2 * bump)
            method = "central"
        else:
            delta = (upper - base) / bump
            method = "forward"
        buckets.append({"tenor": tenors[i], "cs01": delta, "method": method})
    return {"pv": base, "hazards": calibrate(tenors, quotes_bp, recovery, rate, frequency),
            "buckets": buckets, "parallel_sum": sum(b["cs01"] for b in buckets)}


if __name__ == "__main__":
    print(bucket_cs01())
