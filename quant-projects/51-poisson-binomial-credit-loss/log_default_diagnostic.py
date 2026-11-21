"""Log-domain probability of simultaneous independent defaults.

This diagnostic is *not* a general monetary-loss tail estimator.
"""
import argparse
import math


def log_all_default_probability(probabilities):
    """Return log P(all borrowers default); -inf represents a true zero event.

    The log remains finite when the probability underflows in binary64.
    """
    values = list(probabilities)
    if not 1 <= len(values) <= 500:
        raise ValueError("require 1..500 probabilities")
    total = 0.0
    for p in values:
        if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 <= p <= 1:
            raise ValueError("probabilities must be finite numbers in [0,1]")
        if p == 0:
            return float("-inf") if all(
                not isinstance(q, bool) and isinstance(q, (int, float))
                and math.isfinite(q) and 0 <= q <= 1 for q in values
            ) else _invalid()
        total += math.log(p)
    return total


def _invalid():
    raise ValueError("probabilities must be finite numbers in [0,1]")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probabilities", nargs="+", type=float, required=True)
    args = parser.parse_args()
    logp = log_all_default_probability(args.probabilities)
    print("log_all_default_probability:", logp)
    print("binary64_probability:", math.exp(logp))


if __name__ == "__main__":
    main()
