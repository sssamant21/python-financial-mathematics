"""Constant-coefficient continuous-account model; educational draft."""
import math
from numbers import Real

def finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be real, excluding bool")
    try: x = float(x)
    except OverflowError as exc: raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x): raise ValueError(f"{name} must be finite")
    return x

def transition(initial, rate, flow, years):
    initial, rate, flow, years = (finite(v, n) for v, n in
        ((initial, "initial"), (rate, "rate"), (flow, "flow"), (years, "years")))
    if years < 0: raise ValueError("years must be nonnegative")
    if years == 0: return initial
    if rate == 0:
        result = initial + flow * years
    else:
        exponent = rate * years
        if not math.isfinite(exponent): raise OverflowError("exponent exceeds float range")
        try:
            growth = math.exp(exponent)
            contribution = flow * (math.expm1(exponent) / rate)
            result = initial * growth + contribution
        except OverflowError as exc:
            raise OverflowError("transition exceeds float range") from exc
    if not math.isfinite(result): raise OverflowError("transition exceeds float range")
    return result

def scenario_report(initial, rate, flow, years):
    result = transition(initial, rate, flow, years)
    return {"model": "constant-coefficient unconstrained account",
            "inputs": {"initial": initial, "rate": rate, "flow": flow, "years": years},
            "units": {"initial": "currency", "rate": "per year",
                      "flow": "currency per year", "years": "years"},
            "ending_balance": result, "boundary_policy": "unconstrained; negative balances allowed",
            "validation_execution": "not run", "independent_review": "pending",
            "approval": "pending"}

if __name__ == "__main__":
    print(scenario_report(1000, 0, 200, 3))
