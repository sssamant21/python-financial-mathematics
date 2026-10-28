"""Section 5.9: contribution and withdrawal recurrence engine."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Period:
    rate: float
    cash_flow: float

@dataclass(frozen=True)
class EngineResult:
    initial: float
    closing: float
    ledger: tuple
    first_rejected: int | None

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def normalize(periods):
    result = []
    for p in periods:
        if not isinstance(p, Period):
            raise TypeError("each period must be a Period")
        rate = finite(p.rate, "rate")
        flow = finite(p.cash_flow, "cash_flow")
        if rate <= -1:
            raise ValueError("growth factor must be positive")
        result.append(Period(rate, flow))
    return tuple(result)

def run_engine(initial, periods, timing="end", allow_negative=True):
    opening = finite(initial, "initial")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    if type(allow_negative) is not bool:
        raise TypeError("allow_negative must be bool")
    if not allow_negative and opening < 0:
        raise ValueError("negative initial balance")
    periods = normalize(periods)
    balance, ledger, rejected = opening, [], None
    for index, period in enumerate(periods, 1):
        start = balance
        q = 1 + period.rate
        requested = period.cash_flow
        if timing == "end":
            interest = start * period.rate
            available = start * q
            if not math.isfinite(available):
                raise OverflowError("nonfinite available balance")
            feasible = allow_negative or requested >= 0 or available + requested >= 0
            applied = requested if feasible else 0.0
            balance = available + applied
        else:
            available = start
            feasible = allow_negative or requested >= 0 or available + requested >= 0
            applied = requested if feasible else 0.0
            # Reject immediately before growth; no interest is credited
            # for an unprocessed period.
            interest = (start + applied) * period.rate if feasible else 0.0
            balance = (start + applied) * q if feasible else start
        if not math.isfinite(balance) or not math.isfinite(interest):
            raise OverflowError("nonfinite period result")
        rounding_adjustment = math.fsum((balance,-start,-applied,-interest))
        ledger.append({
            "period": index, "opening": start, "rate": period.rate,
            "requested": requested, "applied": applied,
            "interest": interest, "closing": balance,
            "accepted": feasible,
            "rounding_adjustment": rounding_adjustment,
        })
        if not feasible:
            rejected = index
            break
    return EngineResult(opening, balance, tuple(ledger), rejected)

def reconcile(result):
    """Return balance change and rounded interest/flow/adjustment components."""
    change = result.closing - result.initial
    components = math.fsum(row["interest"] for row in result.ledger)
    components += math.fsum(row["applied"] for row in result.ledger)
    components = math.fsum((components,math.fsum(row.get("rounding_adjustment",0.0) for row in result.ledger)))
    return change, components

def closed_form_reference(initial, periods, timing="end"):
    """Independent product/sum reference for unrestricted schedules."""
    start = finite(initial, "initial")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    periods = normalize(periods)
    factors = tuple(1 + p.rate for p in periods)
    result = start * math.prod(factors)
    for k, period in enumerate(periods):
        result += period.cash_flow * math.prod(
            factors[k + 1:] if timing == "end" else factors[k:])
    if not math.isfinite(result):
        raise OverflowError("nonfinite reference balance")
    return result

if __name__ == "__main__":
    scenario = (Period(0.02, 100), Period(-0.01, -50), Period(0.03, 0))
    result = run_engine(1000, scenario, allow_negative=False)
    print("Closing:", result.closing)
    print("Reconciliation:", reconcile(result))
    print("Independent reference:", closed_form_reference(1000, scenario))
