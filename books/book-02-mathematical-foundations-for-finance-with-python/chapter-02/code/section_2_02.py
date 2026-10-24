"""Exact linear classification and one-period financial rearrangements."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def solve_linear(*, coefficient, constant, target):
    a, b, t = map(rational, (coefficient, constant, target))
    if a == 0:
        return {"kind": "all" if b == t else "none", "solution": None}
    return {"kind": "unique", "solution": (t - b) / a}


def principal_for_target(*, target_value, period_rate, fixed_fee, fee_rate):
    target, r, fixed, k = map(rational,
                             (target_value, period_rate, fixed_fee, fee_rate))
    if target < 0 or r <= -1 or fixed < 0 or k < 0:
        raise ValueError("require target >= 0, r > -1, F >= 0, k >= 0")
    result = solve_linear(coefficient=1 + r - k, constant=-fixed, target=target)
    p = result["solution"]
    admissible = result["kind"] == "all" or (p is not None and p > 0)
    residual = None if p is None else p * (1 + r) - fixed - k * p - target
    return {**result, "admissible": admissible, "residual": residual,
            "solution_domain": "positive real principal"}


def rate_for_target(*, principal, target_value, fixed_fee, fee_rate):
    p, target, fixed, k = map(rational,
                             (principal, target_value, fixed_fee, fee_rate))
    if p <= 0 or target < 0 or fixed < 0 or k < 0:
        raise ValueError("require P > 0 and target, F, k >= 0")
    rate = (target + fixed) / p - 1 + k
    residual = p * (1 + rate) - fixed - k * p - target
    return {"kind": "unique", "solution": rate,
            "admissible": rate > -1, "residual": residual,
            "solution_domain": "real period rate greater than -1"}


def main():
    principal = principal_for_target(target_value=1045, period_rate="0.06",
                                     fixed_fee=5, fee_rate="0.01")
    print(f"Principal: {principal['solution']}, "
          f"admissible={principal['admissible']}, residual={principal['residual']}")
    rate = rate_for_target(principal=1000, target_value=1045,
                           fixed_fee=5, fee_rate="0.01")
    print(f"Period rate: {rate['solution']}, "
          f"admissible={rate['admissible']}, residual={rate['residual']}")
    all_case = principal_for_target(target_value=0, period_rate=0,
                                    fixed_fee=0, fee_rate=1)
    none_case = principal_for_target(target_value=0, period_rate=0,
                                     fixed_fee=3, fee_rate=1)
    negative = principal_for_target(target_value=100, period_rate=0,
                                    fixed_fee=0, fee_rate=2)
    print(f"Zero coefficient, zero target: {all_case['kind']}")
    print(f"Zero coefficient, fixed fee 3: {none_case['kind']}")
    print(f"Negative real root: {negative['solution']}, "
          f"admissible={negative['admissible']}, residual={negative['residual']}")


if __name__ == "__main__":
    main()
