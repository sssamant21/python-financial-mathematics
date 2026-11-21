"""Bounded, deterministic synthetic benchmark for sparse independent-default tails."""
import argparse
import json
import time
from decimal import Decimal, localcontext
from math import comb
from sparse_monetary_tail import sparse_tail
from stable_monetary_tail import stable_tail


def binomial_reference(n, p, cutoff, precision=100):
    """Independent equal-loss analytical reference."""
    with localcontext() as ctx:
        ctx.prec = precision
        p = Decimal(str(p))
        return +sum((Decimal(comb(n, k)) * p**k * (1-p)**(n-k)
                     for k in range(cutoff, n+1)), Decimal(0))


def benchmark_case(n, kind, precision=100, max_states=10000):
    """Return observed tail, independent reference and descriptive elapsed time."""
    if (isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 40
            or kind not in ("equal", "distinct")):
        raise ValueError("require 1..40 borrowers and equal/distinct pattern")
    if kind == "distinct" and n > 12:
        raise ValueError("distinct benchmark capped at 12 borrowers")
    exposures = [100] * n if kind == "equal" else [2**i for i in range(n)]
    threshold = 100 * ((n+1)//2) if kind == "equal" else sum(exposures)//2 + 1
    expected_states = n+1 if kind == "equal" else 2**n
    start = time.perf_counter()
    actual = sparse_tail(["0.25"]*n, exposures, [1]*n, threshold,
                         precision=precision, max_states=max_states)
    elapsed = time.perf_counter() - start
    if kind == "equal":
        reference = binomial_reference(n, "0.25", (n+1)//2, precision)
        method = "independent combinatorial binomial formula"
    else:
        # Existing exhaustive reference validates binary64 input, not strings.
        reference = stable_tail([0.25]*n, exposures, [1]*n, threshold,
                                precision=precision)
        method = "independent exhaustive Decimal default-mask enumeration"
    return {"borrowers": n, "pattern": kind, "expected_states": expected_states,
            "state_limit": max_states, "precision_digits": precision,
            "threshold_cents": threshold, "tail_probability": str(actual),
            "reference_probability": str(reference),
            "absolute_error": str(abs(actual-reference)),
            "reference_method": method, "elapsed_seconds": round(elapsed, 6)}


def run_suite(precision=100, max_states=10000):
    cases = [(n, "equal") for n in (4, 8, 12, 20, 40)]
    cases += [(n, "distinct") for n in (4, 8, 12)]
    return [benchmark_case(n, kind, precision, max_states) for n, kind in cases]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=100)
    parser.add_argument("--max-states", type=int, default=10000)
    args = parser.parse_args()
    print(json.dumps({"synthetic_only": True, "timings_not_portable": True,
                      "results": run_suite(args.precision, args.max_states)}, indent=2))
