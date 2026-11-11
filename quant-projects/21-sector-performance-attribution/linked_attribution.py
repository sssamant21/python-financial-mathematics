"""Exact two-period geometric linking of single-period Brinson-Fachler effects."""
import math
from attribution import attribute

KEYS = ('allocation', 'selection', 'interaction')

def link_two_periods(first, second):
    """Link arithmetic effects: first scaled by second portfolio gross return,
    second scaled by first benchmark gross return. No external cash flows."""
    for x in (first, second):
        if not isinstance(x, dict) or any(k not in x for k in ('portfolio_return', 'benchmark_return', 'effects')):
            raise ValueError('expected attribute() outputs')
        if any(not isinstance(x[k], (int, float)) or not math.isfinite(x[k]) or x[k] < -1
               for k in ('portfolio_return', 'benchmark_return')):
            raise ValueError('invalid period return')
        if any(k not in x['effects'] or not isinstance(x['effects'][k], (int, float))
               or not math.isfinite(x['effects'][k]) for k in KEYS):
            raise ValueError('invalid attribution effects')
        if not math.isclose(math.fsum(x['effects'][k] for k in KEYS),
                            x['portfolio_return'] - x['benchmark_return'], abs_tol=1e-11):
            raise ValueError('period attribution does not reconcile')
    p1, b1 = first['portfolio_return'], first['benchmark_return']
    p2, b2 = second['portfolio_return'], second['benchmark_return']
    effects = {k: math.fsum((first['effects'][k] * (1 + p2),
                              second['effects'][k] * (1 + b1))) for k in KEYS}
    portfolio = (1+p1)*(1+p2)-1
    benchmark = (1+b1)*(1+b2)-1
    active = portfolio - benchmark
    if not math.isclose(math.fsum(effects.values()), active, rel_tol=1e-9, abs_tol=1e-11):
        raise ArithmeticError('linked attribution reconciliation failed')
    return {'portfolio_total': portfolio, 'benchmark_total': benchmark,
            'active_total': active, 'linked_effects': effects,
            'period_scales': (1+p2, 1+b1)}

def main():
    a = attribute(('Tech', 'Health'), (.6, .4), (.5, .5), (.1, .02), (.08, .03))
    b = attribute(('Tech', 'Health'), (.55, .45), (.5, .5), (-.06, .04), (-.04, .02))
    result = link_two_periods(a, b)
    print('Synthetic linked attribution (percentage points)')
    for key, value in result['linked_effects'].items():
        print(f'{key}: {value*100:+.6f}')
    print(f"compounded active: {result['active_total']*100:+.6f}")

if __name__ == '__main__':
    main()
