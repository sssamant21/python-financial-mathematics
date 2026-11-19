# Project 48 — Credit rating migration and default stress

**Business question:** How do rating upgrades, downgrades, and default probabilities compound over multiple years, and how does a hypothetical deterioration in transition rates affect expected credit losses?

## Model and mathematics

This beginner-friendly, dependency-free Markov-chain lab has four illustrative states: A (stronger), B, C (weaker), and D (default). Each row of a one-year transition matrix gives probabilities of moving from the current rating to each next rating; rows sum to one. Default is **absorbing**: once D, always D. With an initial one-hot row vector `v_0`, the year-`t` distribution is `v_t = v_0 P^t`. Cumulative default probability is the D component; for a hypothetical constant loss-given-default `LGD`, cumulative expected loss per initial notional is `PD_t × LGD`. This is a cumulative loss measure, **not annualized loss or a discounted present value**.

The built-in `BASE` and `STRESS` matrices are **invented** for education. They are not observations from 2020/2022 or calibrated to any ratings agency, security, or borrower population. For the illustrative initial B rating and three-year horizon, the baseline default probability is approximately 10.6370%, compared with 31.4658% under the hypothetical stress matrix. These are arithmetic outputs from assumptions, not forecasts.

## Reproduce

Python 3.11–3.13 standard library only (no pip dependencies):

```bash
cd quant-projects/48-credit-rating-migration
python migration.py
python -m unittest -v test_migration.py
python -m compileall -q migration.py test_migration.py
```

The nine deterministic tests check row-to-one-year identity, probability conservation, default absorption, monotone cumulative default, expected-loss accounting, stress comparison, and input rejection. Inputs are capped at 50 years and four states; invalid probabilities, non-stochastic matrices, boolean numeric values, and nonabsorbing default rows are rejected.

## Model validation and limitations

A homogeneous, time-invariant transition matrix assumes the Markov property and constant transition rates within each scenario. It ignores rating-history dependence, correlated obligor migrations, exposure amortization, time-varying LGD, competing risks, rating withdrawals, cohort composition, and discounting. Multiplying cumulative PD by constant LGD is an elementary teaching approximation, not tranche valuation. A stress matrix is not a confidence interval. A future empirical extension requires licensed, point-in-time cohort transitions, documented observation and publication dates, treatment of withdrawals, out-of-sample calibration, and survivorship-bias controls. Never redistribute third-party raw data.

**Validation:** Nine tests passed on a locally constructed copy of the authored source on 2026-11-19; compilation and synthetic CLI smoke also passed. Exact published-revision CI, independent mathematical review, empirical calibration, and production certification remain **unverified**. No trading or broker connectivity.

## Time-varying migration stress extension (2026-11-19)

Run `python time_varying.py` and `python -m unittest -v test_migration.py test_time_varying.py`. Python 3.11–3.13 standard library only. The annual sequence `(BASE, STRESS, BASE)` applies a temporary second-year shock, while `(STRESS, STRESS, STRESS)` models persistent deterioration. With row-vector probabilities, `v_t = v_(t-1) P_t`; matrix multiplication order matters. The unconditional default mass in year t is `v_t[D] - v_(t-1)[D]`, and the sum reconciles to cumulative PD for a nondefault initial rating. For an initially defaulted obligor, incremental default mass is zero, although the cumulative default-state probability remains one. With fixed LGD, cumulative EL/notional is the sum of annual new-default masses times LGD; no discounting or exposure amortization is modeled.

Synthetic B-rated three-year illustrations: baseline PD 10.6370%; second-year-only stress PD 17.4819%; persistent stress PD 31.4658%. These figures are *not* historical 2020/2022 observations, forecasts, or calibration. Seven extension tests passed locally using a source-equivalent baseline shim; compilation and synthetic CLI smoke passed. The **exact published integration and hosted CI remain unverified**. Validate against licensed point-in-time rating cohorts, handle withdrawals and survivorship, and obtain independent review before operational use.

## Discounted timing of default losses (2026-11-19)

A default in year 1 and a default in year 3 have the same *undiscounted* LGD but different present values. This synthetic extension applies a fixed effective annual discount rate `r` to year-end losses: `PV(EL)/initial notional = sum_t [new_default_mass_t × LGD / (1+r)^t]`. This assumes losses occur at each year-end; it does not model recovery delays, changes in exposure, risk-neutral valuation, term structures, credit spreads, or calibration. Discounting expected losses is **not** a tradable security price.

Run from this directory:

```bash
python discounted_loss.py
python -m unittest -v test_migration.py test_time_varying.py test_discounted_loss.py
python -m compileall -q migration.py time_varying.py discounted_loss.py test_discounted_loss.py
```

For illustrative initial B, 3 years, LGD 60%, and a hypothetical 4% annual discount rate, baseline undiscounted EL/notional is 6.3822% versus discounted 5.8820%; a second-year shock yields 10.4891% versus 9.6711%, and persistent stress 18.8795% versus 17.4130%. These are **synthetic arithmetic**, not empirical estimates. Eight new deterministic tests passed locally against a source-equivalent copy of the two existing modules; Python compilation and CLI smoke passed. Exact published-revision integration, hosted CI, independent review and market calibration remain unverified. Guardrails reject negative/nonfinite/out-of-range rates or LGD, and initially defaulted exposures, which require separate treatment.
