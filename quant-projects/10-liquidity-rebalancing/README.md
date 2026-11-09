# Project 10 — Liquidity-Aware Rebalancing and Execution Capacity

**Business question:** A target portfolio may look attractive in a backtest, but how many days might it take to rebalance without exceeding a fraction of typical daily volume, and what could trading cost?

## Mathematics

For equity `E`, current holding `H_i`, and target weight `w_i`, the dollar trade is `Q_i = E*w_i - H_i`. Dollar daily volume is `ADV_i = price_i * shares_per_day_i`. At participation cap `p` and stressed volume multiplier `s`, the minimum execution-day proxy is `abs(Q_i)/(p*ADV_i*s)`. One-way turnover is `sum(abs(Q_i))/(2*E)`.

A deliberately stylized transaction-cost proxy charges half the quoted spread and square-root market impact per dollar traded:

`cost_i = abs(Q_i) * (spread_bps/20000 + impact_bps/10000 * sqrt(abs(Q_i)/(ADV_i*s)))`.

The impact coefficient is illustrative, **not empirically calibrated**. The execution-day proxy assumes stable volume, no market movement, and no execution interference; it is not a fill guarantee.

## Run

Python 3.11+, `numpy>=1.26,<3`, `pytest>=8,<10`; the repository shared requirements are compatible.

```bash
cd quant-projects/10-liquidity-rebalancing
python liquidity.py
python liquidity.py --volume-factor 0.25 --participation 0.05
python -m pytest -q test_liquidity.py
```

The deterministic example rebalances a fictional $100,000 portfolio from 60/40 to 40/60. The JSON output includes trades, turnover, capacity days, and modeled costs. No broker connection or market-data download is used.

## Guardrails and limitations

- Long-only, fully invested inputs only: holdings nonnegative and summing to equity; weights nonnegative and summing to one.
- All inputs finite; prices and volumes positive; participation and volume stress in (0,1]; spread and impact coefficients nonnegative.
- No market-impact calibration, order-book depth, cross-impact, fees, taxes, price drift, or liquidity feedback.
- For historical analysis, obtain authorized point-in-time prices and volumes on demand, record provider and observation dates, corporate actions, missing observations, and investable universe. Do not redistribute third-party market data without permission.
- Use lagged volume estimates known at the decision time; same-day realized volume is future information if the order is decided before the close.
- Synthetic educational diagnostics only: no investment advice, trading actions, independent review, or production certification.

## Validation and next milestone

Tests check trade self-financing, turnover, execution-day arithmetic, stressed-volume monotonicity, no-trade costs, and input rejection. Published-revision CI and independent review must be verified separately.

Next: point-in-time rolling ADV estimates and held-out liquidity-shock scoring with an explicit signal-to-execution lag.
