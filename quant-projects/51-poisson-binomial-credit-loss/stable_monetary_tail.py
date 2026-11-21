"""High-precision independent-default monetary tail for <=16 borrowers.

Educational reference: enumerates default masks; not scalable or calibrated.
"""
from decimal import Decimal, localcontext
from itertools import product
from monetary_loss import loss_distribution


def stable_tail(probabilities, exposures_cents, lgds, threshold_cents, precision=100):
    """Return Decimal P(loss >= threshold), preserving sub-binary64 tails.

    Reuse monetary_loss input/cent validation, but compute event probabilities
    independently with Decimal and enumerate all binary default patterns.
    """
    if isinstance(precision, bool) or not isinstance(precision, int) or not 32 <= precision <= 1000:
        raise ValueError("precision must be an integer in [32,1000]")
    if isinstance(threshold_cents, bool) or not isinstance(threshold_cents, int) or threshold_cents < 0:
        raise ValueError("threshold must be nonnegative integer cents")
    # Validation only: do not use the float PMF for the tail calculation.
    loss_distribution(probabilities, exposures_cents, lgds)
    losses = [int(Decimal(e) * Decimal(str(g))) for e, g in zip(exposures_cents, lgds)]
    with localcontext() as ctx:
        ctx.prec = precision
        ps = [Decimal(str(p)) for p in probabilities]
        total = Decimal(0)
        for defaults in product((0, 1), repeat=len(ps)):
            loss = sum(amount for amount, default in zip(losses, defaults) if default)
            if loss < threshold_cents:
                continue
            mass = Decimal(1)
            for p, default in zip(ps, defaults):
                mass *= p if default else (Decimal(1) - p)
            total += mass
        return +total


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probabilities", type=float, nargs="+", required=True)
    parser.add_argument("--exposures-cents", type=int, nargs="+", required=True)
    parser.add_argument("--lgds", nargs="+", required=True)
    parser.add_argument("--threshold-cents", type=int, required=True)
    args = parser.parse_args()
    print(stable_tail(args.probabilities, args.exposures_cents, args.lgds, args.threshold_cents))
