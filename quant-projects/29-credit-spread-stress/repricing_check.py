"""Independent fixed-cash-flow repricing benchmark; synthetic, not a default model."""
from math import exp, isfinite
from spread_stress import Position, scenario

def price(cashflows: list[tuple[float, float]], base_yield: float, spread: float) -> float:
    if not cashflows or not all(isfinite(x) for x in (base_yield, spread)):
        raise ValueError('finite yields and nonempty cash flows required')
    total = 0.0
    last = 0.0
    for t, cash in cashflows:
        if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and isfinite(x) for x in (t, cash)) or t <= last or cash <= 0:
            raise ValueError('cash flows must have increasing positive times and amounts')
        if abs((base_yield + spread) * t) > 700:
            raise ValueError('discount exponent outside safe range')
        total += cash * exp(-(base_yield + spread) * t)
        last = t
    if not isfinite(total) or total <= 0:
        raise ValueError('invalid discounted value')
    return total

def check(cashflows: list[tuple[float, float]], base_yield: float, spread: float, shock_bps: float) -> dict:
    if not isinstance(shock_bps, (int, float)) or isinstance(shock_bps, bool) or not isfinite(shock_bps) or abs(shock_bps) > 2000:
        raise ValueError('shock must be finite and within ±2000 bp')
    p0 = price(cashflows, base_yield, spread)
    weights = [(cash * exp(-(base_yield + spread) * t)) / p0 for t, cash in cashflows]
    duration = sum(w * t for w, (t, _) in zip(weights, cashflows))
    convexity = sum(w * t*t for w, (t, _) in zip(weights, cashflows))
    approx = scenario([Position('bond', p0, duration, convexity)], shock_bps)['pnl']
    exact = price(cashflows, base_yield, spread + shock_bps / 10000) - p0
    return {'base_price': p0, 'spread_duration': duration, 'spread_convexity': convexity,
            'approx_pnl': approx, 'repriced_pnl': exact, 'error': approx - exact,
            'error_bps_of_value': (approx - exact) / p0 * 10000}

if __name__ == '__main__':
    flows = [(float(y), 5.0 if y < 5 else 105.0) for y in range(1, 6)]
    for shock in (0, 25, 100, 500, -100):
        result = check(flows, 0.03, 0.015, shock)
        print(f'{shock:+5} bp | approximation {result["approx_pnl"]:+.6f} | repriced {result["repriced_pnl"]:+.6f} | error {result["error_bps_of_value"]:+.4f} bp of price')
