"""Seeded, synthetic train/held-out default-rate diagnostics (educational only).

Predeclare probability, cohort sizes, prior and seed before simulation.
The held-out sample never enters the posterior fit.
"""
import argparse
import json
import math
import random

from transition_uncertainty import posterior_alpha


def _size(value):
    if type(value) is not int or not 1 <= value <= 100000:
        raise ValueError("cohort size must be an integer in [1, 100000]")


def _probability(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 < value < 1:
        raise ValueError("true default probability must be strictly between 0 and 1")


def _seed(value):
    if type(value) is not int or not 0 <= value <= 2**32 - 1:
        raise ValueError("seed must be a 32-bit unsigned integer")


def cohort_diagnostics(true_pd=0.04, train_size=500, heldout_size=200,
                       prior=(1.0, 1.0), seed=42):
    """Fit a two-state transition row on training observations only.

    Scores use held-out defaults solely after freezing the posterior mean.
    """
    _probability(true_pd)
    _size(train_size)
    _size(heldout_size)
    _seed(seed)
    # Validate prior even if the generated training cohort has no defaults.
    posterior_alpha([0, 0], prior)
    if len(prior) != 2:
        raise ValueError("two-state prior required")
    rng = random.Random(seed)
    train_defaults = sum(rng.random() < true_pd for _ in range(train_size))
    heldout_defaults = sum(rng.random() < true_pd for _ in range(heldout_size))
    alpha = posterior_alpha([train_size - train_defaults, train_defaults], prior)
    predicted = alpha[1] / sum(alpha)
    observed = heldout_defaults / heldout_size
    log_loss = -(heldout_defaults * math.log(predicted) +
                 (heldout_size - heldout_defaults) * math.log1p(-predicted)) / heldout_size
    brier = (heldout_defaults * (1 - predicted)**2 +
             (heldout_size - heldout_defaults) * predicted**2) / heldout_size
    return {
        "synthetic": True, "seed": seed, "true_pd": true_pd,
        "train_size": train_size, "heldout_size": heldout_size,
        "train_defaults": train_defaults, "heldout_defaults": heldout_defaults,
        "posterior_mean_default": predicted, "heldout_default_rate": observed,
        "heldout_calibration_gap": predicted - observed,
        "heldout_log_loss": log_loss, "heldout_brier_score": brier,
        "warning": "Single synthetic split; no empirical coverage or real-market calibration claim",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--true-pd", type=float, default=0.04)
    parser.add_argument("--train-size", type=int, default=500)
    parser.add_argument("--heldout-size", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(cohort_diagnostics(args.true_pd, args.train_size,
                                        args.heldout_size, seed=args.seed), indent=2))


if __name__ == "__main__":
    main()
