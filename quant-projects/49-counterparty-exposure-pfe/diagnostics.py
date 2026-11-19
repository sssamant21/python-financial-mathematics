"""Analytical benchmarks and uncertainty for synthetic Brownian exposure."""
import math
from statistics import NormalDist

def brownian_epe(*, notional, volatility, year, threshold=0.):
    """E[(N*sigma*sqrt(t)*Z-H)+] for Z standard normal."""
    for x in (notional, volatility, threshold):
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
            raise ValueError("inputs must be finite real numbers")
    if notional <= 0 or volatility < 0 or threshold < 0 or type(year) is not int or not 1 <= year <= 50:
        raise ValueError("invalid economic inputs")
    scale = notional * volatility * math.sqrt(year)
    if not math.isfinite(scale):
        raise ValueError("scale overflow")
    if scale == 0:
        return 0.
    z = threshold / scale
    return scale * math.exp(-.5*z*z) / math.sqrt(2*math.pi) - threshold * NormalDist().cdf(-z)

def brownian_pfe(*, notional, volatility, year, threshold=0., confidence=.95):
    """Population quantile of max(V-H,0); not a worst-case loss."""
    brownian_epe(notional=notional, volatility=volatility, year=year, threshold=threshold)
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence must lie strictly between zero and one")
    return max(notional * volatility * math.sqrt(year) * NormalDist().inv_cdf(confidence) - threshold, 0.)

def epe_standard_error(exposures):
    """IID pathwise sample-mean SE; not a PFE or CVA confidence bound."""
    if len(exposures) < 2 or any(isinstance(x, bool) or not isinstance(x, (int,float)) or not math.isfinite(x) or x < 0 for x in exposures):
        raise ValueError("need at least two finite nonnegative exposures")
    mean = math.fsum(exposures) / len(exposures)
    variance = math.fsum((x-mean)**2 for x in exposures) / (len(exposures)-1)
    return math.sqrt(variance/len(exposures))
