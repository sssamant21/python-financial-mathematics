"""European Black-Scholes-Merton educational benchmark; no market data or orders."""
import argparse
import math
from statistics import NormalDist

_NORMAL = NormalDist()

def _inputs(spot, strike, maturity, rate, volatility, dividend):
    values = (spot, strike, maturity, rate, volatility, dividend)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError('all inputs must be finite real numbers')
    if spot <= 0 or strike <= 0 or maturity <= 0 or volatility <= 0:
        raise ValueError('spot, strike, maturity and volatility must be positive')
    if maturity > 100 or volatility > 5 or abs(rate) > 1 or abs(dividend) > 1:
        raise ValueError('input outside educational guardrails')

def price(kind, spot, strike, maturity, rate, volatility, dividend=0.0):
    """European option present value with continuously compounded r and q."""
    _inputs(spot, strike, maturity, rate, volatility, dividend)
    if kind not in ('call', 'put'):
        raise ValueError('kind must be call or put')
    d1 = (math.log(spot / strike) + (rate - dividend + 0.5 * volatility**2) * maturity) / (volatility * math.sqrt(maturity))
    d2 = d1 - volatility * math.sqrt(maturity)
    discounted_spot = spot * math.exp(-dividend * maturity)
    discounted_strike = strike * math.exp(-rate * maturity)
    if kind == 'call':
        value = discounted_spot * _NORMAL.cdf(d1) - discounted_strike * _NORMAL.cdf(d2)
    else:
        value = discounted_strike * _NORMAL.cdf(-d2) - discounted_spot * _NORMAL.cdf(-d1)
    if not math.isfinite(value):
        raise ValueError('nonfinite valuation')
    return max(0.0, value)

def parity_residual(spot, strike, maturity, rate, volatility, dividend=0.0):
    """Call - put - (S exp(-qT) - K exp(-rT)); should be ~0."""
    return (price('call', spot, strike, maturity, rate, volatility, dividend)
            - price('put', spot, strike, maturity, rate, volatility, dividend)
            - (spot * math.exp(-dividend * maturity) - strike * math.exp(-rate * maturity)))

def greeks_fd(kind, spot, strike, maturity, rate, volatility, dividend=0.0,
              spot_step=0.01, vol_step=0.0001):
    """Central differences for spot delta/gamma and volatility vega (per 1.0 vol)."""
    _inputs(spot, strike, maturity, rate, volatility, dividend)
    if not (0 < spot_step < spot and 0 < vol_step < volatility):
        raise ValueError('finite difference steps must be positive and preserve valid inputs')
    base = price(kind, spot, strike, maturity, rate, volatility, dividend)
    up = price(kind, spot + spot_step, strike, maturity, rate, volatility, dividend)
    down = price(kind, spot - spot_step, strike, maturity, rate, volatility, dividend)
    vu = price(kind, spot, strike, maturity, rate, volatility + vol_step, dividend)
    vd = price(kind, spot, strike, maturity, rate, volatility - vol_step, dividend)
    return {'delta': (up - down)/(2*spot_step),
            'gamma': (up - 2*base + down)/(spot_step**2),
            'vega': (vu - vd)/(2*vol_step)}

def main():
    p = argparse.ArgumentParser(description='Hypothetical European Black-Scholes benchmark')
    p.add_argument('--spot', type=float, default=100)
    p.add_argument('--strike', type=float, default=100)
    p.add_argument('--years', type=float, default=1)
    p.add_argument('--rate', type=float, default=0.05)
    p.add_argument('--volatility', type=float, default=0.2)
    p.add_argument('--dividend', type=float, default=0)
    a = p.parse_args()
    args = (a.spot, a.strike, a.years, a.rate, a.volatility, a.dividend)
    for kind in ('call', 'put'):
        print(f'{kind}: {price(kind, *args):.6f}; finite_difference_greeks={greeks_fd(kind, *args)}')
    print(f'put_call_parity_residual={parity_residual(*args):.3g}')
    print('Hypothetical model values only; not executable prices or trading advice.')

if __name__ == '__main__':
    main()
