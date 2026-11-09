"""Descriptive block-bootstrap uncertainty for predeclared hedge sensitivity rows."""
import argparse
import numpy as np

def block_intervals(rows, window=52, shrinkage=0.0, draws=1000, seed=14, confidence=0.95, min_blocks=3):
    """Resample complete non-overlapping held-out blocks, separately by regime.

    These intervals are descriptive and do not guarantee future coverage.
    """
    if type(draws) is not int or not 100 <= draws <= 100000:
        raise ValueError("draws must be integer in [100,100000]")
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be nonnegative integer")
    if not np.isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence must be in (0,1)")
    if type(min_blocks) is not int or min_blocks < 2:
        raise ValueError("min_blocks must be integer >=2")
    if type(window) is not int or window < 8 or not np.isfinite(shrinkage) or not 0 <= shrinkage <= 1:
        raise ValueError("invalid predeclared estimator")
    selected = [r for r in rows if r["window"] == window and r["shrinkage"] == shrinkage]
    if not selected:
        raise ValueError("no matching estimator rows")
    origins = [r["origin"] for r in selected]
    if len(origins) != len(set(origins)) or origins != sorted(origins):
        raise ValueError("duplicate or unordered origins")
    rng = np.random.default_rng(seed)
    result = {}
    for regime in ("early", "late"):
        group = [r for r in selected if r["regime"] == regime]
        if len(group) < min_blocks:
            result[regime] = dict(n_blocks=len(group), status="insufficient_blocks", mean=None, lower=None, upper=None)
            continue
        values = np.array([r["variance_reduction"] for r in group], dtype=float)
        if not np.isfinite(values).all():
            result[regime] = dict(n_blocks=len(group), status="nonfinite_reduction", mean=None, lower=None, upper=None)
            continue
        sampled = rng.choice(values, size=(draws, len(values)), replace=True).mean(axis=1)
        alpha = (1-confidence)/2
        result[regime] = dict(n_blocks=len(group), status="descriptive_only", mean=float(values.mean()),
                              lower=float(np.quantile(sampled, alpha)), upper=float(np.quantile(sampled, 1-alpha)))
    return result

def demo(seed=14):
    from hedge_lab import synthetic
    from sensitivity import sensitivity
    rows = sensitivity(*synthetic(seed=seed))
    for regime, stats in block_intervals(rows, seed=seed).items():
        print(f"{regime}: {stats}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=14)
    demo(parser.parse_args().seed)
