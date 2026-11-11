"""One-period arithmetic Brinson-Fachler sector attribution; synthetic only."""
import math


def attribute(sectors, portfolio_weights, benchmark_weights, portfolio_returns, benchmark_returns):
    """Return allocation, selection and interaction; weights are beginning-of-period."""
    n = len(sectors)
    if not 1 <= n <= 100 or len(set(sectors)) != n or any(not isinstance(s, str) or not s.strip() for s in sectors):
        raise ValueError('require 1..100 unique, nonempty sector names')
    arrays = (portfolio_weights, benchmark_weights, portfolio_returns, benchmark_returns)
    if any(len(a) != n for a in arrays):
        raise ValueError('all arrays must match sector count')
    if any(not math.isfinite(v) for a in arrays for v in a):
        raise ValueError('all numbers must be finite')
    wp, wb, rp, rb = arrays
    if any(w < 0 or w > 1 for w in (*wp, *wb)) or any(abs(sum(w) - 1) > 1e-9 for w in (wp, wb)):
        raise ValueError('long-only portfolio and benchmark weights must sum to one')
    if any(r < -1 for r in (*rp, *rb)):
        raise ValueError('simple returns cannot be below -100%')
    benchmark = math.fsum(w * r for w, r in zip(wb, rb))
    portfolio = math.fsum(w * r for w, r in zip(wp, rp))
    rows = []
    for name, p_w, b_w, p_r, b_r in zip(sectors, wp, wb, rp, rb):
        allocation = (p_w - b_w) * (b_r - benchmark)
        selection = b_w * (p_r - b_r)
        interaction = (p_w - b_w) * (p_r - b_r)
        rows.append({'sector': name, 'allocation': allocation, 'selection': selection,
                     'interaction': interaction, 'active': allocation + selection + interaction})
    effects = {k: math.fsum(row[k] for row in rows) for k in ('allocation', 'selection', 'interaction', 'active')}
    active = portfolio - benchmark
    if not math.isclose(effects['active'], active, rel_tol=1e-9, abs_tol=1e-12):
        raise ArithmeticError('attribution reconciliation failed')
    return {'portfolio_return': portfolio, 'benchmark_return': benchmark,
            'active_return': active, 'effects': effects, 'sectors': rows}


def main():
    result = attribute(('Technology', 'Healthcare', 'Utilities'),
                       (0.5, 0.3, 0.2), (0.4, 0.4, 0.2),
                       (0.12, 0.03, -0.01), (0.10, 0.04, 0.0))
    print('Synthetic single-period sector attribution (percentage points)')
    for key, value in result['effects'].items():
        print(f'{key}: {value * 100:+.4f}')
    print(f"active return: {result['active_return'] * 100:+.4f}")


if __name__ == '__main__':
    main()
