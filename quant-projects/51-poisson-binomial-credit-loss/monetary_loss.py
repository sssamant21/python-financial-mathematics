"""Exact independent-default monetary loss distribution on an integer-cent grid.

Educational small-portfolio reference, not a calibrated credit-risk engine.
"""
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from math import isfinite
import argparse


def loss_distribution(probabilities, exposures_cents, lgds):
    """Return sorted {loss_in_cents: probability} with exact integer-cent losses.

    LGD must produce an integral cent loss for each exposure; reject rather than
    silently discretize. Independence is assumed. Limited to 16 borrowers.
    """
    n = len(probabilities)
    if not (1 <= n <= 16 and len(exposures_cents) == n and len(lgds) == n):
        raise ValueError("require 1..16 aligned borrowers")
    losses = []
    for p, exposure, lgd in zip(probabilities, exposures_cents, lgds):
        if isinstance(p, bool) or not isinstance(p, (float, int)) or not isfinite(p) or not 0 <= p <= 1:
            raise ValueError("invalid probability")
        if isinstance(exposure, bool) or not isinstance(exposure, int) or not 0 <= exposure <= 10**12:
            raise ValueError("exposure must be nonnegative integer cents <= 1e12")
        try:
            if isinstance(lgd, bool):
                raise ValueError("invalid LGD")
            d = Decimal(str(lgd))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError("invalid LGD") from exc
        if not d.is_finite() or not 0 <= d <= 1:
            raise ValueError("LGD outside [0,1]")
        amount = Decimal(exposure) * d
        if amount != amount.to_integral_value():
            raise ValueError("non-integral cent loss; specify finer units")
        losses.append(int(amount))
    pmf = {0: 1.0}
    for p, loss in zip(probabilities, losses):
        updated = defaultdict(float)
        for total, mass in pmf.items():
            updated[total] += mass * (1 - p)
            updated[total + loss] += mass * p
        pmf = dict(updated)
    return dict(sorted(pmf.items()))


def expected_loss(pmf):
    return sum(loss * probability for loss, probability in pmf.items())


def tail_probability(pmf, threshold_cents):
    if isinstance(threshold_cents, bool) or not isinstance(threshold_cents, int) or threshold_cents < 0:
        raise ValueError("threshold must be nonnegative integer cents")
    return sum(prob for loss, prob in pmf.items() if loss >= threshold_cents)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probabilities", nargs="+", type=float, default=[0.01, 0.05])
    parser.add_argument("--exposures-cents", nargs="+", type=int, default=[10000, 20000])
    parser.add_argument("--lgds", nargs="+", default=["0.4", "0.5"])
    parser.add_argument("--threshold-cents", type=int, default=10000)
    args = parser.parse_args()
    result = loss_distribution(args.probabilities, args.exposures_cents, args.lgds)
    print("loss_distribution_cents:", result)
    print("expected_loss_cents:", expected_loss(result))
    print("tail_probability:", tail_probability(result, args.threshold_cents))


if __name__ == "__main__":
    main()
