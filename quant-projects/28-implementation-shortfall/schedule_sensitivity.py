"""Deterministic hypothetical execution schedules; no broker or market data."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class MarketBar:
    price: float
    volume: float

def _valid(x, *, positive=False):
    return type(x) in (int, float) and math.isfinite(x) and (x > 0 if positive else x >= 0)

def evaluate_schedule(bars, quantity, fractions, *, arrival_price, side='buy', fee_bps=0., participation=0.1, impact_bps=0.):
    """Allocate precommitted target fractions to bars, with no carry-forward of capped shares.

    Price impact is an explicitly hypothetical adverse bps markup on each filled share.
    Unfilled opportunity cost is marked at the last bar, not treated as a fill.
    """
    if not isinstance(bars, (list, tuple)) or not bars or not all(isinstance(b, MarketBar) for b in bars):
        raise ValueError('nonempty MarketBar sequence required')
    if not isinstance(fractions, (list, tuple)) or len(fractions) != len(bars):
        raise ValueError('one fraction per bar required')
    if not all(_valid(x) for x in fractions) or not math.isclose(sum(fractions), 1., rel_tol=0., abs_tol=1e-10):
        raise ValueError('fractions must be nonnegative and sum to one')
    if not all(_valid(b.price, positive=True) and _valid(b.volume) for b in bars):
        raise ValueError('invalid bar')
    if not (_valid(quantity, positive=True) and _valid(arrival_price, positive=True) and _valid(fee_bps) and _valid(impact_bps) and _valid(participation, positive=True) and participation <= 1):
        raise ValueError('invalid quantity, price, cost, or cap')
    if side not in ('buy', 'sell'):
        raise ValueError('invalid side')
    sign = 1 if side == 'buy' else -1
    filled = notional = 0.
    for bar, fraction in zip(bars, fractions):
        fill = min(quantity * fraction, bar.volume * participation)
        price = bar.price * (1 + sign * impact_bps / 10000)
        if price <= 0 or not math.isfinite(price):
            raise ValueError('invalid impacted price')
        filled += fill
        notional += fill * price
    unfilled = max(0., quantity - filled)
    price_cost = sign * (notional - filled * arrival_price)
    opportunity = sign * unfilled * (bars[-1].price - arrival_price)
    fees = notional * fee_bps / 10000
    total = price_cost + opportunity + fees
    if not all(math.isfinite(v) for v in (filled, unfilled, total)):
        raise ValueError('numeric overflow')
    return {'filled': filled, 'unfilled': unfilled, 'fill_rate': filled / quantity,
            'price_cost': price_cost, 'opportunity_cost': opportunity,
            'fees': fees, 'shortfall': total, 'shortfall_bps': total / (quantity * arrival_price) * 10000}

def main():
    bars = [MarketBar(100, 1000), MarketBar(101, 300), MarketBar(102, 1000)]
    for name, weights in [('front', [0.6, 0.3, 0.1]), ('even', [1/3]*3), ('back', [0.1, 0.3, 0.6])]:
        result = evaluate_schedule(bars, 150, weights, arrival_price=100, participation=.1, fee_bps=2, impact_bps=5)
        print(f'{name}: fill={result["fill_rate"]:.2%}, shortfall={result["shortfall_bps"]:.4f} bps')

if __name__ == '__main__':
    main()
