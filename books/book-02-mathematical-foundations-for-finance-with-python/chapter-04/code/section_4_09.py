"""Section 4.9 — Growth and Rate Conversion Explorer (standard library)."""
import argparse
import json
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be a number, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def nonnegative(value, name):
    result = finite(value, name)
    if result < 0:
        raise ValueError(f"{name} must be nonnegative")
    return result

def frequency_value(value):
    if type(value) is not int:
        raise TypeError("frequency must be an integer")
    if value < 1:
        raise ValueError("frequency must be positive")
    return value

def periods_value(value):
    if type(value) is not int:
        raise TypeError("periods must be an integer")
    if value < 0:
        raise ValueError("periods must be nonnegative")
    return value

def periodic_log_factor(nominal_rate, frequency, periods):
    j = finite(nominal_rate, "nominal_rate")
    m = frequency_value(frequency)
    n = periods_value(periods)
    i = j / m
    if i <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    result = n * math.log1p(i)
    if not math.isfinite(result):
        raise OverflowError("log factor exceeds finite float range")
    return result

def periodic_result(principal, nominal_rate, frequency, periods):
    p = nonnegative(principal, "principal")
    log_factor = periodic_log_factor(nominal_rate, frequency, periods)
    factor = math.exp(log_factor)
    future = p * factor
    if not math.isfinite(future):
        raise OverflowError("future value exceeds finite float range")
    m = frequency_value(frequency)
    return {
        "convention": "periodic",
        "principal": p,
        "nominal_annual_rate": float(nominal_rate),
        "periods_per_year": m,
        "completed_periods": periods,
        "years": periods / m,
        "future_value": future,
        "recovered_present_value": future / factor,
        "effective_annual_rate": math.expm1(periodic_log_factor(nominal_rate, m, m)),
        "equivalent_continuous_annual_rate": m * math.log1p(float(nominal_rate) / m),
    }

def continuous_result(principal, continuous_rate, years):
    p = nonnegative(principal, "principal")
    r = finite(continuous_rate, "continuous_rate")
    t = nonnegative(years, "years")
    factor = math.exp(r * t)
    future = p * factor
    if not math.isfinite(future):
        raise OverflowError("future value exceeds finite float range")
    return {
        "convention": "continuous",
        "principal": p,
        "continuous_annual_rate": r,
        "years": t,
        "future_value": future,
        "recovered_present_value": future / factor,
        "effective_annual_rate": math.expm1(r),
        "relative_fv_sensitivity_to_10bp": t * 0.001,
        "exact_relative_fv_change_for_10bp": math.expm1(t * 0.001),
    }

def convert_result(effective_annual_rate, frequency):
    ear = finite(effective_annual_rate, "effective_annual_rate")
    m = frequency_value(frequency)
    if ear <= -1:
        raise ValueError("effective annual rate must exceed -1")
    log_factor = math.log1p(ear)
    return {
        "effective_annual_rate": ear,
        "periods_per_year": m,
        "nominal_annual_rate": m * math.expm1(log_factor / m),
        "continuous_annual_rate": log_factor,
    }

def parser():
    p = argparse.ArgumentParser(description="Growth and Rate Conversion Explorer")
    sub = p.add_subparsers(dest="mode", required=True)
    periodic = sub.add_parser("periodic")
    periodic.add_argument("--principal", type=float, required=True)
    periodic.add_argument("--nominal-rate", type=float, required=True)
    periodic.add_argument("--frequency", type=int, required=True)
    periodic.add_argument("--periods", type=int, required=True)
    continuous = sub.add_parser("continuous")
    continuous.add_argument("--principal", type=float, required=True)
    continuous.add_argument("--continuous-rate", type=float, required=True)
    continuous.add_argument("--years", type=float, required=True)
    convert = sub.add_parser("convert")
    convert.add_argument("--ear", type=float, required=True)
    convert.add_argument("--frequency", type=int, required=True)
    return p

def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    try:
        if args.mode == "periodic":
            result = periodic_result(args.principal, args.nominal_rate,
                                     args.frequency, args.periods)
        elif args.mode == "continuous":
            result = continuous_result(args.principal, args.continuous_rate,
                                       args.years)
        else:
            result = convert_result(args.ear, args.frequency)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (ValueError, OverflowError, TypeError, ZeroDivisionError) as exc:
        p.error(str(exc))

if __name__ == "__main__":
    raise SystemExit(main())
