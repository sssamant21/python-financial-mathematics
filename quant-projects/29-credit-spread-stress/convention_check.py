"""Synthetic bond repricing across explicitly matched yield conventions; not external model validation."""
from math import exp, isfinite, log1p
from repricing_check import price

def nominal_to_continuous(nominal_rate: float, frequency: int = 2) -> float:
    if isinstance(frequency, bool) or not isinstance(frequency, int) or not 1 <= frequency <= 365:
        raise ValueError("frequency must be integer 1..365")
    if isinstance(nominal_rate, bool) or not isinstance(nominal_rate, (int, float)) or not isfinite(nominal_rate):
        raise ValueError("nominal rate must be finite")
    if nominal_rate / frequency <= -1:
        raise ValueError("periodic compounding base must be positive")
    return frequency * log1p(nominal_rate / frequency)

def periodic_price(cashflows: list[tuple[float, float]], nominal_rate: float, frequency: int = 2) -> float:
    continuous = nominal_to_continuous(nominal_rate, frequency)
    if not isinstance(cashflows, (list, tuple)) or not cashflows:
        raise ValueError("nonempty cash flows required")
    total, last = 0.0, 0.0
    for item in cashflows:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError("cash flow must be (time, amount)")
        t, amount = item
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v) for v in (t, amount)) or t <= last or amount <= 0:
            raise ValueError("increasing positive times and amounts required")
        if abs(continuous * t) > 700:
            raise ValueError("discount exponent outside safe range")
        total += amount * exp(-continuous * t)
        last = t
    if not isfinite(total) or total <= 0:
        raise ValueError("invalid discounted value")
    return total

def compare_conventions(cashflows: list[tuple[float, float]], nominal_rate: float, frequency: int = 2) -> dict:
    cc_rate = nominal_to_continuous(nominal_rate, frequency)
    periodic = periodic_price(cashflows, nominal_rate, frequency)
    continuous = price(cashflows, cc_rate, 0.0)
    return {"frequency": frequency, "nominal_rate": nominal_rate, "continuous_equivalent": cc_rate,
            "periodic_price": periodic, "continuous_price": continuous, "difference": periodic - continuous}

if __name__ == "__main__":
    flows = [(0.5 * i, 2.5 if i < 10 else 102.5) for i in range(1, 11)]
    for m in (1, 2, 4):
        result = compare_conventions(flows, 0.05, m)
        print(f'm={m} | continuous equivalent={result["continuous_equivalent"]:.8f} | price={result["periodic_price"]:.8f} | difference={result["difference"]:.3g}')
