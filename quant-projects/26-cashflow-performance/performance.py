"""Synthetic time-weighted and money-weighted performance, no external dependencies."""
import math


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    return float(value)


def evaluate(start_nav, end_navs, contributions):
    """Flows occur at each period START; end_navs are period-end valuations.

    contributions[i] is deposited (+) or withdrawn (-) immediately before
    period i's investment return. No final-period terminal flow is assumed.
    """
    start = _number(start_nav, 'start_nav')
    if start <= 0 or not isinstance(end_navs, (list, tuple)) or not isinstance(contributions, (list, tuple)):
        raise ValueError('positive start NAV and list/tuple histories required')
    if not 1 <= len(end_navs) <= 10000 or len(end_navs) != len(contributions):
        raise ValueError('histories must have matching lengths from 1 to 10000')
    previous = start
    factors = []
    invested = []
    for i, (nav_raw, flow_raw) in enumerate(zip(end_navs, contributions)):
        nav = _number(nav_raw, f'end_navs[{i}]')
        flow = _number(flow_raw, f'contributions[{i}]')
        base = previous + flow
        if base <= 0 or nav <= 0 or not math.isfinite(base):
            raise ValueError('post-flow capital and ending NAV must be positive and finite')
        factor = nav / base
        if not math.isfinite(factor) or factor <= 0:
            raise ValueError('nonfinite growth factor')
        factors.append(factor)
        invested.append(flow)
        previous = nav
    twr_factor = math.prod(factors)
    if not math.isfinite(twr_factor):
        raise ValueError('nonfinite cumulative return')
    # Investor cash flows at integer boundaries: initial outflow,
    # intermediate deposits, and final liquidation.
    cashflows = [-start - invested[0]] + [-x for x in invested[1:]] + [previous]
    return {'twr': twr_factor - 1, 'mwr': _irr(cashflows), 'period_returns': tuple(x - 1 for x in factors), 'cashflows': tuple(cashflows)}


def _irr(cashflows):
    """Unique IRR for an initial outflow, subsequent deposits and final inflow."""
    if cashflows[0] >= 0 or cashflows[-1] <= 0 or any(x > 0 for x in cashflows[1:-1]):
        return None

    def npv(rate):
        factor = 1.0 + rate
        value = cashflows[-1]
        for amount in reversed(cashflows[:-1]):
            value = amount + value / factor
        return value

    lo, hi = -0.999999999, 1.0
    while npv(hi) > 0 and hi < 1e12:
        hi = 2 * hi + 1
    if npv(hi) > 0:
        return None
    for _ in range(180):
        mid = (lo + hi) / 2
        if npv(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == '__main__':
    result = evaluate(100, [120, 198], [0, 100])
    print(f"Synthetic TWR: {result['twr']:.6f}; periodic MWR: {result['mwr']:.6f}")
