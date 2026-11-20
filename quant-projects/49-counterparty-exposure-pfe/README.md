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

## Analytical benchmark and uncertainty extension (2026-11-19)

Run `python -m unittest -v test_exposure.py test_diagnostics.py` and `python -m py_compile exposure.py diagnostics.py test_exposure.py test_diagnostics.py` from this directory. Standard library only; no market data download.

For the stylized model, `V_t = N σ sqrt(t) Z`, with `s = N σ sqrt(t)`, the analytical expected positive exposure after threshold `H` is `EPE(t) = s φ(H/s) - H Φ(-H/s)` for `s > 0`, and zero when `s = 0`. The population PFE at quantile `q` is `max(s Φ⁻¹(q) - H, 0)`. Compare these to the simulated `epe` and `pfe95` in `exposure.py`; sample quantiles fluctuate, and the quantile interpolation convention is not identical to the population definition at finite path counts.

`diagnostics.epe_standard_error(exposures)` estimates the IID-path standard error of **mean exposure at one year**, not uncertainty in PFE or aggregate CVA. Cross-year exposures on the same paths are dependent, so do not combine yearwise standard errors as if independent. The benchmarks do not validate real derivative pricing, collateral mechanics, default dependence, or market calibration.

**Evidence:** Six new deterministic analytical test methods passed locally on authored source; Python compilation passed. Existing eight tests and exact published-revision CI were not executed in that local run. Independent model review remains pending.

## Multi-seed Monte Carlo convergence (2026-11-19)

Run from this directory (Python 3.11+, standard library only):

```bash
python -m unittest -v test_exposure.py test_diagnostics.py test_convergence.py
python -m py_compile exposure.py diagnostics.py convergence.py test_convergence.py
python convergence.py --paths 200 800 3200 --seeds 11 23 37 49 71
```

For each path count, independent random seeds generate estimates of EPE at a fixed year. The report compares their average with the analytical Brownian EPE, records absolute benchmark error, and estimates the **between-seed standard error of the average** as sample standard deviation of the independent run estimates divided by the square root of the number of seeds. This is not a PFE confidence interval, a CVA uncertainty bound, or a guarantee of monotonic error reduction as path count grows. Larger path counts should reduce sampling variability *on average*, but an individual realized absolute error can increase. All seeds and path budgets are explicitly bounded; fixtures are synthetic and no market data is redistributed.

The new regression tests check deterministic repeatability, zero-volatility limits, benchmark threshold sensitivity, error arithmetic, invalid seeds/path counts/economic inputs, and the simulation budget. **Exact published-revision CI and independent model review remain unverified until a workflow completes.** This extension assumes independent exposure and default; wrong-way-risk scenarios require a separate explicitly qualified model.
