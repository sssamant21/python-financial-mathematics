"""Seeded asset-correlation and Monte Carlo sensitivity, synthetic only."""
import math
import statistics
from credit_risk import Exposure, summarize
from correlated_defaults import simulate

def sensitivity(exposures, *, correlations=(0.0, 0.2, 0.5), seeds=(11, 23, 37, 51, 71), scenarios=2000, quantile=0.99):
    """Across-seed dispersion is descriptive, not a confidence interval."""
    exposures = tuple(exposures)
    expected = summarize(exposures)['expected_loss']
    correlations, seeds = tuple(correlations), tuple(seeds)
    if not correlations or len(correlations) > 20 or not seeds or len(seeds) > 30:
        raise ValueError('require 1..20 correlations and 1..30 seeds')
    if len(set(seeds)) != len(seeds) or any(isinstance(s, bool) or not isinstance(s, int) for s in seeds):
        raise ValueError('seeds must be distinct integers')
    if any(isinstance(r, bool) or not isinstance(r, (int, float)) or not math.isfinite(r) or not 0 <= r < 1 for r in correlations):
        raise ValueError('correlations must be finite in [0,1)')
    if len(set(correlations)) != len(correlations):
        raise ValueError('correlations must be distinct')
    if isinstance(scenarios, bool) or not isinstance(scenarios, int) or not 100 <= scenarios <= 1000000:
        raise ValueError('scenarios outside [100, 1000000]')
    if isinstance(quantile, bool) or not isinstance(quantile, (int, float)) or not math.isfinite(quantile) or not 0 < quantile < 1:
        raise ValueError('quantile outside (0,1)')
    if scenarios * len(seeds) * len(correlations) > 2_000_000:
        raise ValueError('simulation budget exceeds 2 million scenarios')
    rows = []
    for rho in correlations:
        runs = [simulate(exposures, asset_correlation=rho, scenarios=scenarios, seed=s, quantile=quantile) for s in seeds]
        means = [x['simulated_mean_loss'] for x in runs]
        vars_ = [x['loss_var'] for x in runs]
        tails = [x['loss_expected_shortfall'] for x in runs]
        rows.append({'asset_correlation': rho, 'runs': len(seeds), 'scenarios_per_run': scenarios,
                     'analytical_expected_loss': expected,
                     'mean_loss_across_seeds': statistics.fmean(means),
                     'mean_loss_seed_sd': statistics.stdev(means) if len(means) > 1 else None,
                     'var_across_seeds': statistics.fmean(vars_),
                     'var_seed_sd': statistics.stdev(vars_) if len(vars_) > 1 else None,
                     'tail_average_across_seeds': statistics.fmean(tails),
                     'tail_average_seed_sd': statistics.stdev(tails) if len(tails) > 1 else None})
    return rows

def demo():
    book = (Exposure('A', 1_000_000, .01, .45), Exposure('B', 500_000, .03, .60), Exposure('C', 250_000, .06, .50))
    for row in sensitivity(book):
        print(f"rho={row['asset_correlation']:.2f} EL={row['analytical_expected_loss']:.0f} "
              f"sim_mean={row['mean_loss_across_seeds']:.0f} "
              f"VaR={row['var_across_seeds']:.0f} VaR_seed_SD={row['var_seed_sd']:.0f} "
              f"tail_mean={row['tail_average_across_seeds']:.0f}")

if __name__ == '__main__':
    demo()
