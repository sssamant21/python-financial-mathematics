"""Section 5.6: convergence, stability, and disturbance propagation."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds finite float range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number

def nonnegative_int(value, name):
    if type(value) is not int:
        raise TypeError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value

def classify(q, cash_flow=0):
    factor = finite(q, "q")
    flow = finite(cash_flow, "cash_flow")
    if abs(factor) < 1:
        return "attracting"
    if abs(factor) > 1:
        return "repelling"
    if factor == 1:
        return "neutral" if flow == 0 else "no_fixed_point"
    return "oscillatory_neutral"

def equilibrium(q, cash_flow):
    factor = finite(q, "q")
    flow = finite(cash_flow, "cash_flow")
    if factor == 1:
        return None
    value = flow / (1 - factor)
    if not math.isfinite(value):
        raise OverflowError("equilibrium outside finite float range")
    return value

def deviation(q, initial_deviation, periods):
    factor = finite(q, "q")
    initial = finite(initial_deviation, "initial_deviation")
    n = nonnegative_int(periods, "periods")
    result = (factor ** n) * initial
    if not math.isfinite(result):
        raise OverflowError("deviation outside finite float range")
    return result

def periods_to_tolerance(q, initial_deviation, tolerance):
    factor = abs(finite(q, "q"))
    initial = abs(finite(initial_deviation, "initial_deviation"))
    eps = finite(tolerance, "tolerance")
    if eps <= 0:
        raise ValueError("tolerance must be positive")
    if factor >= 1:
        raise ValueError("tolerance convergence requires |q| < 1")
    if initial <= eps:
        return 0
    if factor == 0:
        return 1
    estimate = math.ceil(math.log(eps / initial) / math.log(factor))
    n = max(0, estimate)
    while initial * factor ** n > eps:
        n += 1
    while n > 0 and initial * factor ** (n-1) <= eps:
        n -= 1
    return n

def half_life(q):
    factor = abs(finite(q, "q"))
    if not 0 < factor < 1:
        raise ValueError("half-life requires 0 < |q| < 1")
    return math.log(0.5) / math.log(factor)

def shock_effect(q, shock, shock_period, observed_period):
    factor = finite(q, "q")
    amount = finite(shock, "shock")
    k = nonnegative_int(shock_period, "shock_period")
    n = nonnegative_int(observed_period, "observed_period")
    if k < 1:
        raise ValueError("shock_period must be at least one")
    if n < k:
        return 0.0
    return amount * factor ** (n-k)

if __name__ == "__main__":
    print("Classification:", classify(0.9, 50))
    print("Equilibrium:", equilibrium(0.9, 50))
    print("Periods to tolerance:",
          periods_to_tolerance(0.9, -400, 10))
    print("Deviation half-life:", half_life(0.9))
