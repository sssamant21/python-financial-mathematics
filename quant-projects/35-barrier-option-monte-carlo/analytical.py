"""Independent reflection-density benchmark for a continuous GBM up-and-out call.

Zero dividends, constant risk-free rate and volatility; educational only.
"""
import argparse
import math


def _cdf(z):
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


def _truncated_call(mean, variance, lower, upper, spot, strike):
    """Integrate (spot*exp(x)-strike) N(mean,variance) on [lower,upper]."""
    sd = math.sqrt(variance)
    probability = _cdf((upper-mean)/sd) - _cdf((lower-mean)/sd)
    tilted = _cdf((upper-mean-variance)/sd) - _cdf((lower-mean-variance)/sd)
    return spot*math.exp(mean+variance/2)*tilted - strike*probability


def up_and_out_call(spot=100., strike=100., barrier=130., years=1., rate=0.02, vol=0.2):
    """Reflection-principle killed-density integral, not a Monte Carlo estimate."""
    values = (spot, strike, barrier, years, rate, vol)
    if (not all(math.isfinite(v) for v in values)
        or min(spot, strike, barrier, years, vol) <= 0
        or barrier <= spot or abs(rate*years) > 100
        or not 1e-6 <= vol*math.sqrt(years) <= 5
        or abs((rate-vol*vol/2)*years) > 100):
        raise ValueError("invalid or numerically unsafe benchmark parameters")
    if strike >= barrier:
        return 0.0
    variance = vol*vol*years
    mean = (rate-vol*vol/2)*years
    upper = math.log(barrier/spot)
    lower = math.log(strike/spot)
    direct = _truncated_call(mean,variance,lower,upper,spot,strike)
    reflected = math.exp(2*mean*upper/variance)*_truncated_call(
        2*upper+mean,variance,lower,upper,spot,strike)
    result = math.exp(-rate*years)*(direct-reflected)
    if not math.isfinite(result) or result < -1e-8:
        raise ValueError("unstable analytical evaluation")
    return max(0.,result)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spot',type=float,default=100.)
    p.add_argument('--strike',type=float,default=100.)
    p.add_argument('--barrier',type=float,default=130.)
    p.add_argument('--years',type=float,default=1.)
    p.add_argument('--rate',type=float,default=0.02)
    p.add_argument('--vol',type=float,default=0.2)
    a=p.parse_args()
    print({'continuous_up_and_out_call':up_and_out_call(**vars(a))})
