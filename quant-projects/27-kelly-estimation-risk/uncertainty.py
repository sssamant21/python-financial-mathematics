"""Wilson-score probability uncertainty and conservative Kelly stress; synthetic education only."""
import argparse
import math
from kelly import optimal_fraction, expected_log_growth


def wilson_interval(wins: int, trials: int, z: float = 1.96):
    """Two-sided Wilson score interval; z=1.96 is an approximate 95% normal quantile."""
    if isinstance(wins, bool) or not isinstance(wins, int) or isinstance(trials, bool) or not isinstance(trials, int):
        raise ValueError("wins and trials must be integers")
    if trials < 1 or wins < 0 or wins > trials:
        raise ValueError("require 0 <= wins <= trials and trials >= 1")
    if isinstance(z, bool) or not isinstance(z, (int, float)) or not math.isfinite(z) or z <= 0:
        raise ValueError("z must be positive and finite")
    p = wins / trials
    denom = 1 + z*z/trials
    center = (p + z*z/(2*trials))/denom
    radius = z*math.sqrt(p*(1-p)/trials + z*z/(4*trials*trials))/denom
    return max(0., center-radius), min(1., center+radius)


def conservative_diagnostic(wins: int, trials: int, win_return=1., loss_fraction=1., cap=.5, z=1.96):
    """Choose from training-only lower bound; evaluate at fixed hypothetical probabilities."""
    low, high = wilson_interval(wins, trials, z)
    optimal_fraction(0.5, win_return, loss_fraction, cap)  # validate even at all-win/all-loss boundaries
    point = wins / trials
    point_fraction = optimal_fraction(point, win_return, loss_fraction, cap) if 0 < point < 1 else (cap if point == 1 else 0.)
    conservative_fraction = optimal_fraction(low, win_return, loss_fraction, cap) if low > 0 else 0.
    scenarios = []
    for p in (0.45, 0.50, 0.55):
        scenarios.append((p, expected_log_growth(point_fraction, p, win_return, loss_fraction), expected_log_growth(conservative_fraction, p, win_return, loss_fraction)))
    return low, high, point_fraction, conservative_fraction, scenarios


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synthetic Wilson uncertainty sensitivity; no trading recommendations')
    parser.add_argument('--wins', type=int, default=55)
    parser.add_argument('--trials', type=int, default=100)
    args = parser.parse_args()
    lo, hi, point, robust, scenarios = conservative_diagnostic(args.wins, args.trials)
    print(f'Wilson interval: [{lo:.6f}, {hi:.6f}]')
    print(f'Point-estimate fraction: {point:.6f}; lower-bound fraction: {robust:.6f}')
    for p, g1, g2 in scenarios:
        print(f'Hypothetical p={p:.2f}: point growth={g1:.6f}; lower-bound growth={g2:.6f}')
