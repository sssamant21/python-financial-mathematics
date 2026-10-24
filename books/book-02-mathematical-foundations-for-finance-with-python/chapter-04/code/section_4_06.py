"""Section 4.6: multiplicative factors and additive log changes."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} cannot be represented as finite float") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def period_log_return(simple_return):
    r = finite(simple_return, "simple_return")
    if r <= -1:
        raise ValueError("simple return must exceed -1")
    return math.log1p(r)

def cumulative_log_return(simple_returns):
    returns = tuple(simple_returns)
    return math.fsum(period_log_return(r) for r in returns)

def cumulative_simple_return(simple_returns):
    return math.expm1(cumulative_log_return(simple_returns))

def price_path_log_return(prices):
    prices = tuple(prices)
    if len(prices) < 2:
        raise ValueError("at least two prices are required")
    values = [finite(x, f"prices[{i}]") for i, x in enumerate(prices)]
    if any(x <= 0 for x in values):
        raise ValueError("prices must be positive")
    return math.log(values[-1]) - math.log(values[0])

def portfolio_simple_return(asset_returns, weights):
    returns, weights = tuple(asset_returns), tuple(weights)
    if not returns or len(returns) != len(weights):
        raise ValueError("nonempty returns and matching weights required")
    rs = [finite(r, f"asset_returns[{i}]") for i, r in enumerate(returns)]
    ws = [finite(w, f"weights[{i}]") for i, w in enumerate(weights)]
    if any(r <= -1 for r in rs):
        raise ValueError("asset returns must exceed -1 for positive portfolio factors")
    if any(w < 0 for w in ws):
        raise ValueError("long-only weights must be nonnegative")
    if not math.isclose(math.fsum(ws), 1.0, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("weights must sum to one")
    return math.fsum(w * r for w, r in zip(ws, rs))

def portfolio_log_return(asset_returns, weights):
    return period_log_return(portfolio_simple_return(asset_returns, weights))

if __name__ == "__main__":
    changes = (0.10, -0.05, 0.08)
    print("Cumulative log return:", cumulative_log_return(changes))
    print("Cumulative simple return:", cumulative_simple_return(changes))
    print("Portfolio log return:", portfolio_log_return((0.2, -0.1), (0.5, 0.5)))
