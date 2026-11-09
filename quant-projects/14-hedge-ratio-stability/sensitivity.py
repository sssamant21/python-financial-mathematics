"""Historical-only hedge window and covariance-shrinkage sensitivity (synthetic)."""
import argparse
import numpy as np
from hedge_lab import synthetic


def sensitivity(asset, hedge, windows=(26, 52, 78), shrinkages=(0.0, 0.5, 1.0),
                horizon=13, max_abs=2.0):
    """Compare predeclared estimators on identical non-overlapping held-out blocks.

    Shrink sample covariance toward zero, leaving hedge variance unchanged.
    All models share origins beginning after the longest lookback.
    """
    a, b = np.asarray(asset, dtype=float), np.asarray(hedge, dtype=float)
    if a.ndim != 1 or b.shape != a.shape or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("matching finite one-dimensional returns required")
    if np.any(a <= -1) or np.any(b <= -1):
        raise ValueError("simple returns must exceed -100%")
    if not windows or any(type(w) is not int or w < 8 for w in windows):
        raise ValueError("windows must be integers >= 8")
    if not shrinkages or any(not np.isfinite(s) or s < 0 or s > 1 for s in shrinkages):
        raise ValueError("shrinkages must be within [0,1]")
    if type(horizon) is not int or horizon < 2 or not np.isfinite(max_abs) or not 0 < max_abs <= 10:
        raise ValueError("invalid horizon or hedge limit")
    start = max(windows)
    if len(a) < start + horizon:
        raise ValueError("insufficient held-out observations")
    rows = []
    for origin in range(start, len(a) - horizon + 1, horizon):
        future_a, future_b = a[origin:origin+horizon], b[origin:origin+horizon]
        baseline = float(np.var(future_a, ddof=1))
        for window in windows:
            x, y = a[origin-window:origin], b[origin-window:origin]
            var_h = float(np.var(y, ddof=1))
            if var_h <= 1e-14:
                raise ValueError("near-zero training hedge variance")
            raw = float(np.cov(x, y, ddof=1)[0, 1] / var_h)
            for shrinkage in shrinkages:
                ratio = float(np.clip((1-shrinkage)*raw, -max_abs, max_abs))
                realized = float(np.var(future_a-ratio*future_b, ddof=1))
                rows.append(dict(origin=origin, window=window, shrinkage=float(shrinkage),
                                 ratio=ratio, baseline_variance=baseline,
                                 hedged_variance=realized,
                                 variance_reduction=(baseline-realized)/baseline if baseline > 1e-14 else float("nan"),
                                 regime="early" if origin < len(a)//2 else "late"))
    return rows


def demo(seed=14):
    rows = sensitivity(*synthetic(seed=seed))
    for w in (26, 52, 78):
        for s in (0.0, 0.5, 1.0):
            selected = [r["variance_reduction"] for r in rows if r["window"] == w and r["shrinkage"] == s]
            print(f"window={w} shrinkage={s:.1f} mean_variance_reduction={np.nanmean(selected):.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=14)
    demo(parser.parse_args().seed)
