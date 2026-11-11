"""Lagged-target synthetic rebalancing with self-financing cost accounting."""
import math
from concentration import diagnostics, drift, turnover


def simulate(initial_weights, target_schedule, return_rows, cost_bps=10.0):
    """Targets are fixed before each period's returns; fees reduce invested wealth."""
    weights = list(initial_weights)
    diagnostics(weights)
    if isinstance(cost_bps, bool) or not isinstance(cost_bps, (int, float)) or not math.isfinite(cost_bps) or not 0 <= cost_bps < 10000:
        raise ValueError('cost_bps must be finite and in [0, 10000)')
    if not target_schedule or len(target_schedule) != len(return_rows):
        raise ValueError('matched nonempty targets and returns required')
    wealth = 1.0
    history = []
    for t, (target, returns) in enumerate(zip(target_schedule, return_rows)):
        target = list(target)
        diagnostics(target)
        if len(target) != len(weights):
            raise ValueError('target dimension mismatch')
        trn = turnover(weights, target)
        fee = wealth * trn * cost_bps / 10000.0
        wealth_after_cost = wealth - fee
        if wealth_after_cost <= 0:
            raise ValueError('costs exhaust wealth')
        after = drift(target, returns)
        gross = math.fsum(w * (1 + r) for w, r in zip(target, returns))
        wealth = wealth_after_cost * gross
        history.append({'period': t, 'turnover': trn, 'cost': fee,
                        'end_wealth': wealth, 'end_weights': after,
                        'hhi': diagnostics(after)['hhi']})
        weights = after
    return history


if __name__ == '__main__':
    initial = [0.5, 0.5]
    targets = [[0.5, 0.5]] * 3
    returns = [[0.2, -0.1], [-0.05, 0.1], [0.0, 0.03]]
    for bps in (0, 10, 50):
        rows = simulate(initial, targets, returns, bps)
        print(f'{bps} bps: final wealth={rows[-1]["end_wealth"]:.6f}, '
              f'turnover={sum(x["turnover"] for x in rows):.6f}')
