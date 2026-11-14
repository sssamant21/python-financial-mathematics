"""Synthetic Black-Scholes implied volatility; standard library only."""
import argparse
import math

def cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))

def price(spot, strike, years, rate, sigma, kind="call"):
    if kind not in ("call", "put") or not all(math.isfinite(x) for x in (spot, strike, years, rate, sigma)) or min(spot, strike, years) <= 0 or sigma < 0:
        raise ValueError("invalid model inputs")
    disc = math.exp(-rate * years)
    if not math.isfinite(disc) or disc <= 0:
        raise ValueError("invalid discount factor")
    if sigma == 0:
        call = max(spot - strike * disc, 0.0)
    else:
        d1 = (math.log(spot / strike) + (rate + sigma*sigma/2)*years)/(sigma*math.sqrt(years))
        d2 = d1 - sigma*math.sqrt(years)
        call = spot*cdf(d1) - strike*disc*cdf(d2)
    return call if kind == "call" else call - spot + strike*disc

def implied_vol(quote, spot, strike, years, rate, kind="call", max_sigma=5.0, tolerance=1e-9, iterations=120):
    if not math.isfinite(quote) or quote < 0 or not math.isfinite(max_sigma) or max_sigma <= 0 or not math.isfinite(tolerance) or tolerance <= 0 or type(iterations) is not int or iterations < 1:
        raise ValueError("invalid solver inputs")
    lower = price(spot, strike, years, rate, 0.0, kind)
    upper = price(spot, strike, years, rate, max_sigma, kind)
    if quote < lower-tolerance or quote > upper+tolerance:
        raise ValueError("quote outside attainable finite volatility bracket")
    if abs(quote-lower) <= tolerance:
        return 0.0
    if abs(quote-upper) <= tolerance:
        return max_sigma
    lo, hi = 0.0, max_sigma
    for _ in range(iterations):
        mid = (lo+hi)/2
        val = price(spot, strike, years, rate, mid, kind)
        if abs(val-quote) <= tolerance:
            return mid
        if val < quote:
            lo = mid
        else:
            hi = mid
    raise RuntimeError("solver did not converge")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Synthetic option quote implied-volatility inversion")
    p.add_argument("--spot", type=float, default=100)
    p.add_argument("--strike", type=float, default=105)
    p.add_argument("--years", type=float, default=1)
    p.add_argument("--rate", type=float, default=0.02)
    p.add_argument("--vol", type=float, default=0.25)
    p.add_argument("--kind", choices=("call", "put"), default="call")
    a = p.parse_args()
    q = price(a.spot, a.strike, a.years, a.rate, a.vol, a.kind)
    print(f"synthetic_quote={q:.8f} recovered_annual_vol={implied_vol(q,a.spot,a.strike,a.years,a.rate,a.kind):.8f}")
