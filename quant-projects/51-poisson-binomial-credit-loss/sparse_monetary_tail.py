"""Sparse Decimal DP for independent-default loss tails (educational, synthetic).

Cent-exact loss amounts; no discretization, external data, or trading.
"""
import argparse
from decimal import Decimal, InvalidOperation, localcontext


def sparse_tail(probabilities, exposures_cents, lgds, threshold_cents,
                precision=100, max_states=10000):
    """Return Decimal P(total loss >= threshold) using bounded sparse states.

    Each state is an exact integer-cent loss.  Computation stops with ValueError
    rather than approximating or silently dropping states when the cap is hit.
    """
    if (isinstance(precision, bool) or not isinstance(precision, int)
            or not 32 <= precision <= 1000):
        raise ValueError("precision must be an integer in [32,1000]")
    if (isinstance(max_states, bool) or not isinstance(max_states, int)
            or not 2 <= max_states <= 100000):
        raise ValueError("max_states must be an integer in [2,100000]")
    if (isinstance(threshold_cents, bool) or not isinstance(threshold_cents, int)
            or threshold_cents < 0):
        raise ValueError("threshold must be nonnegative integer cents")
    n = len(probabilities)
    if not 1 <= n <= 128 or len(exposures_cents) != n or len(lgds) != n:
        raise ValueError("require 1..128 aligned borrowers")
    ps, losses = [], []
    for p, exposure, lgd in zip(probabilities, exposures_cents, lgds):
        if isinstance(p, bool) or not isinstance(p, (int, float, str, Decimal)):
            raise ValueError("invalid probability")
        if isinstance(exposure, bool) or not isinstance(exposure, int) or not 0 <= exposure <= 10**12:
            raise ValueError("invalid exposure cents")
        try:
            probability, severity = Decimal(str(p)), Decimal(str(lgd))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("invalid probability or LGD") from exc
        if (not probability.is_finite() or not 0 <= probability <= 1
                or not severity.is_finite() or not 0 <= severity <= 1
                or isinstance(lgd, bool)):
            raise ValueError("probability and LGD must be finite in [0,1]")
        amount = Decimal(exposure) * severity
        if amount != amount.to_integral_value():
            raise ValueError("non-integral cent loss; use finer units")
        ps.append(probability)
        losses.append(int(amount))
    if threshold_cents == 0:
        return Decimal(1)
    if threshold_cents > sum(losses):
        return Decimal(0)
    with localcontext() as ctx:
        ctx.prec = precision
        states = {0: Decimal(1)}
        for p, amount in zip(ps, losses):
            if p == 0 or amount == 0:
                continue
            if p == 1:
                states = {loss + amount: mass for loss, mass in states.items()}
                continue
            updated = {}
            for loss, mass in states.items():
                for key, contribution in ((loss, mass * (1-p)), (loss + amount, mass * p)):
                    updated[key] = updated.get(key, Decimal(0)) + contribution
            if len(updated) > max_states:
                raise ValueError("state limit exceeded; no approximate result returned")
            states = updated
        return +sum((mass for loss, mass in states.items() if loss >= threshold_cents), Decimal(0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probabilities", nargs="+", required=True)
    parser.add_argument("--exposures-cents", nargs="+", type=int, required=True)
    parser.add_argument("--lgds", nargs="+", required=True)
    parser.add_argument("--threshold-cents", type=int, required=True)
    parser.add_argument("--precision", type=int, default=100)
    parser.add_argument("--max-states", type=int, default=10000)
    a = parser.parse_args()
    print(sparse_tail(a.probabilities, a.exposures_cents, a.lgds,
                      a.threshold_cents, a.precision, a.max_states))
