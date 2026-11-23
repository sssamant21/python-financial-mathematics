"""Predeclared prior-strength stability on identical synthetic cohorts (research only)."""
import argparse
import json
import math
import statistics

from cohort_calibration import cohort_diagnostics


def prior_stability(true_pd=0.04, train_size=500, heldout_size=200,
                    first_seed=42, repetitions=10, strengths=(0.5, 1.0, 5.0)):
    """Evaluate every fixed prior on the SAME train/held-out draws per seed.

    The two-state prior is (strength, strength). Held-out outcomes are
    used only for scoring; no strength is selected or optimized.
    """
    if type(repetitions) is not int or not 2 <= repetitions <= 100:
        raise ValueError("repetitions must be in [2, 100]")
    if type(first_seed) is not int or not 0 <= first_seed <= 2**32 - repetitions:
        raise ValueError("invalid 32-bit seed range")
    if not isinstance(strengths, (tuple, list)) or not 1 <= len(strengths) <= 8:
        raise ValueError("provide 1 to 8 prior strengths")
    if any(isinstance(k, bool) or not isinstance(k, (float, int))
           or not math.isfinite(k) or not 0.01 <= k <= 1000 for k in strengths):
        raise ValueError("strengths must be finite in [0.01, 1000]")
    if len(set(strengths)) != len(strengths):
        raise ValueError("duplicate strengths are not permitted")
    # Limit the total work and output before generating any data.
    if type(train_size) is not int or type(heldout_size) is not int or (
        train_size + heldout_size) * repetitions * len(strengths) > 2_000_000:
        raise ValueError("simulation budget exceeded")
    rows = []
    for seed in range(first_seed, first_seed + repetitions):
        for strength in strengths:
            row = cohort_diagnostics(true_pd, train_size, heldout_size,
                                     (float(strength), float(strength)), seed)
            rows.append({"strength": float(strength), **row})
    summary = []
    for strength in strengths:
        group = [row for row in rows if row["strength"] == float(strength)]
        summary.append({
            "strength": float(strength),
            "mean_log_loss": statistics.fmean(r["heldout_log_loss"] for r in group),
            "mean_brier": statistics.fmean(r["heldout_brier_score"] for r in group),
            "mean_absolute_gap": statistics.fmean(
                abs(r["heldout_calibration_gap"]) for r in group),
        })
    return {"synthetic": True, "first_seed": first_seed,
            "repetitions": repetitions, "strengths": list(strengths),
            "runs": rows, "summary": summary,
            "warning": "No test-set prior selection; synthetic only; no empirical calibration claim"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--true-pd", type=float, default=0.04)
    parser.add_argument("--train-size", type=int, default=500)
    parser.add_argument("--heldout-size", type=int, default=200)
    parser.add_argument("--first-seed", type=int, default=42)
    parser.add_argument("--repetitions", type=int, default=10)
    parser.add_argument("--strengths", type=float, nargs="+", default=[0.5, 1.0, 5.0])
    args = parser.parse_args()
    print(json.dumps(prior_stability(args.true_pd, args.train_size,
          args.heldout_size, args.first_seed, args.repetitions,
          args.strengths), indent=2))


if __name__ == "__main__":
    main()
