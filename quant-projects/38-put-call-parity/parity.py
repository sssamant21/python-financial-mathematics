"""Synthetic European put-call parity diagnostics; no trading instructions."""
import math

def parity_bounds(spot, strike, years, rate, dividend_yield, call_bid, call_ask, put_bid, put_ask):
    vals = (spot, strike, years, rate, dividend_yield, call_bid, call_ask, put_bid, put_ask)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in vals):
        raise ValueError('all inputs must be finite numbers')
    if spot <= 0 or strike <= 0 or years <= 0 or years > 100 or abs(rate) > 1 or abs(dividend_yield) > 1:
        raise ValueError('invalid market conventions')
    if min(call_bid, call_ask, put_bid, put_ask) < 0 or call_bid > call_ask or put_bid > put_ask:
        raise ValueError('invalid quote intervals')
    discounted_spot = spot * math.exp(-dividend_yield * years)
    discounted_strike = strike * math.exp(-rate * years)
    theoretical_difference = discounted_spot - discounted_strike
    lower = call_bid - put_ask
    upper = call_ask - put_bid
    return {'theoretical_call_minus_put': theoretical_difference,
            'quoted_lower': lower, 'quoted_upper': upper,
            'compatible': lower <= theoretical_difference <= upper,
            'gap': max(lower - theoretical_difference, theoretical_difference - upper, 0.0)}

if __name__ == '__main__':
    print(parity_bounds(100, 100, 1, 0.03, 0.01, 9, 10, 7, 8))
