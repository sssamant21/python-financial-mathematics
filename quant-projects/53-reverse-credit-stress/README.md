# Project 53 — Reverse credit stress testing (synthetic)

**Business question:** How severe would a common increase in borrower default probabilities need to be for a fixed portfolio's *expected credit loss* to reach a predeclared risk budget?

This is **reverse stress testing**, not a prediction: specify the adverse outcome first, then find the smallest stress multiplier that reaches it. Unlike Project 18's forward credit concentration and Project 52's transition-parameter uncertainty, this lab solves a **threshold-inversion** problem with capped probabilities.

## Mathematics

For borrower i, exposure at default EAD_i, probability of default PD_i, and loss given default LGD_i, define:

`EL(m) = sum_i EAD_i * min(1, m * PD_i) * LGD_i`.

The common stress multiplier `m >= 1` is fixed across borrowers. Bisection locates the smallest `m` in a **predeclared bounded interval** such that `EL(m) >= budget`. If the upper bound cannot reach the budget, report **unreachable**, never silently extrapolate. A baseline already above the budget returns `m=1`. This monotone deterministic calculation does **not** model default dependence, loss quantiles, exposure changes, liquidity, dynamic recoveries, or macroeconomic transmission.

## Reproduce

Python 3.11+; **standard library only**. No third-party downloads or market data.

```bash
cd quant-projects/53-reverse-credit-stress
python -m unittest -v test_reverse_stress.py
python -m py_compile reverse_stress.py test_reverse_stress.py
python reverse_stress.py --budget 25 --max-multiplier 20
```

The example uses invented EAD/PD/LGD observations. The JSON reports baseline loss, maximum loss within the bounded search, the budget, and either a breach multiplier or `null`. Interpret the multiplier only as a *model sensitivity*; it is not a plausible macro scenario without separate calibration.

## Guardrails and validation

Require 1–10,000 aligned borrowers; finite nonnegative EAD, PD and LGD; PD/LGD <= 1; positive finite budget and multiplier; 1–200 bisection iterations; reject booleans and overflow. The portfolio and threshold are predeclared: no optimization or selection on observed outcomes. Tests cover exact arithmetic, saturation, monotonicity, threshold identity, unreachable cases and invalid inputs.

**Validation status:** synthetic tests authored; exact published-revision CI and independent model review are unverified until checked. No historical market data, real-world calibration, regulatory capital validation, production certification, financial advice or broker connection. Future extension: borrower-specific stresses, concentration contributions and independent analytical piecewise-linear threshold checks.
