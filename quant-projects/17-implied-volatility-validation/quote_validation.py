"""Synthetic European call/put bid-ask consistency; educational only."""
import math
from implied_vol import bounds, implied_vol

def validate_quotes(s, k, t, r, call_bid, call_ask, put_bid, put_ask, q=0):
    """Return parity and no-arbitrage diagnostics; reject invalid quotes."""
    cb = bounds("call", s, k, t, r, q)
    pb = bounds("put", s, k, t, r, q)
    quotes = (call_bid, call_ask, put_bid, put_ask)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in quotes):
        raise ValueError("quotes must be finite numbers")
    if call_bid > call_ask or put_bid > put_ask:
        raise ValueError("crossed bid/ask spread")
    if any(v < 0 for v in quotes):
        raise ValueError("negative option quote")
    if not (cb[0] <= call_bid <= call_ask <= cb[1] and pb[0] <= put_bid <= put_ask <= pb[1]):
        raise ValueError("quote violates European no-arbitrage bounds")
    parity = s * math.exp(-q*t) - k * math.exp(-r*t)
    low = call_bid - put_ask
    high = call_ask - put_bid
    if not low - 1e-10 <= parity <= high + 1e-10:
        raise ValueError("call/put bid-ask parity interval excludes forward value")
    return {"parity": parity, "parity_interval": (low, high),
            "call_spread": call_ask-call_bid, "put_spread": put_ask-put_bid}

def iv_intervals(s, k, t, r, call_bid, call_ask, put_bid, put_ask, q=0):
    """Infer IV ranges only for strictly interior quotes and bracketed roots."""
    diagnostics = validate_quotes(s,k,t,r,call_bid,call_ask,put_bid,put_ask,q)
    intervals = {}
    for kind, bid, ask in (("call",call_bid,call_ask),("put",put_bid,put_ask)):
        lo = implied_vol(kind,s,k,t,r,bid,q)
        hi = implied_vol(kind,s,k,t,r,ask,q)
        intervals[kind] = (lo,hi)
    return {"validation":diagnostics, "iv_intervals":intervals}

if __name__ == "__main__":
    from implied_vol import price
    args = (100.,100.,1.,.05)
    c = price("call",*args,.2)
    p = price("put",*args,.2)
    print(iv_intervals(*args,c-.02,c+.02,p-.02,p+.02))
