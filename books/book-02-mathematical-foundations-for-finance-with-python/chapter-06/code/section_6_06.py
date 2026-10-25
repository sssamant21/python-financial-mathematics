"""Section 6.6: perpetuities, deferral, and exact tails."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def periods(value):
    if type(value) is not int:
        raise TypeError("period count must be an integer")
    if value < 0:
        raise ValueError("period count must be nonnegative")
    return value

def level_perpetuity(payment, rate, timing="end"):
    c, r = finite(payment, "payment"), finite(rate, "rate")
    if r <= 0:
        raise ValueError("level perpetuity requires rate > 0")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be end or begin")
    value = c / r * (1 + r if timing == "begin" else 1)
    if not math.isfinite(value):
        raise OverflowError("nonfinite value")
    return value

def growing_perpetuity(first_payment, growth, rate):
    c = finite(first_payment, "first_payment")
    g, r = finite(growth, "growth"), finite(rate, "rate")
    if g <= -1 or r <= -1:
        raise ValueError("growth factors must be positive")
    if c == 0:
        return 0.0
    if r <= g:
        raise ValueError("nonzero growing perpetuity requires rate > growth")
    value = c / (r - g)
    if not math.isfinite(value):
        raise OverflowError("nonfinite value")
    return value

def deferred_level(payment, rate, deferred_periods):
    m = periods(deferred_periods)
    r = finite(rate, "rate")
    value = level_perpetuity(payment, r) * math.exp(-m * math.log1p(r))
    if not math.isfinite(value):
        raise OverflowError("nonfinite value")
    return value

def deferred_growing(first_payment_after_deferral, growth, rate, deferred_periods):
    m = periods(deferred_periods)
    r = finite(rate, "rate")
    value = growing_perpetuity(first_payment_after_deferral, growth, r)
    value *= math.exp(-m * math.log1p(r))
    if not math.isfinite(value):
        raise OverflowError("nonfinite value")
    return value

def level_tail(payment, rate, completed_periods):
    return deferred_level(payment, rate, completed_periods)

def growing_tail(first_payment, growth, rate, completed_periods):
    n = periods(completed_periods)
    g, r = finite(growth, "growth"), finite(rate, "rate")
    base = growing_perpetuity(first_payment, g, r)
    value = base * math.exp(n * (math.log1p(g) - math.log1p(r)))
    if not math.isfinite(value):
        raise OverflowError("nonfinite value")
    return value

def finite_level_pv(payment, rate, n):
    c, r = finite(payment, "payment"), finite(rate, "rate")
    n = periods(n)
    if r <= 0:
        raise ValueError("rate must be positive")
    return math.fsum(c * (1 + r)**(-k) for k in range(1, n + 1))

def finite_growing_pv(first_payment, growth, rate, n):
    c = finite(first_payment, "first_payment")
    g, r = finite(growth, "growth"), finite(rate, "rate")
    n = periods(n)
    if g <= -1 or r <= -1:
        raise ValueError("growth factors must be positive")
    return math.fsum(c * (1 + g)**(k - 1) / (1 + r)**k
                     for k in range(1, n + 1))

if __name__ == "__main__":
    print("Level perpetuity:", level_perpetuity(100, 0.05))
    print("Deferred by 3:", deferred_level(100, 0.05, 3))
    print("Level tail after 10:", level_tail(100, 0.05, 10))
    print("Growing perpetuity:", growing_perpetuity(100, 0.02, 0.05))
    print("Growing tail after 5:", growing_tail(100, 0.02, 0.05, 5))
