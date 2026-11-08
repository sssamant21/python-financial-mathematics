"""Rolling one-week historical/normal VaR and bootstrap estimation uncertainty."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm, binomtest

ALPHA = 0.05

def rolling_risk(returns: pd.DataFrame, lookback: int = 52, alpha: float = ALPHA,
                 bootstrap: int = 500, seed: int = 42) -> pd.DataFrame:
    """Score week t using training returns [t-lookback,t), never week t."""
    if not isinstance(lookback, int) or lookback < 20:
        raise ValueError('lookback must be an integer >= 20')
    if not 0 < alpha < 0.5 or not isinstance(bootstrap, int) or bootstrap < 100:
        raise ValueError('alpha must be in (0,0.5); bootstrap >= 100')
    if not {'Date', 'Return'}.issubset(returns):
        raise ValueError('Require Date and Return columns')
    df = returns[['Date', 'Return']].copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='raise')
    df['Return'] = pd.to_numeric(df['Return'], errors='raise')
    if df.Date.isna().any() or df.Date.duplicated().any() or not df.Date.is_monotonic_increasing:
        raise ValueError('Dates must be nonmissing, unique and strictly increasing')
    x = df.Return.to_numpy(dtype=float)
    if not np.isfinite(x).all() or np.any(x <= -1):
        raise ValueError('Returns must be finite and > -100%')
    if len(x) <= lookback:
        raise ValueError('Need at least one out-of-sample return')
    rng = np.random.default_rng(seed)
    rows = []
    for t in range(lookback, len(x)):
        train = x[t-lookback:t]
        hist_loss = -float(np.quantile(train, alpha))
        normal_loss = -float(np.mean(train) + np.std(train, ddof=1) * norm.ppf(alpha))
        draws = rng.choice(train, size=(bootstrap, lookback), replace=True)
        boot_losses = -np.quantile(draws, alpha, axis=1)
        lo, hi = np.quantile(boot_losses, [0.025, 0.975])
        cutoff = np.quantile(train, alpha)
        empirical_cvar = -float(np.mean(train[train <= cutoff]))
        realized_loss = -float(x[t])
        rows.append({
            'Date': df.Date.iloc[t].date().isoformat(), 'RealizedReturn': float(x[t]),
            'RealizedLoss': realized_loss, 'HistoricalVaR95': max(0., hist_loss),
            'NormalVaR95': max(0., normal_loss), 'HistoricalCVaR95': max(0., empirical_cvar),
            'BootstrapVaRLower95': max(0., float(lo)),
            'BootstrapVaRUpper95': max(0., float(hi)),
            'HistoricalBreach': int(realized_loss > max(0., hist_loss)),
            'NormalBreach': int(realized_loss > max(0., normal_loss)),
            'TrainingEndDate': df.Date.iloc[t-1].date().isoformat(),
        })
    return pd.DataFrame(rows)

def breach_summary(scored: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame:
    """Binomial diagnostic assumes independent breaches; do not treat as certification."""
    rows = []
    for label, col in [('Historical', 'HistoricalBreach'), ('Normal', 'NormalBreach')]:
        n = len(scored)
        k = int(scored[col].sum())
        rows.append({'Method': label, 'Weeks': n, 'Breaches': k,
                     'BreachRate': k/n, 'ExpectedRate': alpha,
                     'BinomialPValue': float(binomtest(k, n, alpha).pvalue)})
    return pd.DataFrame(rows)

def synthetic_returns(n: int = 260, seed: int = 2026) -> pd.DataFrame:
    """Fictional weekly volatility regimes; date labels are not market evidence."""
    if n < 60:
        raise ValueError('n >= 60')
    rng = np.random.default_rng(seed)
    sigma = np.full(n, 0.014)
    sigma[n//3:n//3+25] = 0.045
    sigma[2*n//3:2*n//3+30] = 0.030
    x = rng.normal(0.001, sigma)
    x = np.maximum(x, -0.99)
    return pd.DataFrame({'Date': pd.date_range('2019-01-04', periods=n, freq='W-FRI'), 'Return': x})

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--returns', type=Path, help='Licensed CSV with Date,Return weekly decimal simple returns')
    parser.add_argument('--output', type=Path, default=Path(__file__).parent/'reports')
    parser.add_argument('--lookback', type=int, default=52)
    parser.add_argument('--bootstrap', type=int, default=500)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    df = pd.read_csv(args.returns) if args.returns else synthetic_returns()
    scored = rolling_risk(df, lookback=args.lookback, bootstrap=args.bootstrap, seed=args.seed)
    summary = breach_summary(scored)
    args.output.mkdir(parents=True, exist_ok=True)
    scored.to_csv(args.output/'weekly_tail_risk.csv', index=False)
    summary.to_csv(args.output/'breach_summary.csv', index=False)
    (args.output/'metadata.json').write_text(json.dumps({
        'data_source': str(args.returns) if args.returns else 'synthetic_seed_2026',
        'input_start': str(pd.to_datetime(df.Date.iloc[0]).date()),
        'input_end': str(pd.to_datetime(df.Date.iloc[-1]).date()),
        'lookback_weeks': args.lookback, 'bootstrap_resamples': args.bootstrap,
        'bootstrap_seed': args.seed, 'alpha': ALPHA, 'scored_weeks': len(scored),
        'note': 'Bootstrap interval is uncertainty in estimated historical VaR, not a coverage guarantee.'
    }, indent=2)+'\n', encoding='utf-8')
    print(summary.to_string(index=False))
    print('Synthetic scenario unless --returns was supplied; no live trading.')

if __name__ == '__main__':
    main()
