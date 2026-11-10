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
