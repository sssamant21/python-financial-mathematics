"""Training-only drawdown scenario forecasts and held-out realized outcomes."""
import argparse
import json
import numpy as np
from drawdown import analyze, bootstrap_risk


def walkforward(returns, *, train=104, horizon=26, step=None,
                blocks=(2, 4, 8), simulations=500, seed=2026):
    """Evaluate non-overlapping held-out paths, with each forecast trained strictly before origin."""
    r = np.asarray(returns, dtype=float)
    analyze(r)
    if step is None:
        step = horizon
    if not all(isinstance(v, int) and not isinstance(v, bool) for v in (train, horizon, step, simulations, seed)):
        raise ValueError('train, horizon, step, simulations and seed must be integers')
    if train < 20 or horizon < 2 or step < horizon or simulations < 10 or simulations > 100000:
        raise ValueError('invalid window, horizon, step or simulation count')
    if not isinstance(blocks, (tuple, list)) or not blocks or len(set(blocks)) != len(blocks):
        raise ValueError('blocks must be a nonempty sequence of distinct integers')
    if any(not isinstance(b, int) or isinstance(b, bool) or b < 1 or b > train for b in blocks):
        raise ValueError('each block must fit the training window')
    if r.size < train + horizon:
        raise ValueError('insufficient observations for one held-out horizon')
    results = []
    for origin in range(train, r.size - horizon + 1, step):
        training = r[origin - train:origin]
        realized = analyze(r[origin:origin + horizon])['max_drawdown']
        for block in blocks:
            # Stable seed independent of call ordering or future observations.
            local_seed = (seed + origin * 1009 + block * 9176) % (2**32)
            forecast = bootstrap_risk(training, horizon=horizon, block=block,
                                      simulations=simulations, seed=local_seed)
            p95 = forecast['p95_max_drawdown']
            results.append({'origin': origin, 'train_start': origin - train,
                            'test_end_exclusive': origin + horizon, 'block': block,
                            'forecast_p95': p95, 'realized_max_drawdown': realized,
                            'exceeded_p95': bool(realized > p95),
                            'absolute_error': abs(realized - forecast['mean_max_drawdown'])})
    summary = []
    for block in blocks:
        subset = [row for row in results if row['block'] == block]
        summary.append({'block': block, 'scored_periods': len(subset),
                        'p95_exceedances': sum(row['exceeded_p95'] for row in subset),
                        'mean_absolute_error': float(np.mean([row['absolute_error'] for row in subset]))})
    return {'data': 'user-supplied or synthetic; caller responsible for provenance',
            'train': train, 'horizon': horizon, 'step': step,
            'rows': results, 'summary': summary}


def main():
    parser = argparse.ArgumentParser(description='Synthetic-only walk-forward drawdown validation')
    parser.add_argument('--seed', type=int, default=2026)
    parser.add_argument('--observations', type=int, default=260)
    parser.add_argument('--simulations', type=int, default=200)
    args = parser.parse_args()
    if not 130 <= args.observations <= 100000:
        parser.error('observations must be between 130 and 100000')
    rng = np.random.default_rng(args.seed)
    r = np.clip(rng.normal(.001, .025, args.observations), -.95, 2)
    print(json.dumps(walkforward(r, simulations=args.simulations, seed=args.seed), indent=2))


if __name__ == '__main__':
    main()
