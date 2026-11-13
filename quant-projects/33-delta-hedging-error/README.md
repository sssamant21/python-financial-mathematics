# Project 33 — Discrete Delta-Hedging Error and Transaction Costs

**Question:** Why can a theoretically delta-hedged European call still generate a nonzero realized P&L? This lab simulates a *short* hypothetical European call hedged by a long stock position, with cash earning a constant rate. No real prices, broker connections, or trading instructions.

## Math and business context

Under risk-neutral GBM, each synthetic step follows `S_next = S exp((r - sigma²/2) dt + sigma sqrt(dt) Z)`, where independent `Z ~ N(0,1)`. The Black–Scholes call delta is `N(d1)`. Initially sell one call for its theoretical premium, purchase delta shares, and hold the remaining proceeds (possibly negative) in cash. At each selected date, adjust shares to the new model delta and charge `abs(shares_traded) * spot * cost_bps / 10000`. Cash accrues at `exp(r dt)`; at expiry settle the option payoff and liquidate the stock, charging the closing cost. **Hedge P&L** is terminal cash plus stock value minus call payoff and closing cost.

Even with correct model parameters, discrete hedging leaves *gamma/discretization error*. More frequent hedging can reduce exposure to price moves but increase turnover and fees. RMSE summarizes P&L dispersion around zero, **not** investment returns or guaranteed hedging effectiveness.

## Reproduce (Python 3.11+ standard library only)

```bash
cd quant-projects/33-delta-hedging-error
python -m unittest -v test_hedge.py
python -m compileall -q hedge.py test_hedge.py
python hedge.py --paths 100
```

The predeclared comparison uses rebalance intervals of 1, 4 and 13 weekly steps; 0 and 5 basis-point proportional costs; and 100 fixed independent synthetic paths (seeds 2026–2125). A given seed produces the **same terminal path across scenarios** for paired comparisons. The model assumes a frictionless borrowing rate, no dividends, no volatility changes, no jumps, no bid/ask dynamics beyond the simplified fee, and continuous option-model inputs. The first hedge and final liquidation incur costs. This is a synthetic teaching experiment, not a backtest, market forecast, financial advice, or production risk system.

## Validation boundaries

Seven deterministic `unittest` methods cover Black–Scholes reference price/delta, expiry payoffs, repeatability, cost drag, rebalance sensitivity, scenario shape and rejected inputs. No third-party data or dependencies are redistributed. Exact-source hosted CI, historical market calibration, and independent model review must be verified separately. Next: predeclare path-count/volatility sensitivity and benchmark cost-free discrete hedging error across increasingly fine grids without interpreting a single sample as a convergence proof.

## Paired path-count and volatility sensitivity

Run `python -m unittest -v test_sensitivity.py` and `python sensitivity.py --paths 40`.
The extension predeclares nested path counts 40/160/640, annualized model
volatilities 10%/20%/40%, and hedge intervals 1/4/13 weekly steps. For each
volatility and frequency it reuses identical seeded shocks for zero-cost and
5-bps cases, allowing a paired estimate of **cost drag**. Across volatility
scenarios the shocks match but simulated price paths do not. Each row reports
the mean terminal hedging P&L, root-mean-square error, sample standard error
of the mean, a descriptive normal 95% Monte Carlo interval, mean paired
cost drag, and its standard error. The interval measures **simulation sampling
uncertainty conditional on this GBM model**, not a confidence bound on future
hedging performance or a guarantee of coverage. Nested path counts are not
independent experiments. Increasing the number of paths reduces Monte Carlo
noise, **not** time-discretization bias. No monotonic convergence of realized
RMSE or cost drag is assumed. Outputs are synthetic and require independent
numerical review; no historical-market calibration is claimed.
