# Project 49 — Counterparty Exposure, PFE and Simplified CVA

**Goal.** Learn why a derivative with zero initial mark-to-market can still create future counterparty credit exposure. This lab simulates a *stylized* zero-mean Brownian mark-to-market process, computes expected positive exposure (EPE), 95% potential future exposure (PFE), and a simplified unilateral credit valuation adjustment (CVA). It is **not** a derivative pricing engine, regulatory exposure model, or financial advice.

## Mathematics and business interpretation

At year `t`, simulated mark-to-market is `V_t = V_(t-1) + N σ Z_t`, with independent standard-normal `Z_t` and annual time steps. Positive exposure after a fixed collateral threshold `H` is `E_t = max(V_t - H, 0)`. EPE is the sample mean of `E_t`; PFE95 is its empirical 95th percentile. EPE measures average exposure; PFE summarizes a high-exposure tail and **is not a maximum loss**.

With a constant illustrative hazard rate `λ`, first-default mass in year `t` is `exp(-λ(t-1)) - exp(-λt)`. Under **independent exposure and default**, year-end discounted unilateral CVA is `LGD × Σ_t exp(-rt) × EPE_t × default_mass_t`. This simplified expression ignores wrong-way risk, netting sets, margin periods, collateral dynamics, funding, discount-curve calibration, and bilateral adjustments.

## Reproduce (Python 3.11+; standard library only)

From this directory:

```bash
python exposure.py --paths 10000 --seed 49 --threshold 0
python -m unittest -v test_exposure.py
python -m py_compile exposure.py test_exposure.py
```

Output columns: `year,epe,pfe95,default_mass,incremental_cva`; a final line reports total CVA. Repeat with `--threshold 100000` to explore collateral sensitivity. Default scenarios are **synthetic** and use no third-party market data. The random seed makes paths reproducible; Monte Carlo error remains. Input limits cap path counts and years to avoid accidental heavy runs.

## Model validation and limits

Tests cover deterministic reproducibility, nonnegative exposure, zero-volatility and zero-default limiting cases, monotonic threshold effects on matched paths, hazard-mass accounting, quantile interpolation and invalid inputs. Additional research should compare EPE with analytical Brownian positive-part expectations, quantify Monte Carlo standard errors and seeds, introduce exposure/default dependence, and independently review financial conventions. No historical market calibration, CI pass for this publication, independent validation, or production certification is claimed.
