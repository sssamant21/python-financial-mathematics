"""Exact integer powers, approximate real roots, and equivalent period rates."""
from fractions import Fraction
import math


def integer_power(base, exponent):
    if type(base) not in (int, str, Fraction):
        raise TypeError("exact base requires int, rational string, or Fraction")
    if type(exponent) is not int:
        raise TypeError("exponent must be an integer, excluding bool")
    value = Fraction(base)
    if value == 0 and exponent <= 0:
        raise ValueError("zero base requires a positive exponent in this interface")
    return value ** exponent


def finite_float(value):
    if type(value) not in (int, float):
        raise TypeError("use a built-in int or float, excluding bool")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError("input exceeds the float interface") from exc
    if not math.isfinite(number):
        raise ValueError("input must be finite")
    return number


def root_index(index):
    if type(index) is not int or not 1 <= index <= 120:
        raise ValueError("root index must be an integer from 1 to 120")
    return index


def real_root(value, index):
    x, n = finite_float(value), root_index(index)
    if x < 0 and n % 2 == 0:
        raise ValueError("even root of a negative value is outside the real domain")
    magnitude = abs(x) ** (1.0 / n)
    return -magnitude if x < 0 else magnitude


def infer_period_rate(*, initial_value, final_value, periods):
    initial, final = finite_float(initial_value), finite_float(final_value)
    n = root_index(periods)
    if initial <= 0 or final <= 0:
        raise ValueError("rate inference requires positive endpoint values")
    ratio = final / initial
    if not math.isfinite(ratio) or ratio <= 0:
        raise ValueError("endpoint ratio is outside the supported float range")
    factor = real_root(ratio, n)
    rate = factor - 1.0
    if rate <= -1:
        raise ValueError("period rate cannot be represented inside the declared domain")
    return {"growth_factor": factor, "period_rate": rate, "target_ratio": ratio}


def main():
    print("Exact discount factor:", integer_power("1.05", -2))
    print(f"Principal square root of 9: {real_root(9, 2):.6f}")
    print(f"Real cube root of -8: {real_root(-8, 3):.6f}")
    print(f"16 to the power 3/4: {real_root(16, 4) ** 3:.6f}")
    for ending, periods in [(1210, 2), (810, 2), (1331, 3)]:
        result = infer_period_rate(initial_value=1000, final_value=ending, periods=periods)
        print(f"Ending {ending} over {periods} periods: "
              f"rate={result['period_rate']:.6f}, factor={result['growth_factor']:.6f}")


if __name__ == "__main__":
    main()
