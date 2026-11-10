"""Numerical stability diagnostics for European option Greeks; synthetic inputs only."""
import argparse
import math
from statistics import NormalDist
from black_scholes import price, greeks_fd, _inputs

_NORMAL = NormalDist()

def analytic_greeks(kind, spot, strike, maturity, rate, volatility, dividend=0.0):
    """Closed-form spot delta, gamma, vega (vega per unit volatility)."""
    _inputs(spot, strike, maturity, rate, volatility, dividend)
    if kind not in ("call", "put"):
        raise ValueError("kind must be call or put")
    d1 = (math.log(spot / strike) + (rate - dividend + 0.5 * volatility**2) * maturity) / (volatility * math.sqrt(maturity))
    discount = math.exp(-dividend * maturity)
    pdf = math.exp(-0.5 * d1 * d1) / math.sqrt(2 * math.pi)
    delta = discount * (_NORMAL.cdf(d1) if kind == "call" else _NORMAL.cdf(d1) - 1)
    gamma = discount * pdf / (spot * volatility * math.sqrt(maturity))
    vega = spot * discount * pdf * math.sqrt(maturity)
    return {"delta": delta, "gamma": gamma, "vega": vega}

def diagnose(kind="call", spot=100.0, strike=100.0, rate=0.05, dividend=0.0,
             scenarios=((1.0, 0.2), (1/365, 0.2), (1/365, 0.01)),
             relative_spot_step=1e-4, relative_vol_step=1e-3):
    """Compare central differences to analytic Greeks at fixed hypothetical inputs.

    Results are descriptive; unstable finite differences are flagged, not repaired.
    """
    if not scenarios or len(scenarios) > 30:
        raise ValueError("require 1..30 scenarios")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x <= 0 for x in (relative_spot_step, relative_vol_step)):
        raise ValueError("steps must be finite and positive")
    if relative_spot_step >= 0.1 or relative_vol_step >= 0.5:
        raise ValueError("steps exceed educational bounds")
    rows = []
    for maturity, volatility in scenarios:
        _inputs(spot, strike, maturity, rate, volatility, dividend)
        h = spot * relative_spot_step
        v = volatility * relative_vol_step
        exact = analytic_greeks(kind, spot, strike, maturity, rate, volatility, dividend)
        numeric = greeks_fd(kind, spot, strike, maturity, rate, volatility, dividend, h, v)
        errors = {key: abs(numeric[key] - exact[key]) for key in exact}
        # Mixed absolute/relative tolerance avoids dividing by near-zero Greeks.
        stable = all(errors[key] <= 1e-4 + 0.01 * abs(exact[key]) for key in exact)
        rows.append({"years": maturity, "volatility": volatility,
                     "price": price(kind, spot, strike, maturity, rate, volatility, dividend),
                     "analytic": exact, "finite_difference": numeric,
                     "absolute_error": errors, "within_tolerance": stable})
    return rows

def main():
    parser = argparse.ArgumentParser(description="Synthetic Black-Scholes numerical stability diagnostic")
    parser.add_argument("--kind", choices=("call", "put"), default="call")
    args = parser.parse_args()
    for row in diagnose(kind=args.kind):
        print(f"T={row['years']:.8f} sigma={row['volatility']:.4f} "
              f"gamma_error={row['absolute_error']['gamma']:.6g} "
              f"within_tolerance={row['within_tolerance']}")
    print("Educational synthetic diagnostics; no market calibration or trading.")

if __name__ == "__main__":
    main()
