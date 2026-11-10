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

## Extension — Black–Scholes–Merton European valuation (synthetic only)

**Business question:** What is the *theoretical present value* of a European call or put before expiry, assuming a constant annual volatility, continuously compounded risk-free rate and continuous dividend yield? This differs from the expiry-only net P&L above: the option value is not a forecast of realized profit or an executable quote.

Under lognormal diffusion with no arbitrage, constant `r`, `q`, `sigma > 0` and time to expiry `T > 0` in years:

```text
d1 = [ln(S/K) + (r - q + sigma²/2)T] / (sigma sqrt(T))
d2 = d1 - sigma sqrt(T)
Call = S exp(-qT) N(d1) - K exp(-rT) N(d2)
Put  = K exp(-rT) N(-d2) - S exp(-qT) N(-d1)
Call - Put = S exp(-qT) - K exp(-rT)
```

`N` is the standard-normal CDF. `black_scholes.py` uses only Python's standard library. Central finite differences approximate delta (value change per one underlying-price unit), gamma (second spot derivative), and vega (per **1.0** volatility change, not per 1 percentage point). The numerical step sizes are fixed defaults and may be unstable for extreme strikes, tiny maturities or very small volatility.

```bash
cd quant-projects/16-option-payoff-stress
python black_scholes.py --spot 100 --strike 100 --years 1 --rate 0.05 --volatility 0.2
python -m unittest -v test_option_payoff.py test_black_scholes.py
python -m compileall -q option_payoff.py black_scholes.py test_option_payoff.py test_black_scholes.py
```

A canonical zero-dividend hypothetical benchmark gives call approximately **10.450584**, put approximately **5.573526**, and near-zero parity residual. Tests cover that benchmark, dividend-adjusted parity, arbitrage bounds, monotonicity, finite-difference Greeks versus analytical values, deterministic results, and invalid inputs. **Nine extension tests passed locally on authored source**; exact published-revision CI remains unverified until GitHub Actions confirms it.

**Model risk:** Constant volatility/rates/dividend yield, frictionless markets, continuous hedging, European exercise, and lognormal diffusion are simplifying assumptions. No calibration to real quotes, stochastic volatility, jumps, discrete dividends, American exercise, funding, margin, liquidity, contract multiplier, transaction costs or broker execution. Inputs are hypothetical; independent model review and production readiness remain unverified.

**Next:** Verify exact-revision CI and add bounded volatility/maturity sensitivity with independent numerical checks before Project 17.

## Extension — volatility and maturity sensitivity (2026-11-09)

**Business question:** How sensitive is the *theoretical* European option value to predeclared volatility and remaining-maturity assumptions? This is not implied-volatility calibration or a forecast.

The Black–Scholes value is evaluated on a fixed 3 × 3 grid: annual volatility 10%, 20%, 40%; maturity 0.25, 1, 2 years; default spot/strike 100, continuously compounded rate 5%, dividend yield 0. Volatility sensitivity is positive for calls and puts under these assumptions. Maturity monotonicity is **not universal** (notably for puts, dividends and negative rates); the regression check restricts its positive-time-value example to an at-the-money, zero-dividend call with positive rate.

```bash
cd quant-projects/16-option-payoff-stress
python sensitivity.py --kind call
python sensitivity.py --kind put
python -m unittest -v test_option_payoff.py test_black_scholes.py test_sensitivity.py
python -m compileall -q sensitivity.py test_sensitivity.py
```

The new grid uses the existing pricing function, verifies put-call parity at every point, and rejects nonfinite/invalid grid inputs and grids larger than 100 points. The deep-out-of-money short-maturity test checks finite, nonnegative values but **does not certify numerical accuracy** in extreme tails. The module uses the standard library only. No market data, quotes, or broker integration.

**Evidence:** Nine extension tests passed in an isolated source-equivalent environment with a locally reconstructed pricing core; compilation and CLI smoke passed. Exact published-revision integration and the updated GitHub Actions run remain unverified until confirmed. No independent review, historical calibration, or production certification.

**Next:** Confirm exact-revision CI and investigate near-expiry/low-volatility finite-difference stability before beginning a distinct Project 17.

## Extension — near-expiry and low-volatility numerical stability (2026-11-10)

**Business question:** Can finite-difference delta, gamma and vega become numerically unreliable when expiry is close or volatility is very low? We compare the existing central-difference implementation to independent closed-form Black–Scholes–Merton derivatives on a **predeclared synthetic** grid (one year at 20% volatility, one day at 20%, and one day at 1%). No market data or model fitting.

Analytical Greeks with continuous dividend yield `q`, standard normal density `phi`, and `d1` defined above:

```text
Call delta = exp(-qT) N(d1)
Put delta  = exp(-qT) (N(d1)-1)
Gamma      = exp(-qT) phi(d1)/(S sigma sqrt(T))
Vega       = S exp(-qT) phi(d1) sqrt(T)
```

Vega is **per 1.0 volatility change**, not per percentage point. Central differences use `spot_step = 0.0001 * spot` and `vol_step = 0.001 * volatility`. The diagnostic reports absolute error for each Greek and a descriptive pass flag using `abs(error) <= 1e-4 + 0.01*abs(analytic)`. This threshold is an **illustrative numerical check**, not a market calibration or certified accuracy limit. Near expiry the Greeks can become sharply peaked or discontinuous in the limiting case, so finite differences can be step-sensitive.

```bash
cd quant-projects/16-option-payoff-stress
python stability_diagnostics.py --kind call
python stability_diagnostics.py --kind put
python -m unittest -v test_stability_diagnostics.py
python -m unittest -v test_option_payoff.py test_black_scholes.py test_sensitivity.py test_stability_diagnostics.py
python -m compileall -q stability_diagnostics.py test_stability_diagnostics.py
```

Guardrails reject invalid or nonfinite scenarios, excessive scenario counts and invalid step scales. Tests cover independent analytical benchmarks, call/put derivative identities, finite outputs in near-expiry/low-volatility cases, determinism and invalid inputs. **Execution evidence is pending:** tests were authored and published, but this run could not clone the exact repository revision because the GitHub hostname did not resolve from the local runtime. The dedicated CI workflow now includes the tests; its result must be verified separately. Independent review, real-market calibration and production certification remain unverified.

**Next:** Confirm exact-revision CI and review numerical tolerance behavior; then begin Project 17 as a distinct quantitative-finance exercise.
