"""Section 5.5: fixed points and equilibria of affine balance recurrences."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float, excluding bool")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds finite float range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number

def periods_value(value):
    if type(value) is not int:
        raise TypeError("periods must be an integer")
    if value < 0:
        raise ValueError("periods must be nonnegative")
    return value

def equilibrium(rate, cash_flow, timing="end"):
    i = finite(rate, "rate")
    c = finite(cash_flow, "cash_flow")
    if i <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be 'end' or 'begin'")
    if i == 0:
        if c == 0:
            return {"kind": "all_balances", "balance": None,
                    "stability": "neutral"}
        return {"kind": "none", "balance": None, "stability": "not_applicable"}
    q = 1 + i
    value = -c / i if timing == "end" else -(q * c) / i
    if not math.isfinite(value):
        raise OverflowError("equilibrium outside finite float range")
    return {"kind": "unique", "balance": value,
            "stability": "attracting" if 0 < q < 1 else "repelling"}

def deviation_balance(initial, rate, cash_flow, periods, timing="end"):
    b0 = finite(initial, "initial")
    i = finite(rate, "rate")
    c = finite(cash_flow, "cash_flow")
    n = periods_value(periods)
    state = equilibrium(i, c, timing)
    if state["kind"] == "none":
        return b0 + n*c
    if state["kind"] == "all_balances":
        return b0
    star = state["balance"]
    value = star + math.exp(n*math.log1p(i))*(b0-star)
    if not math.isfinite(value):
        raise OverflowError("balance outside finite float range")
    return value

def iterative_balance(initial, rate, cash_flow, periods, timing="end"):
    b = finite(initial, "initial")
    i = finite(rate, "rate")
    c = finite(cash_flow, "cash_flow")
    n = periods_value(periods)
    if i <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be 'end' or 'begin'")
    for _ in range(n):
        b = (1+i)*b+c if timing == "end" else (b+c)*(1+i)
        if not math.isfinite(b):
            raise OverflowError("balance outside finite float range")
    return b

if __name__ == "__main__":
    for rate, flow in ((0.02, -100), (-0.1, 50), (0, 0), (0, 50)):
        print("rate=", rate, "flow=", flow, equilibrium(rate, flow))
    print("Below unstable equilibrium:",
          deviation_balance(4000, 0.02, -100, 4))
