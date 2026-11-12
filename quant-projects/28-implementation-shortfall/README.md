# Project 28 — Implementation Shortfall and Execution Benchmarks

**Business question:** How much of an intended portfolio trade's value is lost between the decision-time *arrival price* and hypothetical execution? Unlike Project 10 (liquidity capacity), this lab focuses on **ex-post execution-quality accounting**, not portfolio rebalancing optimization.

This offline Python 3.11+ lab uses invented prices, quantities and market volumes. It does not connect to a broker, submit orders, fetch prices or redistribute market data.

## Mathematics

For intended quantity `Q`, arrival price `P0`, filled slices `(q_i, P_i)`, and side sign `s=+1` for buys or `-1` for sells:

- Filled price cost: `s * sum(q_i * (P_i - P0))`.
- Unfilled shares: `U = Q - sum(q_i)`.
- Opportunity-cost convention: `s * U * (P_terminal - P0)`; **not** an actual fill.
- Explicit fee: `fee_bps / 10000 * sum(q_i * P_i)`.
- Implementation shortfall (currency) = price cost + opportunity cost + fee.
- Implementation shortfall (bps) = `10000 * shortfall / (Q * P0)`.

Positive values mean a worse result than arrival; negative values can represent favorable price moves. For a sell, the price-cost sign reverses. An incomplete trade may have positive or negative marked opportunity cost. This **particular terminal-mark convention** is not universal; report it whenever comparing execution reports.

A predeclared participation cap requires `q_i <= max_participation * market_volume_i`. It is an input consistency check, not an impact model or a claim that liquidity existed.

## Reproduce

From the repository root:

```bash
cd quant-projects/28-implementation-shortfall
python -m unittest -v test_execution.py
python -m compileall -q execution.py test_execution.py
python execution.py --fee-bps 2
```

For 100 hypothetical buy shares at arrival 100, with 40 shares at 100.10, 35 at 100.30, and 25 at 100.50, price cost is 27 currency units; the 2-bps fee adds 2.0054, giving **29.0054 currency units / 29.0054 bps**. These are deterministic toy numbers, not observations.

## Guardrails, validation and limits

Inputs must be finite and positive (zero permitted for quantities and fees), slices must be typed, participation must be within (0,1], and fills cannot exceed intended quantity. Tests include sell sign, price improvement, unfilled marking, overfill, nonfinite values, and invalid caps. There is no spread decomposition, market impact estimation, intraday timestamp alignment, benchmark VWAP, queue position, survivorship correction or real-market data. No predictive execution quality, independent model review, production certification or investment advice is claimed.

**Next exercise:** Compare arrival-price and predeclared VWAP benchmarks on matched synthetic schedules, with deterministic price-path and fee stress. Any future real-data work must document provider, license, observation dates, and point-in-time availability.

## VWAP benchmark extension (synthetic)

The market volume-weighted average price is `sum(market_price * market_volume) / sum(market_volume)` over the **predeclared full observation window**. Execution VWAP is `sum(fill_price * fill_quantity) / sum(fill_quantity)` for filled shares only. Signed slippage is `side * 10000 * (execution_vwap / market_vwap - 1)` where side is +1 for buys and -1 for sells. Fees are added separately to currency-denominated cost; partial-fill opportunity cost is **not** silently included in VWAP slippage. No-fill cases return undefined execution VWAP and slippage, rather than zero.

Run from this directory:

```bash
python -m unittest -v test_benchmarks.py
python -m compileall -q benchmarks.py test_benchmarks.py
python benchmarks.py
```

The deterministic example uses three invented market bars and yields market VWAP 101, execution VWAP 101.035, and buy VWAP slippage approximately 3.4653 bps, before fees. **Interpretation:** this is a full-window benchmark; it is not arrival-price shortfall, and can be distorted by intraday timing, missing trades, venue selection, or a benchmark window chosen after observing outcomes. The calculation does not estimate market impact or prove best execution. No third-party data or broker actions are used.

## Execution-schedule sensitivity (synthetic)

**Business question:** How does a fixed *precommitted* front-loaded, even, or back-loaded schedule change fill rate and arrival-price shortfall when market volume, adverse price moves, fees and a participation cap vary? This is an **ex-post stress comparison**, not a schedule optimizer or an executable trading algorithm.

For target shares Q and schedule fractions f_i summing to one, filled shares in bar i are q_i = min(Q f_i, participation_cap × bar_volume_i). Capped shares are **not** moved to future bars. A hypothetical adverse impact assumption marks buy fills at P_i(1 + impact_bps/10000), and sell fills at P_i(1 − impact_bps/10000). Signed filled price cost is s Σ q_i(P_fill,i − P_arrival), with s=+1 for buys and −1 for sells. Add terminal-marked unfilled opportunity cost s(Q−Σq_i)(P_terminal−P_arrival) and explicit fees. Divide by Q × P_arrival and multiply by 10,000 for shortfall bps.

Run in this folder (Python 3.11+, standard library only):

```bash
python -m unittest -v test_schedule_sensitivity.py
python -m compileall -q schedule_sensitivity.py test_schedule_sensitivity.py
python schedule_sensitivity.py
```

The deterministic illustration uses 150 buy shares, 100 arrival price, three hypothetical bars with prices 100/101/102 and volumes 1000/300/1000, a 10% participation cap, 2 bps fees, and 5 bps adverse impact. Front/even/back schedules respectively produce approximately **66.3289 / 119.4615 / 166.3989 bps** shortfall and **90.00% / 86.67% / 90.00%** fill. The terminal mark is a chosen accounting convention; the impact is an assumed markup, **not a calibrated market-impact model**. The future price path is used only to score fixed schedules, never to select weights. No real-market prices, independent review, production certification, or best-execution claim.
