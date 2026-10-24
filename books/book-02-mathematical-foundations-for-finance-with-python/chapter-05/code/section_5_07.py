"""Variable-rate, signed cash-flow recurrence: Section 5.7."""
import math

def number(value, name):
    if type(value) not in (int, float):
        raise TypeError(name + " must be numeric (not bool)")
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(name + " must be finite")
    return x

def schedule(initial, rates, cash_flows, timing="end", allow_negative=True):
    b = number(initial, "initial")
    if timing not in ("end", "begin"):
        raise ValueError("invalid timing")
    if type(allow_negative) is not bool:
        raise TypeError("allow_negative must be bool")
    if not allow_negative and b < 0:
        raise ValueError("negative opening balance")
    rates = tuple(number(x, "rate") for x in rates)
    flows = tuple(number(x, "cash_flow") for x in cash_flows)
    if len(rates) != len(flows):
        raise ValueError("schedule lengths differ")
    if any(x <= -1 for x in rates):
        raise ValueError("growth factors must be positive")
    balances, ledger = [b], []
    for n, (rate, cash) in enumerate(zip(rates, flows), 1):
        opening = b
        interest = rate * (opening if timing == "end" else opening + cash)
        b = opening + cash + interest
        if not math.isfinite(b) or not math.isfinite(interest):
            raise OverflowError("nonfinite balance")
        if not allow_negative and b < 0:
            raise ValueError("negative balance at period " + str(n))
        ledger.append({"period": n, "opening": opening, "rate": rate,
                       "interest": interest, "cash_flow": cash, "closing": b})
        balances.append(b)
    return balances, ledger

def closed_end_balance(initial, rates, cash_flows):
    b = number(initial, "initial")
    rates = tuple(number(x, "rate") for x in rates)
    flows = tuple(number(x, "cash_flow") for x in cash_flows)
    if len(rates) != len(flows):
        raise ValueError("schedule lengths differ")
    if any(x <= -1 for x in rates):
        raise ValueError("growth factors must be positive")
    factors = tuple(1 + x for x in rates)
    result = b * math.prod(factors)
    for k, cash in enumerate(flows):
        result += cash * math.prod(factors[k + 1:])
    if not math.isfinite(result):
        raise OverflowError("nonfinite balance")
    return result

def reconcile(initial, balances, ledger):
    if len(balances) != len(ledger) + 1:
        raise ValueError("schedule lengths differ")
    return (balances[-1] - number(initial, "initial"),
            math.fsum(row["interest"] for row in ledger) +
            math.fsum(row["cash_flow"] for row in ledger))

if __name__ == "__main__":
    r, c = (0.02, -0.01, 0.03), (100, -50, 0)
    balances, ledger = schedule(1000, r, c)
    print(balances, reconcile(1000, balances, ledger))
