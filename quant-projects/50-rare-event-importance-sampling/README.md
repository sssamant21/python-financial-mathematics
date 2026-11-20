# Project 50 — Rare-Event Credit Loss and Importance Sampling

**Goal:** Understand why ordinary Monte Carlo can miss rare portfolio credit-loss events, and how importance sampling can estimate their probabilities more efficiently. This is an educational synthetic model, not a credit capital engine or investment recommendation.

## Business and mathematical context

Imagine **n independent, identical** one-year borrowers, each defaulting with probability **p**, with one unit of loss per default. The total default count K follows Binomial(n,p). The stress event is K >= threshold; its exact probability is the sum of binomial masses from threshold through n.

Ordinary Monte Carlo samples each default with probability p. When the event is rare, it may observe zero tail events and report a misleading zero estimated standard error. Importance sampling instead samples defaults under an *artificial* probability q (typically greater than p), then corrects each simulated scenario using the likelihood ratio:

`w(K) = (p/q)^K ((1-p)/(1-q))^(n-K)`.

The importance-sampling estimate averages `w(K) * 1[K >= threshold]`. Its sample standard error uses the standard deviation of these weighted outcomes divided by sqrt(number of paths). The exact binomial tail is an independent analytical benchmark. A larger q is **not automatically better**; excessive tilting can increase variance.

## Reproduce

Requires **Python 3.11+**, standard library only (no third-party dependencies or downloaded prices):

```bash
cd quant-projects/50-rare-event-importance-sampling
python -m unittest -v test_rare_event.py
python -m py_compile rare_event.py test_rare_event.py
python rare_event.py --n 30 --p 0.02 --threshold 5 --q 0.17 --paths 20000 --seed 50
```

The CLI reports exact, ordinary Monte Carlo and importance-sampling event probabilities plus their individual path-based standard errors. Inputs cap the number of borrowers and paths, reject nonfinite or boundary probabilities, and validate seed and threshold. No broker actions, real counterparty data, or licensed datasets are used.

## Validation and limitations

Six deterministic tests cover analytical limiting examples, seeded repeatability, a loose five-standard-error comparison with the exact benchmark, nonnegative outputs, and invalid-input rejection. The authored implementation passed **6/6 local tests**, compilation and a 1,000-path CLI smoke test on 2026-11-20. **The exact published GitHub revision, hosted CI, historical calibration, and independent model review remain unverified.**

Assumptions include independent homogeneous defaults, deterministic severity, one-year horizon and known p. The model excludes default correlation, exposure at default, recovery uncertainty, parameter estimation, time variation and portfolio concentration. Sample standard errors are not model-risk bounds. The comparison is illustrative, not proof that a particular tilt is optimal.

## Fixed tilt sensitivity extension

`tilt_diagnostics.py` compares predeclared artificial default probabilities using independent, seeded synthetic draws. It reports weighted event estimates, pathwise standard errors, event hits, the exact binomial reference, mean likelihood weight and the conventional **full-weight effective sample size** `(sum w)^2 / sum(w^2)`. ESS is a descriptive weight-degeneracy diagnostic, **not** an event-specific variance reduction guarantee; low ESS or high standard error can reveal a poor tilt. Each tilt has its own deterministic seed stream, so cross-tilt estimates are not paired.

```bash
python -m unittest -v test_rare_event.py test_tilt_diagnostics.py
python -m py_compile rare_event.py tilt_diagnostics.py test_rare_event.py test_tilt_diagnostics.py
python tilt_diagnostics.py --paths 1000 --seed 50 --tilts 0.08 0.17 0.35
```

Six new deterministic tests are authored for reproducibility, exact-reference consistency, ESS bounds, the identity-tilt limit, and input guardrails. **Execution of these new tests and exact-revision CI remain unverified.** The grid is fixed in advance and does not use held-out outcomes to tune `q`. The default model is independent, homogeneous, and synthetic; no production calibration or independent review is claimed.
