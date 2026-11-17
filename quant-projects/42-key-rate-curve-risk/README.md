# Project 42 — Key-rate PV01 and curve-shape risk

**Question:** How much does a hypothetical bond's present value change if only one maturity's zero rate moves? A single parallel-duration number hides maturity concentration. This lab reports a sensitivity bucket at each cash-flow maturity and reconciles their sum with a parallel curve bump.

## Business and mathematical context

For fixed future cash flows `C_i`, year fractions `t_i`, and continuously compounded zero rates `z_i`, the simplified present value is

`PV = sum_i C_i exp(-z_i t_i)`.

For a **one-basis-point** (0.0001) symmetric bump of the *individual* rate at tenor `i`:

`PV01_i = [PV(z_i - 0.0001) - PV(z_i + 0.0001)] / 2`.

The sign convention makes a positive PV01 correspond to a loss of value for a rate increase when cash flows are positive. Summing the buckets equals the parallel PV01 **for this separable cash-flow-at-node model**. The sum identity does not generally hold under interpolated market curves, curve recalibration or nonlinear multi-instrument models. This is a present-value sensitivity in currency units per one-basis-point bump, not a hedge recommendation.

## Reproduce (Python 3.11–3.13, standard library only)

```bash
cd quant-projects/42-key-rate-curve-risk
python -m unittest -v test_key_rate.py
python -m compileall -q key_rate.py test_key_rate.py
python key_rate.py
python key_rate.py --bump-bp 0.5
```

The default five-year synthetic fixed-coupon cash-flow example uses year-end payments of 3, 3, 3, 3 and 103 units and zero rates of 2.5%, 2.8%, 3%, 3.2% and 3.4%. No market quotes or external data are bundled. Nine deterministic tests cover closed-form valuation, finite-difference identity, sign, invalid inputs, and nonmutation.

## Guardrails and model validation

Tenors must be strictly increasing and positive; inputs finite, rates within an intentionally broad +/-100% educational bound, and bump in (0, 100] basis points. Negative cash flows and negative rates are allowed. The implementation rejects nonfinite PV. For any market exercise, document quote provider, license, as-of timestamp, day count, calendar, instrument mapping, and curve calibration; use observations known at valuation time only.

**Limitations:** No bootstrapped curve integration, interpolation, compounding conventions beyond continuous, settlement, accrued interest, convexity hedging, instrument-specific repricing, bid/ask, or independent market validation. Synthetic fixture tests are not production certification or financial advice. Exact published-revision CI and independent mathematical review remain unverified at initial publication.

**Next:** test off-grid cash flows with explicitly documented interpolation and compare finite differences against analytic derivatives, without implying a tradable hedge.

## Off-grid interpolation and analytical gradients (extension)

Run `python -m unittest -v test_key_rate.py test_offgrid.py`, `python -m compileall -q key_rate.py offgrid.py test_key_rate.py test_offgrid.py`, and `python offgrid.py` from this folder (Python 3.11–3.13; standard library only).

The new `offgrid.py` example uses synthetic curve nodes at 1, 3 and 5 years and payments at 1.5, 2.5 and 4 years. Between nodes `t_L <= t <= t_R`, linearly interpolate the **continuously compounded zero rate**: `z(t) = w_L z_L + w_R z_R`, with `w_R=(t-t_L)/(t_R-t_L)` and `w_L=1-w_R`. Discount a cash flow `C` as `C exp(-t z(t))`. The exact node gradient is `dPV/dz_j = -sum_i t_i w_ij C_i exp(-t_i z(t_i))`; approximate the node PV01 as `-0.0001*dPV/dz_j` and cross-check against central differences. Each cash-flow interpolation weight sums to one, so the **exact gradients** add to the parallel-rate gradient. Finite-difference PV01 bucket sums are generally only approximately equal to a parallel PV01 for off-grid multi-node cash flows: nonlinear cross terms remain.

**Risk boundaries:** No extrapolation outside the first/last curve node, no market-data fetch, no curve fitting, no historical claims, no live execution. The interpolation choice is a modeling assumption; it does not preserve an arbitrage-free forward curve automatically. Tests use only synthetic deterministic fixtures. New extension runtime/CI and independent model review must be verified separately.
