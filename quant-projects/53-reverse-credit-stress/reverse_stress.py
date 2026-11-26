"""Synthetic reverse credit stress: minimum common PD multiplier breaching a loss budget.

Educational expected-loss arithmetic, not a default simulation or regulatory capital model.
"""
import argparse
import json
import math


def _number(value, name, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value) or (value <= 0 if positive else value < 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}")
    return value


def expected_loss(exposures, pds, lgds, multiplier=1.0):
    """Sum EAD * min(1, PD * multiplier) * LGD for a fixed borrower set."""
    multiplier = _number(multiplier, "multiplier", positive=True)
    if not (len(exposures) == len(pds) == len(lgds)) or not 1 <= len(exposures) <= 10000:
        raise ValueError("require 1..10000 aligned borrowers")
    total = 0.0
    for e, p, l in zip(exposures, pds, lgds):
        e, p, l = _number(e, "EAD"), _number(p, "PD"), _number(l, "LGD")
        if p > 1 or l > 1:
            raise ValueError("PD and LGD must be <= 1")
        total += e * min(1.0, p * multiplier) * l
    if not math.isfinite(total):
        raise ValueError("loss overflow")
    return total



def borrower_stress(exposures, pds, lgds, multipliers):
    """Forward stress with one predeclared PD multiplier >= 1 per borrower."""
    baseline = expected_loss(exposures, pds, lgds)
    if len(multipliers) != len(exposures):
        raise ValueError("require one multiplier per borrower")
    rows = []
    for e, p, l, m in zip(exposures, pds, lgds, multipliers):
        m = _number(m, "borrower multiplier", positive=True)
        if m < 1:
            raise ValueError("borrower multiplier must be >= 1")
        p = float(p)
        stressed_pd = min(1.0, p * m)
        before = float(e) * p * float(l)
        after = float(e) * stressed_pd * float(l)
        rows.append({"baseline_pd": p, "stressed_pd": stressed_pd,
                     "baseline_loss": before, "stressed_loss": after,
                     "incremental_loss": after - before})
    try:
        stressed = math.fsum(row["stressed_loss"] for row in rows)
        increment = math.fsum(row["incremental_loss"] for row in rows)
    except OverflowError as exc:
        raise ValueError("loss overflow") from exc
    if not math.isfinite(stressed) or not math.isfinite(increment):
        raise ValueError("loss overflow")
    return {"baseline_loss": baseline, "stressed_loss": stressed,
            "incremental_loss": increment, "borrowers": rows}


def reverse_stress(exposures, pds, lgds, budget, *, maximum_multiplier=1000.0, iterations=80):
    """Find first multiplier in [1, max] with EL >= budget, or report unreachable.

    Equality at baseline returns 1.0. A budget above saturation is unreachable.
    """
    budget = _number(budget, "budget", positive=True)
    maximum_multiplier = _number(maximum_multiplier, "maximum_multiplier", positive=True)
    if maximum_multiplier < 1 or isinstance(iterations, bool) or not isinstance(iterations, int) or not 1 <= iterations <= 200:
        raise ValueError("invalid search bounds")
    baseline = expected_loss(exposures, pds, lgds)
    upper_loss = expected_loss(exposures, pds, lgds, maximum_multiplier)
    result = {"baseline_loss": baseline, "max_loss": upper_loss, "budget": budget,
              "max_multiplier": maximum_multiplier, "breach_multiplier": None}
    if baseline >= budget:
        result["breach_multiplier"] = 1.0
    elif upper_loss >= budget:
        lo, hi = 1.0, maximum_multiplier
        for _ in range(iterations):
            mid = lo + (hi - lo) / 2
            if expected_loss(exposures, pds, lgds, mid) >= budget:
                hi = mid
            else:
                lo = mid
        result["breach_multiplier"] = hi
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--budget", type=float, default=25.0)
    parser.add_argument("--max-multiplier", type=float, default=20.0)
    args = parser.parse_args()
    # Hypothetical exposures, probabilities and recoveries; no market data.
    result = reverse_stress([1000, 500, 750], [0.01, 0.02, 0.03],
                            [0.4, 0.5, 0.6], args.budget,
                            maximum_multiplier=args.max_multiplier)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
