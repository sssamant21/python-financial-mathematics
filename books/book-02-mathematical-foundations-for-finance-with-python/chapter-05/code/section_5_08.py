"""Section 5.8: withdrawal feasibility and depletion boundaries."""
import math

def number(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def simulate_withdrawals(initial, rates, withdrawals, timing="end",
                         policy="reject"):
    """Simulate nonnegative balances; stop at first infeasible withdrawal.

    policy='reject': record rejected request, leave account at the available
    balance, and stop. policy='partial': pay available amount, close at zero,
    and stop. Each record includes requested and paid amounts.
    """
    b = number(initial, "initial")
    if b < 0:
        raise ValueError("initial balance must be nonnegative")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be 'end' or 'begin'")
    if policy not in ("reject", "partial"):
        raise ValueError("policy must be 'reject' or 'partial'")
    rates = tuple(number(x, "rate") for x in rates)
    withdrawals = tuple(number(x, "withdrawal") for x in withdrawals)
    if len(rates) != len(withdrawals):
        raise ValueError("schedule lengths differ")
    if any(x <= -1 for x in rates):
        raise ValueError("growth factors must be positive")
    if any(x < 0 for x in withdrawals):
        raise ValueError("withdrawals must be nonnegative")
    rows = []
    first_infeasible = None
    for n, (rate, requested) in enumerate(zip(rates, withdrawals), 1):
        opening = b
        available = opening * (1 + rate) if timing == "end" else opening
        if not math.isfinite(available):
            raise OverflowError("nonfinite available balance")
        feasible = requested <= available
        paid = requested if feasible else (0.0 if policy == "reject" else available)
        if timing == "end":
            closing = available - paid
        else:
            closing = (available - paid) * (1 + rate)
        if not math.isfinite(closing):
            raise OverflowError("nonfinite closing balance")
        rows.append({"period": n, "opening": opening, "rate": rate,
                     "requested": requested, "available": available,
                     "paid": paid, "feasible": feasible, "closing": closing})
        b = closing
        if not feasible:
            first_infeasible = n
            break
    return {"closing_balance": b, "first_infeasible": first_infeasible,
            "ledger": rows}

def zero_rate_first_infeasible(initial, withdrawal):
    b = number(initial, "initial")
    w = number(withdrawal, "withdrawal")
    if b < 0 or w <= 0:
        raise ValueError("require nonnegative initial and positive withdrawal")
    return math.floor(b / w) + 1

if __name__ == "__main__":
    result = simulate_withdrawals(500, (0.01,)*3, (200,)*3)
    print("First infeasible period:", result["first_infeasible"])
    print("Ledger:", result["ledger"])
