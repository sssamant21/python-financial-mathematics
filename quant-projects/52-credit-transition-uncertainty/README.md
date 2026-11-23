# Project 52 — Credit rating transition uncertainty (Dirichlet–multinomial)

**Question:** How uncertain is an estimated one-year rating-to-default probability when transition counts are sparse?

A transition row records counts of borrowers moving from one starting rating to several ending ratings. A point estimate alone can hide considerable sampling uncertainty. This lab uses a **Dirichlet prior** and **multinomial observations** to produce a posterior distribution for a *single* row, then samples its default-column marginal using a Beta distribution (via independent Gamma draws).

## Mathematics and business context

For counts `n_j` and predeclared prior concentrations `alpha_j > 0`, the posterior is `Dirichlet(alpha_j + n_j)`. The marginal probability of default for column `d` is `Beta(alpha_d+n_d, sum_{j != d}(alpha_j+n_j))`; its posterior mean is `(alpha_d+n_d) / sum_j(alpha_j+n_j)`. The equal-tailed interval is an **approximate posterior credible interval** based on seeded simulation, *not* a frequentist confidence interval or proof of calibrated coverage.

The starting rating, observation horizon, borrower cohort, default definition and transition-count provenance must be fixed before using real observations. The sample counts below are **invented**, not observations of any issuer. This is different from Project 48's deterministic rating-migration exercise and Project 51's conditional independent-default loss calculations: it measures **parameter uncertainty**, not correlated defaults or economic capital.

## Reproduce

Python 3.11+; **standard library only**, no downloaded data or third-party dependencies.

```bash
cd quant-projects/52-credit-transition-uncertainty
python -m unittest -v test_transition_uncertainty.py
python -m py_compile transition_uncertainty.py test_transition_uncertainty.py
python transition_uncertainty.py --counts 920 65 15 --prior 1 1 1 --default-index 2 --draws 4000 --seed 42
```

The CLI prints JSON including the posterior mean, simulated 95% interval, posterior concentrations, seed and number of observations. A zero-observation row yields the prior distribution. Compare predeclared alternative prior strengths to understand sensitivity; do **not** tune priors after inspecting held-out outcomes.

## Guardrails and validation boundaries

Inputs require 2–20 states, nonnegative integer counts, strictly positive finite prior concentrations, valid default column, bounded draws (100–100,000) and seed. Simulation is reproducible for the same Python environment and seed. The model assumes exchangeable independent observations conditional on a fixed transition row; cohort selection, rating withdrawals, censored observations, time variation, clustering, migration dependence, historical regime shifts and survivorship bias are **not modeled**. The default state is identified by an explicit column index; no absorbing-row constraint is inferred or enforced.

Seven deterministic synthetic unit tests are authored for conjugacy, mean identity, reproducibility, interval ordering, prior-only data and malformed inputs. **Exact published-revision runtime/CI is unverified until executed.** No historical calibration, independent model validation, production certification, financial advice or trading integration.
