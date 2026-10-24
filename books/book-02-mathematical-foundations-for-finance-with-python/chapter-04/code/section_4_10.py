"""Section 4.10: Chapter 04 integrated numerical assessment."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def positive(value, name):
    result = finite(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result

def periodic_future_value(principal, nominal_rate, frequency, periods):
    p = finite(principal, "principal")
    j = finite(nominal_rate, "nominal_rate")
    if p < 0:
        raise ValueError("principal must be nonnegative")
    if type(frequency) is not int or frequency < 1:
        raise ValueError("frequency must be a positive integer")
    if type(periods) is not int or periods < 0:
        raise ValueError("periods must be a nonnegative integer")
    i = j / frequency
    if i <= -1:
        raise ValueError("periodic factor must be positive")
    return p * math.exp(periods * math.log1p(i))

def effective_annual_rate(nominal_rate, frequency):
    j = finite(nominal_rate, "nominal_rate")
    if type(frequency) is not int or frequency < 1:
        raise ValueError("frequency must be a positive integer")
    i = j / frequency
    if i <= -1:
        raise ValueError("periodic factor must be positive")
    return math.expm1(frequency * math.log1p(i))

def continuous_from_effective(ear):
    ear = finite(ear, "ear")
    if ear <= -1:
        raise ValueError("EAR must exceed -1")
    return math.log1p(ear)

def continuous_future_value(principal, rate, years):
    p = finite(principal, "principal")
    r = finite(rate, "rate")
    t = finite(years, "years")
    if p < 0 or t < 0:
        raise ValueError("principal and years must be nonnegative")
    return p * math.exp(r * t)

def doubling_periods(periodic_rate):
    r = finite(periodic_rate, "periodic_rate")
    if r <= 0:
        raise ValueError("doubling requires positive periodic growth")
    return math.log(2) / math.log1p(r)

def cumulative_log_return(returns):
    values = tuple(returns)
    checked = [finite(r, "return") for r in values]
    if any(r <= -1 for r in checked):
        raise ValueError("all return factors must be positive")
    return math.fsum(math.log1p(r) for r in checked)

def cumulative_simple_return(returns):
    return math.expm1(cumulative_log_return(returns))

def implied_continuous_rate(initial, final, years):
    p = positive(initial, "initial")
    f = positive(final, "final")
    t = positive(years, "years")
    return (math.log(f) - math.log(p)) / t

def relative_fv_change(rate_delta, years):
    delta = finite(rate_delta, "rate_delta")
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    return math.expm1(delta * t)

def answers():
    return {
        "quarterly_future_value": periodic_future_value(5000, 0.08, 4, 12),
        "quarterly_ear": effective_annual_rate(0.08, 4),
        "present_value_at_10pct_ear": 1210 / (1.1 ** 2),
        "continuous_rate_from_7pct_ear": continuous_from_effective(0.07),
        "doubling_periods_at_6pct": doubling_periods(0.06),
        "implied_continuous_rate": implied_continuous_rate(1000, 1250, 4),
        "three_period_simple_return": cumulative_simple_return((0.15, -0.1, 0.05)),
        "loss_recovery_return": 1 / 0.7 - 1,
        "sensitivity_exact_20yr_15bp": relative_fv_change(0.0015, 20),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(answers(), indent=2))
