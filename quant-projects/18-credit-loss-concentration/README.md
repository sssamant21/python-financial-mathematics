# Project 18 — Credit Portfolio Expected Loss and Concentration Stress

**Business question:** How much one-year credit loss is expected under explicitly hypothetical default assumptions, and how concentrated is the exposure book? This is a simple **credit-risk** lab, not a market VaR model or a regulatory capital calculator.

## Mathematics

For borrower *i*, expected loss is `EL_i = EAD_i × PD_i × LGD_i`, where exposure at default (EAD) is in currency units, probability of default (PD) is a one-year probability, and loss given default (LGD) is the fraction lost conditional on default. Portfolio EL is the sum of individual ELs. EAD concentration is measured by `HHI = Σ(EAD_i / total_EAD)^2`, between `1/n` (equal exposures) and `1` (single borrower). The largest EAD share is also reported.

The predefined stress multiplies PD and adds an absolute LGD increment, each capped at 100%. It does **not** estimate the probability of the stress, joint defaults, unexpected loss, or economic capital. No external data or broker connectivity.

## Reproduce

Python 3.11+ standard library; no package installation needed.

```bash
cd quant-projects/18-credit-loss-concentration
python credit_risk.py
python -m unittest -v test_credit_risk.py
```

Expected demonstration values: base EAD 1,750,000 and EL 21,000; stressed EL 50,000. All inputs are synthetic, not calibrated to observed obligors. The CLI uses no random seeds or downloaded data.

## Guardrails and validation

Reject duplicate/empty borrower names, empty portfolios, zero aggregate exposure, negative EAD, invalid PD/LGD, nonfinite numeric values, and negative/nonfinite stress inputs. Tests cover numerical identities, stress caps, invalid inputs and input immutability. In real credit modeling, PD/LGD/EAD need point-in-time vintage data, default definitions, exposure changes, recovery timing, correlation and concentration-tail models; none is validated here. **Synthetic tests do not establish calibration, independent model validation, regulatory compliance or production readiness.** Educational only, not financial advice.

## Correlated-default tail simulation (extension)

`correlated_defaults.py` uses a **seeded, synthetic one-factor Gaussian latent-variable model**. Each borrower defaults when `sqrt(rho) * Z + sqrt(1-rho) * epsilon_i < Phi^{-1}(PD_i)`, with one shared standard-normal systematic shock `Z` and independent standard-normal borrower shocks `epsilon_i`. Here `rho` is latent **asset** correlation, not observed default correlation. Marginal PDs remain the input PDs in the model. Loss severity is fixed at `EAD × LGD`; there is no stochastic recovery, exposure migration or multi-period dependence.

```bash
cd quant-projects/18-credit-loss-concentration
python correlated_defaults.py
python -m unittest -v test_credit_risk.py test_correlated_defaults.py
```

The deterministic CLI uses 10,000 scenarios, seed 42, and a hypothetical 20% latent asset correlation. It reports analytical expected loss, simulated mean loss, empirical 99% loss VaR (nearest-rank), mean of the highest 1% simulated losses (tail-average proxy), and `VaR - analytical EL` as an **illustrative unexpected-loss measure**. This tail-average is not a calibrated regulatory expected shortfall. Finite-sample Monte Carlo noise and discrete losses can produce jumps; increase scenarios and compare seeds before interpreting tails. The simulation does **not** represent observed 2020/2022 default episodes or calibrated economic capital. No third-party data is distributed.

## Asset-correlation and repeated-seed sensitivity (2026-11-10)

The additional `correlation_sensitivity.py` fixes the same hypothetical borrower book, PDs and LGDs, then varies **latent asset correlation** (`rho = 0, 0.2, 0.5`) while repeating simulations with predeclared seeds. This tests whether loss-tail estimates change with common-factor dependence and how much they vary with finite Monte Carlo sampling. Analytical `EL = sum(EAD × PD × LGD)` is independent of rho, whereas loss VaR and tail averages can shift. The tail metrics need **not** rise monotonically for small discrete portfolios or finite simulation samples.

```bash
cd quant-projects/18-credit-loss-concentration
python correlation_sensitivity.py
python -m unittest -v test_credit_risk.py test_correlated_defaults.py test_correlation_sensitivity.py
```

Python 3.11+ standard library only. Each row reports average simulated loss, 99% loss VaR and tail average across seeds, together with **sample standard deviations across seed runs** (reported as `None` for one seed). These are *descriptive Monte Carlo stability diagnostics*, **not** statistical confidence intervals, real-world loss forecasts, independent scenarios, or regulatory capital. The same seed values are reused across rho settings for paired comparisons. Predeclared parameter grids, finite inputs, unique seeds and a two-million-scenario total budget guard against accidental runaway jobs. Tests use small synthetic books. No external data, broker or live trading actions.

**Limitations:** Three obligors produce a very discrete tail distribution; nearest-rank VaR may jump. The model assumes a single Gaussian factor, constant marginal PDs, fixed LGD and EAD, and no parameter uncertainty. A larger simulated mean at one rho is sampling noise, not evidence that rho changes analytical expected loss. No observed 2020/2022 default calibration, independent model validation or production certification is claimed. Borrower-level tail attribution is a separate future milestone.

## Borrower-level scenario-tail attribution (2026-11-10)

The seeded `tail_attribution.py` reconstructs the one-factor synthetic default model and retains each borrower's loss per scenario. Sort scenario losses descending and select the highest `k = N - ceil(q*N) + 1` scenarios. For borrower `i`, the tail contribution is the **average borrower loss in those same selected scenarios**. By construction, `sum_i contribution_i = average selected portfolio loss` (up to floating-point rounding). Equal-loss ties are broken by original scenario index; this is a **top-k scenario-tail average**, not a unique allocation of VaR or an Euler regulatory-capital contribution.

```bash
cd quant-projects/18-credit-loss-concentration
python tail_attribution.py
python -m unittest -v test_tail_attribution.py
```

`concentration_comparison` transfers part of the largest EAD to the smallest EAD, holding aggregate EAD and each borrower's PD/LGD assumptions fixed. It uses paired random seeds for descriptive sensitivity, not independent model validation. **Analytical expected loss may change** because EAD is moved between borrowers with different PD/LGD; lower HHI does not guarantee lower tail loss. The simulator caps scenario count and total borrower-scenario work, rejects nonfinite parameters, and uses no downloaded market data. Python 3.11+ standard library only.

**Evidence:** 13/13 local tests, Python compilation and synthetic CLI smoke passed using a locally reconstructed `credit_risk` helper; complete published-revision CI remains unverified until GitHub Actions runs. No historical default/recovery calibration, independent model validation, regulatory capital approval or production certification.
