"""Section 5.3: first-order balance recurrences and reconciliation."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def balance_ledger(initial, rates, cash_flows, timing="end",
                   allow_negative=True):
    """Return (balances, ledger) for one rate and cash flow per period."""
    opening = finite(initial, "initial")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be 'end' or 'begin'")
    if type(allow_negative) is not bool:
        raise TypeError("allow_negative must be bool")
    if not allow_negative and opening < 0:
        raise ValueError("initial balance cannot be negative")
    rate_values = tuple(finite(x, "rate") for x in rates)
    flows = tuple(finite(x, "cash_flow") for x in cash_flows)
    if len(rate_values) != len(flows):
        raise ValueError("rates and cash_flows must have equal length")
    if any(rate <= -1 for rate in rate_values):
        raise ValueError("each period growth factor must be positive")
    balances = [opening]
    ledger = []
    for period, (rate, cash_flow) in enumerate(zip(rate_values, flows), 1):
        previous = balances[-1]
        interest_base = previous if timing == "end" else previous + cash_flow
        interest = interest_base * rate
        closing = previous + interest + cash_flow
        if not math.isfinite(closing) or not math.isfinite(interest):
            raise OverflowError("nonfinite balance or interest")
        if not allow_negative and closing < 0:
            raise ValueError(f"period {period} would produce negative balance")
        ledger.append({
            "period": period,
            "opening_balance": previous,
            "periodic_rate": rate,
            "cash_flow": cash_flow,
            "interest": interest,
            "closing_balance": closing,
        })
        balances.append(closing)
    return balances, ledger

def constant_rate_path(initial, periodic_rate, cash_flows,
                       timing="end", allow_negative=True):
    flows = tuple(cash_flows)
    rate = finite(periodic_rate, "periodic_rate")
    return balance_ledger(initial, [rate] * len(flows), flows,
                          timing=timing, allow_negative=allow_negative)

def reconcile(initial, balances, ledger):
    start = finite(initial, "initial")
    if not balances or not ledger and len(balances) != 1:
        raise ValueError("inconsistent balance path")
    if len(balances) != len(ledger) + 1:
        raise ValueError("ledger length does not match balances")
    interest = math.fsum(row["interest"] for row in ledger)
    cash_flows = math.fsum(row["cash_flow"] for row in ledger)
    return (balances[-1] - start, interest + cash_flows)

if __name__ == "__main__":
    path, rows = constant_rate_path(1000, 0.02, (100, 100, 100))
    print("Balances:", path)
    print("Reconciliation:", reconcile(1000, path, rows))
