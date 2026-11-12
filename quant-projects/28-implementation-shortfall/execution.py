"""Offline, synthetic implementation-shortfall accounting; no trading integration."""
import argparse
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Slice:
    price: float
    quantity: float
    market_volume: float

def positive(x, name, zero=False):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0 or (x == 0 and not zero):
        raise ValueError(f"{name} must be finite and positive"+(" or zero" if zero else ""))

def shortfall(arrival_price, target_quantity, slices, *, side="buy", fee_bps=0.0, max_participation=1.0, terminal_price=None):
    """Positive cost means worse than arrival. Unfilled quantity is marked, not traded."""
    positive(arrival_price, "arrival_price")
    positive(target_quantity, "target_quantity")
    positive(fee_bps, "fee_bps", True)
    positive(max_participation, "max_participation")
    if max_participation > 1 or side not in ("buy", "sell"):
        raise ValueError("invalid participation or side")
    if not isinstance(slices, (tuple, list)) or not slices or any(not isinstance(row, Slice) for row in slices):
        raise ValueError("nonempty sequence of Slice required")
    if terminal_price is None:
        terminal_price = slices[-1].price
    positive(terminal_price, "terminal_price")
    direction = 1 if side == "buy" else -1
    filled = notional = price_cost = 0.0
    for row in slices:
        positive(row.price, "price")
        positive(row.quantity, "quantity", True)
        positive(row.market_volume, "market_volume")
        if row.quantity > row.market_volume * max_participation + 1e-9:
            raise ValueError("participation cap exceeded")
        filled += row.quantity
        notional += row.price * row.quantity
        price_cost += direction * (row.price - arrival_price) * row.quantity
    if filled > target_quantity + 1e-9:
        raise ValueError("overfill")
    unfilled = max(0.0, target_quantity - filled)
    opportunity_cost = direction * (terminal_price - arrival_price) * unfilled
    fees = notional * fee_bps / 10000
    total = price_cost + opportunity_cost + fees
    return dict(filled=filled, unfilled=unfilled, price_cost=price_cost,
                opportunity_cost=opportunity_cost, fees=fees, total_cost=total,
                shortfall_bps=10000 * total / (arrival_price * target_quantity))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fee-bps", type=float, default=2.0)
    args = parser.parse_args()
    rows = [Slice(100.10, 40, 1000), Slice(100.30, 35, 1000), Slice(100.50, 25, 1000)]
    result = shortfall(100, 100, rows, fee_bps=args.fee_bps, max_participation=0.1)
    for key, value in result.items():
        print(f"{key}: {value:.4f}")

if __name__ == "__main__":
    main()
