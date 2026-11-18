"""Synthetic CDS protection-buyer PV and finite-difference credit sensitivities."""
import math


def _number(value, name, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number')
    if minimum is not None and value < minimum or maximum is not None and value > maximum:
        raise ValueError(f'{name} out of range')
    return float(value)


def legs(hazard, maturity=5, recovery=0.4, rate=0.02, frequency=4):
    h = _number(hazard, 'hazard', 0, 5)
    t = _number(maturity, 'maturity', 0.25, 30)
    r = _number(rate, 'rate', -0.1, 1)
    rec = _number(recovery, 'recovery', 0, 0.999999)
    if isinstance(frequency, bool) or not isinstance(frequency, int) or not 1 <= frequency <= 24:
        raise ValueError('frequency must be integer in [1,24]')
    n = round(t * frequency)
    if n < 1 or abs(n / frequency - t) > 1e-10:
        raise ValueError('maturity must align with coupon grid')
    premium = protection = 0.0
    previous = 1.0
    for i in range(1, n + 1):
        time = i / frequency
        survival = math.exp(-h * time)
        discount = math.exp(-r * time)
        premium += discount * survival / frequency
        protection += discount * (previous - survival) * (1 - rec)
        previous = survival
    return premium, protection


def pv(hazard, coupon, notional=1_000_000, **kwargs):
    c = _number(coupon, 'coupon', 0, 1)
    size = _number(notional, 'notional', 0.01, 1e12)
    annuity, protection = legs(hazard, **kwargs)
    return size * (protection - c * annuity)


def sensitivities(hazard=0.02, coupon=0.012, bump_bp=1.0, **kwargs):
    """Hazard01 is central hazard bump (forward at zero), not quote-based CS01."""
    h = _number(hazard, 'hazard', 0, 5)
    bump = _number(bump_bp, 'bump_bp', 0.001, 100) / 10000
    base = pv(h, coupon, **kwargs)
    annuity, protection = legs(h, **{k: v for k, v in kwargs.items() if k != 'notional'})
    notional = _number(kwargs.get('notional', 1_000_000), 'notional', 0.01, 1e12)
    coupon_dv01 = -notional * annuity * 0.0001
    if h + bump > 5:
        raise ValueError('hazard bump exceeds supported bound')
    upper = pv(h + bump, coupon, **kwargs)
    lower = pv(h - bump, coupon, **kwargs) if h >= bump else None
    hazard01 = (upper - lower) / 2 if lower is not None else upper - base
    return {'pv': base, 'par_spread_bp': 10000 * protection / annuity,
            'coupon_dv01': coupon_dv01, 'hazard01': hazard01,
            'hazard_difference': 'central' if lower is not None else 'forward'}


if __name__ == '__main__':
    for key, value in sensitivities().items():
        print(f'{key}: {value}')
