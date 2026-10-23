"""Exact affine-fee comparisons and finite counterexample searches."""
from fractions import Fraction
from itertools import combinations


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError("use an integer, rational string, or Fraction")
    return Fraction(value)


def fee_metrics(*, amount, fixed_fee, fee_rate):
    x, fixed, rate = map(rational, (amount, fixed_fee, fee_rate))
    if x <= 0 or fixed < 0 or rate < 0:
        raise ValueError("require amount > 0 and nonnegative fee parameters")
    total = fixed + rate * x
    return {"total": total, "effective": total / x}


def search_pairs(*, amounts, fixed_fee, fee_rate, claim):
    claims = ("effective_nonincreasing", "effective_strictly_decreasing")
    if claim not in claims:
        raise ValueError("unknown claim")
    xs = tuple(rational(x) for x in amounts)
    if len(xs) < 2 or any(x <= 0 for x in xs):
        raise ValueError("provide at least two positive amounts")
    if any(a >= b for a, b in zip(xs, xs[1:])):
        raise ValueError("amounts must be strictly increasing")
    metrics = [fee_metrics(amount=x, fixed_fee=fixed_fee, fee_rate=fee_rate)
               for x in xs]
    checked = 0
    witness = None
    for i, j in combinations(range(len(xs)), 2):
        left, right = metrics[i]["effective"], metrics[j]["effective"]
        holds = right <= left if claim == claims[0] else right < left
        checked += 1
        if not holds and witness is None:
            witness = {"a": xs[i], "b": xs[j],
                       "effective_a": left, "effective_b": right}
    return {"claim": claim, "pairs_checked": checked,
            "counterexample": witness,
            "scope": "supplied finite candidate pairs only"}


def main():
    for x in (100, 200):
        m = fee_metrics(amount=x, fixed_fee=5, fee_rate="0.01")
        print(f"Amount {x}: total={m['total']}, effective={m['effective']}")
    strict = search_pairs(amounts=(100, 200, 400), fixed_fee=0,
                          fee_rate="0.01", claim="effective_strictly_decreasing")
    weak = search_pairs(amounts=(100, 200, 400), fixed_fee=0,
                        fee_rate="0.01", claim="effective_nonincreasing")
    print(f"Strict claim witness: {strict['counterexample']}")
    print(f"Non-strict claim witness: {weak['counterexample']}")
    print(f"Pairs checked per search: {weak['pairs_checked']}")
    print(f"Scope: {weak['scope']}")


if __name__ == "__main__":
    main()
