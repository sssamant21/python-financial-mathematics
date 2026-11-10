# Project 16 — European Option Expiry Payoffs and Stress Scenarios

**Business question:** What is the hypothetical profit or loss at expiry of a long call, put, short option, or vertical spread under predeclared underlying-price scenarios?

This is an **expiry payoff exercise**, not an option valuation, probability forecast, strategy recommendation, or execution system. All strikes, premiums and scenarios are hypothetical. No broker connection or market data.

## Mathematics

For terminal underlying price `S_T >= 0`, strike `K > 0`, and premium `p >= 0` paid per underlying unit:

- Long call net expiry P&L: `max(S_T-K,0)-p`.
- Long put net expiry P&L: `max(K-S_T,0)-p`.
- A short leg has negative quantity; its P&L is the negative of the equivalent long leg.
- Multi-leg net P&L is the sum of each signed quantity times its intrinsic payoff less premium.

A 100/110 call debit spread with long-call premium 7 and short-call premium 3 costs 4, has maximum expiry loss 4 and maximum expiry profit 6 **per underlying unit**, assuming both contracts share the same expiry and deliverable. This ignores contract multipliers, commissions, funding, margin and settlement.

## Reproduce

Requires Python 3.11+ and **standard library only** for implementation and tests:

```bash
cd quant-projects/16-option-payoff-stress
python option_payoff.py --strike 100 --premium 6
python -m unittest -v test_option_payoff.py
python -m compileall -q option_payoff.py test_option_payoff.py
```

The command prints seven fixed synthetic terminal-price scenarios. No random seed or external data is needed.

## Model validation and guardrails

Tests check analytical break-even, call/put intrinsic values, short-leg sign, capped vertical-spread payoff, additivity, scenario outputs, invalid inputs and input immutability. Inputs must be finite, with nonnegative terminal spot and premium, positive strike, nonzero bounded quantities, at most 20 legs and 1001 scenarios. No assumptions about future prices are inferred from the scenarios.

**Limits:** European-style expiry only. Does not model mark-to-market values before expiry, implied volatility, Black–Scholes, exercise/assignment, American options, dividends, taxes, contract multipliers, slippage, fees, margin, borrow, liquidity or counterparty risk. Short options may have large or unbounded losses. Synthetic unit tests cannot establish market accuracy or production readiness.

**Acceptance:** Run tests on exact published GitHub revision and verify CI separately. Independent model review, real-market inputs, pricing calibration and production certification remain unverified.

**Next:** Add an independently tested European Black–Scholes benchmark with clearly stated continuous-rate/dividend assumptions, put-call parity and finite-difference Greeks; retain expiry P&L as a separate concept.
