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

## Walk-forward ADV extension

`adv_walkforward.py` estimates dollar average daily volume (ADV) using **only completed historical sessions**. At forecast origin `t`, the trailing `window` observations `[t-window,t)` determine the estimate; the next `horizon` observations `[t,t+horizon)` are held out. Origins advance by the horizon so evaluation windows do not overlap. A synthetic volume drop demonstrates when forecast execution-day capacity underestimates realized capacity needs.

`forecast_max_days = max_i |Q_i| / (participation * forecast_ADV_i * stress_factor)`.
Held-out realized days use observed future ADV *only for scoring*, never for forecasting. Scenarios with 1.0, 0.5, and 0.25 stress multipliers are pre-specified, not tuned on test outcomes. These ratios are **proxies**, not execution forecasts.

```bash
cd quant-projects/10-liquidity-rebalancing
python adv_walkforward.py
python adv_walkforward.py --window 15 --horizon 5
python -m pytest -q test_adv_walkforward.py
```

Input arrays are aligned daily observations (days × assets). For any authorized historical study, record provider, retrieval date, symbol universe as known at each decision, adjustment policy, exchange calendar, corporate actions, and observation cutoff; do not commit licensed raw data. The included seeded data are entirely synthetic. There is no fill simulation, price impact calibration, execution feedback, survivorship adjustment, or independent validation. Future work: compare predicted capacity with real authorized point-in-time observations and add uncertainty intervals.


## Prequential capacity-forecast calibration

`calibration.py` adds a training-only empirical upper bound for the *maximum execution-day proxy*. Each origin first predicts from lagged ADV, then scores the following non-overlapping window. Only **earlier completed** forecast/outcome pairs calibrate the next origin. For earlier ratios `r = realized_days / predicted_days`, the conservative nearest-rank empirical `(1-alpha)` quantile `q` yields `upper_days = predicted_days * q`. The first three origins intentionally have **no interval**.

```bash
cd quant-projects/10-liquidity-rebalancing
python calibration.py
python calibration.py --alpha 0.2
python -m pytest -q test_calibration.py
```

The reported empirical coverage is a **descriptive held-out diagnostic**, not a guaranteed prediction-interval coverage rate. Small calibration samples, serial dependence, regime breaks, and the conservative finite-sample rank can materially affect reliability; the ratios are not exchangeable under liquidity shocks. The tool does not trade, model fills, or claim a validated liquidity risk model. The demo uses seeded synthetic observations only. Independent review and licensed point-in-time market validation remain outstanding.
