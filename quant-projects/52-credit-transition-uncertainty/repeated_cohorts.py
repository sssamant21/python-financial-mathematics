"""Predeclared repeated synthetic cohort diagnostics; educational, not market calibration."""
import argparse
import json
import math
import statistics

from cohort_calibration import cohort_diagnostics


def repeated_diagnostics(true_pd=0.04, train_size=500, heldout_size=200,
                         prior=(1.0, 1.0), first_seed=42, repetitions=20):
    """Report every independent seeded split and aggregate held-out scores.

    All settings are fixed before simulation; no best-seed selection.
    """
    if type(repetitions) is not int or not 2 <= repetitions <= 200:
        raise ValueError("repetitions must be an integer in [2, 200]")
    if type(first_seed) is not int or not 0 <= first_seed <= 2**32 - repetitions:
        raise ValueError("seed range exceeds 32-bit unsigned limit")
    rows = [
        cohort_diagnostics(true_pd, train_size, heldout_size, prior, first_seed + i)
        for i in range(repetitions)
    ]
    metrics = ("posterior_mean_default", "heldout_default_rate",
               "heldout_calibration_gap", "heldout_log_loss", "heldout_brier_score")
    aggregate = {
        key: {
            "mean": statistics.fmean(row[key] for row in rows),
            "min": min(row[key] for row in rows),
            "max": max(row[key] for row in rows),
        }
        for key in metrics
    }
    aggregate["mean_absolute_calibration_gap"] = statistics.fmean(
        abs(row["heldout_calibration_gap"]) for row in rows
    )
    aggregate["root_mean_squared_calibration_gap"] = math.sqrt(
        statistics.fmean(row["heldout_calibration_gap"] ** 2 for row in rows)
    )
    return {
        "synthetic": True, "repetitions": repetitions,
        "first_seed": first_seed, "prior": list(prior),
        "aggregate": aggregate, "runs": rows,
        "warning": "Synthetic repeated splits, not frequentist coverage, real-world calibration, or production validation",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--true-pd", type=float, default=0.04)
    parser.add_argument("--train-size", type=int, default=500)
    parser.add_argument("--heldout-size", type=int, default=200)
    parser.add_argument("--first-seed", type=int, default=42)
    parser.add_argument("--repetitions", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(repeated_diagnostics(
        args.true_pd, args.train_size, args.heldout_size,
        first_seed=args.first_seed, repetitions=args.repetitions
    ), indent=2))


if __name__ == "__main__":
    main()
