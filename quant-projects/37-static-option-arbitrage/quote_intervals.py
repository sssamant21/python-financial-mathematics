"""Conservative necessary-condition screens for European call bid/ask intervals."""
import math

def _finite(values):
    return all(not isinstance(x, bool) and isinstance(x, (int, float)) and math.isfinite(x) for x in values)

def screen(strikes, bids, asks, *, discount=1.0, tolerance=1e-10):
    """Flag inequalities impossible for any choice of prices inside quote intervals."""
    if len(strikes) < 3 or len(strikes) != len(bids) or len(bids) != len(asks):
        raise ValueError("at least three aligned quotes required")
    if not _finite([*strikes, *bids, *asks, discount, tolerance]):
        raise ValueError("finite numeric inputs required")
    if not 0 < discount <= 2 or not 0 <= tolerance <= 1e-4:
        raise ValueError("invalid discount or tolerance")
    if any(k <= 0 for k in strikes) or any(y <= x for x, y in zip(strikes, strikes[1:])):
        raise ValueError("strictly increasing positive strikes required")
    if any(b < 0 or a < b for b, a in zip(bids, asks)):
        raise ValueError("negative or crossed quote")
    issues = []
    for i in range(len(strikes)-1):
        if bids[i+1] > asks[i] + tolerance:
            issues.append(f"monotonicity:{i}")
        if bids[i] - asks[i+1] > discount * (strikes[i+1]-strikes[i]) + tolerance:
            issues.append(f"vertical_spread_bound:{i}")
    for i in range(1, len(strikes)-1):
        w = (strikes[i+1]-strikes[i]) / (strikes[i+1]-strikes[i-1])
        if bids[i] > w*asks[i-1] + (1-w)*asks[i+1] + tolerance:
            issues.append(f"convexity:{i}")
    return {"valid_necessary_conditions": not issues, "issues": issues}

def calendar_screen(earlier_bids, later_asks, *, earlier_discount, later_discount, tolerance=1e-10):
    """Common-forward, same-strike European call normalized calendar screen.

    Requires a shared forward level across expiries, deterministic discounting,
    and a martingale forward; NOT valid for arbitrary dividend/forward curves.
    """
    if not earlier_bids or len(earlier_bids) != len(later_asks):
        raise ValueError("aligned nonempty expiry grids required")
    if not _finite([*earlier_bids, *later_asks, earlier_discount, later_discount, tolerance]):
        raise ValueError("finite numeric inputs required")
    if min(*earlier_bids, *later_asks) < 0 or not 0 < earlier_discount <= 2 or not 0 < later_discount <= 2 or not 0 <= tolerance <= 1e-4:
        raise ValueError("invalid quote, discount or tolerance")
    issues = [f"calendar:{i}" for i, (b,a) in enumerate(zip(earlier_bids,later_asks))
              if b/earlier_discount > a/later_discount + tolerance]
    return {"valid_necessary_conditions": not issues, "issues": issues}

if __name__ == "__main__":
    import json
    print(json.dumps({"strike": screen([90,100,110],[14,9,5],[15,10,6]),
                      "calendar": calendar_screen([10,6,3],[12,8,4],earlier_discount=1,later_discount=1)}, indent=2))
