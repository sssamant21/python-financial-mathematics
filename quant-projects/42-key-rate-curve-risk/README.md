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
