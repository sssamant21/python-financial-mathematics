"""Annualized dated cash-flow IRR, synthetic educational use only."""
from datetime import date, datetime
import math

def xirr(dates, cashflows, day_count=365.0):
    """Investor flows: initial negative, optional nonpositive deposits, positive final NAV."""
    if not isinstance(dates, (list, tuple)) or not isinstance(cashflows, (list, tuple)):
        raise ValueError("sequences required")
    if not 2 <= len(dates) <= 10000 or len(dates) != len(cashflows):
        raise ValueError("matching histories of 2..10000 required")
    if isinstance(day_count, bool) or not isinstance(day_count, (int, float)) or not math.isfinite(day_count) or day_count <= 0:
        raise ValueError("invalid day count")
    parsed = []
    for d in dates:
        if isinstance(d, date) and not isinstance(d, datetime):
            parsed.append(d)
        elif isinstance(d, str):
            try:
                parsed.append(date.fromisoformat(d))
            except ValueError as exc:
                raise ValueError("invalid ISO date") from exc
        else:
            raise ValueError("invalid date type")
    if any(b <= a for a, b in zip(parsed, parsed[1:])):
        raise ValueError("dates must increase strictly")
    values = []
    for v in cashflows:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError("nonfinite cashflow")
        values.append(float(v))
    if values[0] >= 0 or values[-1] <= 0 or any(v > 0 for v in values[1:-1]):
        return None
    if (parsed[-1] - parsed[0]).days / day_count > 100:
        raise ValueError("horizon exceeds 100 years")
    remaining = [(parsed[-1] - d).days / day_count for d in parsed]
    scale = max(abs(v) for v in values)
    normalized = [v / scale for v in values]
    def terminal_value(rate):
        growth = math.log1p(rate)
        total = normalized[-1]
        for v, t in zip(normalized[:-1], remaining[:-1]):
            if v == 0:
                continue
            exponent = t * growth
            if exponent > 700:
                return -math.inf
            total += v * math.exp(exponent)
        return total
    lo, hi = -0.999999, 1.0
    if terminal_value(lo) < 0:
        return None
    while terminal_value(hi) > 0 and hi < 1e6:
        hi = 2 * hi + 1
    if terminal_value(hi) > 0:
        return None
    for _ in range(180):
        mid = (lo + hi) / 2
        if terminal_value(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

if __name__ == "__main__":
    print(f"Synthetic dated XIRR: {xirr(['2024-01-01','2024-07-01','2025-01-01'],[-100,-50,170]):.6%}")
