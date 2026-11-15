"""Static no-arbitrage checks for same-expiry European call mid prices."""
import math


def diagnose(strikes, calls, *, discount=1.0, tolerance=1e-10):
    """Check call bounds, monotonicity, vertical slopes and convexity on irregular grids.

    discount is exp(-rT); this is a necessary-condition diagnostic, not certification.
    """
    if len(strikes) != len(calls) or len(strikes) < 3:
        raise ValueError('at least three aligned quotes required')
    if not (math.isfinite(discount) and 0 < discount <= 2):
        raise ValueError('invalid discount factor')
    if not (math.isfinite(tolerance) and 0 <= tolerance <= 1e-4):
        raise ValueError('invalid tolerance')
    if any(not isinstance(x, (float, int)) or isinstance(x, bool) or not math.isfinite(x) for x in (*strikes, *calls)):
        raise ValueError('nonfinite or nonnumeric quote')
    if any(k <= 0 for k in strikes) or any(strikes[i+1] <= strikes[i] for i in range(len(strikes)-1)):
        raise ValueError('strikes must be positive and strictly increasing')
    slopes = [(calls[i+1]-calls[i])/(strikes[i+1]-strikes[i]) for i in range(len(strikes)-1)]
    issues = []
    for i, c in enumerate(calls):
        if c < -tolerance:
            issues.append(f'negative_call:{i}')
    for i, s in enumerate(slopes):
        if s > tolerance:
            issues.append(f'monotonicity:{i}')
        if s < -discount-tolerance:
            issues.append(f'vertical_spread_bound:{i}')
    for i in range(len(slopes)-1):
        if slopes[i+1] < slopes[i]-tolerance:
            issues.append(f'convexity:{i+1}')
    return {'valid': not issues, 'issues': issues, 'slopes': slopes}


def sample():
    strikes = [80., 90., 100., 110., 120.]
    calls = [23., 16., 10., 6., 3.]
    return strikes, calls


if __name__ == '__main__':
    import json
    k, c = sample()
    print(json.dumps({'strikes': k, 'calls': c, **diagnose(k, c)}, indent=2))
