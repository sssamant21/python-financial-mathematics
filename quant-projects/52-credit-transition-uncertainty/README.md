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

## Prior-strength and held-out sensitivity (incremental extension)

The companion `test_prior_sensitivity.py` defines a **predeclared** prior-strength grid and a held-out Bernoulli negative log-likelihood scoring helper. The training transition counts are used to estimate the posterior mean; the separately supplied held-out event count is used **only for scoring**, never to choose the prior after the fact. A smaller held-out log score is better, but one synthetic cohort is not evidence of calibrated real-world prediction.

For prior multiplier `k > 0`, the posterior is `Dirichlet(k * alpha_j + n_j)`. A larger `k` puts more weight on the assumed prior; it does not automatically improve prediction. The held-out score is `-[d log(p) + (N-d) log(1-p)]/N` for `0 < p < 1`. Keep the cohort definition and time split fixed and report *all* predeclared settings rather than selecting the best on the test set.

```bash
python -m unittest -v test_transition_uncertainty.py test_prior_sensitivity.py
python -m py_compile transition_uncertainty.py test_transition_uncertainty.py test_prior_sensitivity.py
```

The five new tests cover deterministic grid agreement, directional prior sensitivity, invalid grid rejection, proper held-out log-score ordering and invalid scoring inputs. **These tests are authored but not yet verified on the published revision.** The helper currently lives in the test module as a teaching scaffold, not a separate CLI or a full walk-forward calibration study. Market-data validation and independent review remain pending.


## Seeded train/held-out cohort calibration exercise (2026-11-23)

`cohort_calibration.py` simulates a **two-state** (survival/default) cohort using a predeclared true default probability and a local seeded RNG. It fits the posterior mean using training counts **only**, freezes the forecast, then scores an independent held-out cohort with mean Bernoulli log loss, Brier score, and signed calibration gap (predicted minus observed default rate). No external market data or third-party dependencies are used. A single held-out cohort cannot establish calibration, uncertainty coverage, or performance across market regimes.

```bash
python -m unittest -v test_transition_uncertainty.py test_prior_sensitivity.py test_cohort_calibration.py
python -m py_compile transition_uncertainty.py cohort_calibration.py test_cohort_calibration.py
python cohort_calibration.py --true-pd 0.04 --train-size 500 --heldout-size 200 --seed 42
```

Five new synthetic tests check reproducibility, training-only posterior identity, independence of fitted parameters from held-out cohort size, independent score reconciliation, and invalid-input rejection. **Authored, not executed or verified in CI in this checkpoint.** This extension is not a real historical backtest. Next: execute all 17 tests on the published revision, add repeated-cohort calibration summaries and verify CI coverage.


## Repeated-cohort calibration diagnostics (2026-11-23)

`repeated_cohorts.py` repeats the **predeclared** two-state synthetic train/held-out experiment with consecutive independent RNG seeds. It reports every run (no best-seed selection) and the mean, minimum and maximum of posterior PD, held-out default rate, signed calibration gap, log loss and Brier score. Mean absolute and root-mean-squared calibration gaps describe the dispersion of observed held-out errors; **they are not confidence intervals or demonstrated predictive coverage**. Each run refits on training observations only, never held-out outcomes.

```bash
cd quant-projects/52-credit-transition-uncertainty
python -m unittest -v test_transition_uncertainty.py test_prior_sensitivity.py test_cohort_calibration.py test_repeated_cohorts.py
python -m py_compile cohort_calibration.py repeated_cohorts.py test_repeated_cohorts.py
python repeated_cohorts.py --true-pd 0.04 --train-size 500 --heldout-size 200 --first-seed 42 --repetitions 20
```

The number of repetitions is bounded to 2–200 and each cohort to 1–100,000 observations; seed overflow, booleans and invalid model parameters are rejected. The five new tests check deterministic output, individual-run agreement, aggregate arithmetic and invalid inputs. **These tests were authored but exact-revision execution and CI inclusion remain unverified.** All cohorts are synthetic; no historical transition calibration, model approval, or investment decision is supported.


## Paired prior-strength stability (2026-11-23)

`prior_stability.py` evaluates a **predeclared** symmetric Beta-prior strength grid against identical seeded training and held-out synthetic cohorts. For each seed, training and held-out default counts are the same across prior strengths (paired comparison); only the prior changes. The posterior forecast is frozen before held-out scoring. All rows are retained, with per-strength mean log loss, Brier score and absolute calibration gap. No winning prior is selected using held-out outcomes.

```bash
cd quant-projects/52-credit-transition-uncertainty
python -m unittest -v test_prior_stability.py
python -m py_compile prior_stability.py test_prior_stability.py
python prior_stability.py --true-pd 0.04 --train-size 500 --heldout-size 200 --first-seed 42 --repetitions 10 --strengths 0.5 1 5
```

The simulation has a bounded work budget, 2–100 repetitions, 1–8 distinct finite prior strengths and 32-bit seed checks. These **five new tests are authored, not yet verified** against the published revision. Paired simulation reduces random comparison noise but does not establish historical stability, predictive coverage, independent review, or production suitability.
