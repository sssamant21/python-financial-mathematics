"""Educational deterministic valuation and pending dossier template."""
import math
from numbers import Real

def finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be real, excluding bool")
    try:
        x = float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def value(flows, rate):
    r = finite(rate, "rate")
    terms = []
    for amount, years in flows:
        c, t = finite(amount, "amount"), finite(years, "time")
        if t < 0: raise ValueError("time must be nonnegative")
        try:
            term = c * math.exp(-r * t)
        except OverflowError as exc:
            raise OverflowError("discount factor exceeds numerical range") from exc
        if not math.isfinite(term):
            raise OverflowError("discounted cash flow exceeds numerical range")
        terms.append(term)
    try:
        result = math.fsum(terms)
    except OverflowError as exc:
        raise OverflowError("portfolio exceeds numerical range") from exc
    if not math.isfinite(result): raise OverflowError("portfolio exceeds numerical range")
    return result

def pending_dossier():
    return {"model": "constant-rate continuous discounting",
            "source_commit": None, "environment": None, "execution": "not run",
            "findings": [], "independent_review": "pending", "approval": "pending"}

if __name__ == "__main__":
    print("Synthetic example:", value([(100, 1), (200, 2)], 0))
    print("Template:", pending_dossier())
    print("Record execution and review separately.")
