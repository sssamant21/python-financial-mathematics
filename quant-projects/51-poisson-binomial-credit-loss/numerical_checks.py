"""Independent small-portfolio enumeration and log-domain extreme-tail checks.

Synthetic educational diagnostics, not a replacement for calibrated credit models.
"""
import argparse
import itertools
import math
from decimal import Decimal, localcontext

from poisson_binomial import distribution


def enumerate_decimal(probabilities, precision=80):
    ps = list(probabilities)
    if not 1 <= len(ps) <= 16:
        raise ValueError("enumeration supports 1..16 obligors")
    if isinstance(precision, bool) or not isinstance(precision, int) or not 30 <= precision <= 200:
        raise ValueError("precision must be an integer in [30,200]")
    # Delegate input validation to the published baseline implementation.
    distribution(ps)
    with localcontext() as ctx:
        ctx.prec = precision
        ds = [Decimal(str(p)) for p in ps]
        out = [Decimal(0)] * (len(ps) + 1)
        for outcome in itertools.product((0, 1), repeat=len(ps)):
            mass = Decimal(1)
            for p, defaulted in zip(ds, outcome):
                mass *= p if defaulted else 1 - p
            out[sum(outcome)] += mass
        return out


def all_default_log_probability(probabilities):
    ps = list(probabilities)
    distribution(ps)  # same finite, bounded input validation
    if any(p == 0 for p in ps):
        return -math.inf
    return math.fsum(math.log(p) for p in ps)


def diagnostics(probabilities):
    ps = list(probabilities)
    pmf = distribution(ps)
    exact = enumerate_decimal(ps)
    return {
        "max_absolute_pmf_error": max(abs(Decimal(str(x)) - y) for x, y in zip(pmf, exact)),
        "log_all_default_probability": all_default_log_probability(ps),
        "float_all_default_probability": pmf[-1],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probabilities", nargs="+", type=float, default=[0.01, 0.02, 0.05, 0.1])
    args = parser.parse_args()
    try:
        result = diagnostics(args.probabilities)
    except ValueError as exc:
        parser.error(str(exc))
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
