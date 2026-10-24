"""Restricted exact rational equations and positive-principal fee targets."""
from fractions import Fraction


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def solve_ratio(*, a, b, c, d, target):
    a, b, c, d, t = map(rational, (a, b, c, d, target))
    result = {"candidate": None, "solution": None, "residual": None,
              "excluded": () if c == 0 else (-d / c,),
              "domain_empty": c == 0 and d == 0}
    if result["domain_empty"]:
        return {**result, "kind": "none", "reason": "undefined_for_all_inputs"}
    coefficient, rhs = a - t * c, t * d - b
    if coefficient == 0:
        kind = "all" if rhs == 0 else "none"
        return {**result, "kind": kind, "reason": "cleared_" + kind}
    x = rhs / coefficient
    result["candidate"] = x
    denominator = c * x + d
    if denominator == 0:
        return {**result, "kind": "none", "reason": "candidate_at_excluded_pole"}
    residual = (a * x + b) / denominator - t
    return {**result, "kind": "unique", "solution": x,
            "residual": residual, "reason": "checked_original_equation"}


def principal_for_fee_target(*, fixed_fee, fee_rate, target_fraction):
    fixed, k, q = map(rational, (fixed_fee, fee_rate, target_fraction))
    if fixed < 0 or k < 0 or q < 0:
        raise ValueError("fee parameters and target fraction must be nonnegative")
    result = solve_ratio(a=k, b=fixed, c=1, d=0, target=q)
    p = result["solution"]
    admissible = result["kind"] == "all" or (p is not None and p > 0)
    return {**result, "admissible": admissible,
            "financial_domain": "positive real principal"}


def main():
    valid = solve_ratio(a=2, b=3, c=1, d=-1, target=5)
    hole = solve_ratio(a=1, b=-1, c=1, d=-1, target=0)
    print(f"Valid ratio root: {valid['solution']}, residual={valid['residual']}")
    print(f"Excluded candidate: {hole['candidate']}, kind={hole['kind']}")
    fee = principal_for_fee_target(fixed_fee=5, fee_rate="0.01", target_fraction="0.02")
    same = principal_for_fee_target(fixed_fee=0, fee_rate="0.01", target_fraction="0.01")
    zero = principal_for_fee_target(fixed_fee=0, fee_rate="0.01", target_fraction="0.02")
    negative = principal_for_fee_target(fixed_fee=5, fee_rate="0.01", target_fraction="0.005")
    print(f"Fee target principal: {fee['solution']}, admissible={fee['admissible']}")
    print(f"Zero fixed fee, matching target: {same['kind']}")
    print(f"Zero fixed fee, other target: {zero['kind']}, candidate={zero['candidate']}")
    print(f"Negative ratio root: {negative['solution']}, admissible={negative['admissible']}")


if __name__ == "__main__":
    main()
