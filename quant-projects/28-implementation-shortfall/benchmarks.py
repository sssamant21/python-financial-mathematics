"""Synthetic VWAP execution benchmark; no orders or external data."""
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Bar:
    market_price: float
    market_volume: float
    fill_price: float
    fill_quantity: float

def _number(value, name, *, allow_zero=False):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0 or (value == 0 and not allow_zero):
        raise ValueError(f"invalid {name}")

def compare_vwap(arrival_price, target_quantity, bars, *, side="buy", fee_bps=0.0, max_participation=1.0):
    """Compare filled shares to full-window market VWAP; partial fills are reported separately."""
    _number(arrival_price, "arrival price")
    _number(target_quantity, "target quantity")
    _number(fee_bps, "fee", allow_zero=True)
    _number(max_participation, "participation")
    if max_participation > 1 or side not in ("buy", "sell") or not isinstance(bars, (list, tuple)) or not bars:
        raise ValueError("invalid side, participation or bars")
    market_notional = market_volume = fill_notional = filled = 0.0
    for bar in bars:
        if not isinstance(bar, Bar):
            raise ValueError("Bar required")
        _number(bar.market_price, "market price")
        _number(bar.market_volume, "market volume")
        _number(bar.fill_price, "fill price")
        _number(bar.fill_quantity, "fill quantity", allow_zero=True)
        if bar.fill_quantity > bar.market_volume * max_participation + 1e-9:
            raise ValueError("participation exceeded")
        market_notional += bar.market_price * bar.market_volume
        market_volume += bar.market_volume
        fill_notional += bar.fill_price * bar.fill_quantity
        filled += bar.fill_quantity
    if filled > target_quantity + 1e-9:
        raise ValueError("overfill")
    market_vwap = market_notional / market_volume
    execution_vwap = fill_notional / filled if filled else None
    direction = 1 if side == "buy" else -1
    fee = fill_notional * fee_bps / 10000
    return {"market_vwap": market_vwap, "execution_vwap": execution_vwap,
            "filled": filled, "unfilled": max(0, target_quantity - filled),
            "fill_rate": filled / target_quantity,
            "arrival_slippage_bps": (direction * (execution_vwap / arrival_price - 1) * 10000 if filled else None),
            "vwap_slippage_bps": (direction * (execution_vwap / market_vwap - 1) * 10000 if filled else None),
            "fees": fee, "vwap_cost_with_fees": direction * (fill_notional - filled * market_vwap) + fee}

def main():
    bars = [Bar(100, 1000, 100.1, 40), Bar(101, 1000, 101.2, 35), Bar(102, 1000, 102.3, 25)]
    for k, v in compare_vwap(100, 100, bars, fee_bps=2, max_participation=.1).items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
