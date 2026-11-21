# Project 51 — Exact heterogeneous credit-default counts (Poisson–binomial)

**Purpose.** A portfolio may contain borrowers with different one-year default probabilities. A binomial model assumes all probabilities are equal; the **Poisson–binomial** model allows distinct probabilities while retaining independent Bernoulli defaults. This synthetic educational exercise computes the entire default-count distribution exactly, without Monte Carlo sampling error.

## Business and mathematics

For borrower `i`, let `D_i` be 1 on default and 0 otherwise, with `P(D_i=1)=p_i`. Assuming independence, total defaults are `K=sum(D_i)`. Start with `P(K=0)=1` for an empty processed prefix. Adding each borrower updates each count `k`:

`new[k] += old[k]*(1-p_i)` and `new[k+1] += old[k]*p_i`.

After all borrowers, `P(K >= h)=sum(pmf[h:])` and `E[K]=sum(p_i)`. Complexity is O(n²) time and O(n) memory. This is a count model, **not** a monetary loss distribution: different exposure sizes, recovery rates and default dependence are excluded. Unlike Project 50's rare-event importance sampling, this provides an exact independent-default benchmark for heterogeneous probabilities.

## Reproduce

Python **3.11+**, standard library only; no external packages, prices or licensed market data.

```bash
cd quant-projects/51-poisson-binomial-credit-loss
python -m unittest -v test_poisson_binomial.py
python -m py_compile poisson_binomial.py test_poisson_binomial.py
python poisson_binomial.py --probabilities 0.01 0.02 0.05 0.10 --threshold 2
```

Inputs accept 1–500 finite probabilities between zero and one, including deterministic endpoints; invalid thresholds and boolean probabilities are rejected. The `n+1` threshold denotes an impossible event. Floating-point rounding can affect the last decimal places, particularly in extreme tails. Do not interpret this synthetic calculation as a regulatory capital estimate, calibrated credit model, trading signal or investment advice.

## Validation status

The original seven regression tests passed in the previously verified hosted CI checkpoint. Six additional independent-enumeration and log-tail tests are authored; execution on their published revision is not yet verified. They check analytical two-borrower probabilities, normalization, expected count, deterministic defaults, tail limits, ordering invariance and guardrails. The earlier baseline hosted CI passed, but new numerical diagnostics, historical default calibration and independent model validation remain **unverified**. Run `python -m unittest -v test_poisson_binomial.py test_numerical_checks.py` and `python numerical_checks.py --probabilities 0.01 0.02 0.05 0.10`. The second module enumerates all 2^n outcomes for n <= 16 with 80-digit Decimal arithmetic to cross-check the dynamic program. It also computes log P(all default) = sum(log(p_i)), showing when binary64 underflows to zero. This log-domain identity applies only to the all-default event; it does not make arbitrary tail sums numerically stable. Enumeration is exponential and deliberately capped. Next: add dedicated CI coverage, verify new tests, and extend to heterogeneous EAD/LGD with explicit discretization error.


## Heterogeneous monetary loss extension (synthetic)

`monetary_loss.py` adds an **independent-default** exact distribution of monetary loss in integer cents, using per-borrower exposure at default (EAD) and loss given default (LGD). Each borrower contributes either zero or `EAD_i × LGD_i`; a sparse dynamic program combines the outcomes. Expected loss is `sum(p_i × EAD_i × LGD_i)` in cents, and the tail is the sum of mass at losses greater than or equal to the chosen threshold. Distinct borrowers can have the same loss, so their masses coalesce.

This is **not** a discretized approximation: inputs whose product cannot be represented as a whole cent are rejected. For sub-cent precision, choose a finer integer unit and adapt the implementation explicitly; do not silently round. The method has up to `2^n` distinct loss states, hence the deliberate **16-borrower** limit. Probabilities are floating-point, so numerical rounding and extreme-tail underflow remain possible. This is not a dependence model, regulatory loss forecast, or production risk engine.

```bash
cd quant-projects/51-poisson-binomial-credit-loss
python -m unittest -v test_monetary_loss.py
python -m py_compile monetary_loss.py test_monetary_loss.py
python monetary_loss.py --probabilities 0.01 0.05 --exposures-cents 10000 20000 --lgds 0.4 0.5 --threshold-cents 10000
```

Six new regression tests are authored but **runtime execution and hosted CI for this extension are unverified**. No real credit observations or licensed data are included. Independent mathematical review and calibration remain pending.


## Independent monetary-loss reference tests

`test_monetary_reference.py` enumerates all default/no-default combinations independently of the monetary-loss dynamic program, then reconciles the loss probability mass, direct expected-loss identity, and threshold tail sums on small synthetic portfolios. It includes colliding losses, deterministic borrowers, zero LGD, order invariance, and a deliberately underflowing rare joint-default event. Underflow yielding zero in binary64 **does not mean the true event is impossible**. The reference is an internal educational cross-check, not an independent external audit.

```bash
cd quant-projects/51-poisson-binomial-credit-loss
python -m unittest -v test_poisson_binomial.py test_numerical_checks.py test_monetary_loss.py test_monetary_reference.py
python -m py_compile monetary_loss.py test_monetary_reference.py
```

Five new tests are authored; only local syntax compilation of the new test module has been confirmed. Runtime execution, exact-revision hosted CI and independent model review remain unverified.


## Log-domain all-default diagnostic

`log_default_diagnostic.py` computes `log P(all default) = sum(log(p_i))` for independent borrowers. This retains a finite log probability when `P(all default)` underflows to zero in ordinary binary64 arithmetic (for example, two probabilities of `1e-200`). A true zero input yields negative infinity. This **does not** calculate a general loss-tail probability, repair the monetary-loss PMF, or validate a dependence model. It is a narrow diagnostic for a specified joint event, not a replacement for a stable general tail algorithm.

```bash
cd quant-projects/51-poisson-binomial-credit-loss
python -m unittest -v test_log_default_diagnostic.py
python log_default_diagnostic.py --probabilities 1e-200 1e-200
```

Four new synthetic tests are authored for ordinary probabilities, underflow, endpoints and invalid inputs. Execution against the published revision, independent review and historical calibration remain unverified.

## High-precision monetary tail reference

`stable_monetary_tail.py` independently enumerates up to 2^16 default masks with Decimal arithmetic, retaining extreme independent-default monetary tail probabilities that underflow in binary64. It reuses the existing cent-exact EAD/LGD input guardrails, but **does not** use the floating-point PMF to calculate its result. The default 100-digit precision is configurable from 32 to 1000 digits; Decimal input is constructed from the supplied probability's string representation, so information already lost when a caller first creates a float cannot be recovered. Runtime is exponential; this is a **small-portfolio reference**, not a scalable general tail engine.

```bash
cd quant-projects/51-poisson-binomial-credit-loss
python -m unittest -v test_stable_monetary_tail.py
python -m py_compile stable_monetary_tail.py test_stable_monetary_tail.py
python stable_monetary_tail.py --probabilities 1e-200 1e-200 --exposures-cents 100 100 --lgds 1 1 --threshold-cents 200
```

Five synthetic tests are authored, including the expected 1e-400 two-default event, comparison with the float PMF for ordinary probabilities, deterministic endpoints, and invalid inputs. **Tests and exact-revision CI have not been executed or verified in this publication milestone.** No licensed data, independent model review, dependence calibration, or production certification.

## Bounded sparse high-precision monetary-loss DP

`sparse_monetary_tail.py` uses a sparse map from **exact integer-cent losses** to **Decimal probability masses**, combining independent borrower default/no-default outcomes. Unlike exhaustive default-mask enumeration, identical loss totals merge at every step. This can handle more than 16 borrowers when loss-state collisions keep the map small, but worst-case state growth remains exponential. The method **never silently prunes states**: it raises an error if the configured state limit is exceeded. Inputs allow 1–128 borrowers, Decimal-string probabilities, precision 32–1000 digits, and 2–100,000 states. EAD × LGD must be a whole cent; no rounding or loss discretization is performed.

```bash
cd quant-projects/51-poisson-binomial-credit-loss
python -m unittest -v test_sparse_monetary_tail.py
python -m py_compile sparse_monetary_tail.py test_sparse_monetary_tail.py
python sparse_monetary_tail.py --probabilities 1e-200 1e-200 --exposures-cents 100 100 --lgds 1 1 --threshold-cents 200
```

The six synthetic tests compare small portfolios to independent Decimal default-mask enumeration, exercise an underflowing 1e-400 joint tail, deterministic endpoints, borrower ordering, state-limit rejection, and invalid inputs. **New tests and exact-revision hosted CI remain unverified until executed.** This remains an independent-default educational model, not a scalable production engine or a calibrated credit-risk estimate. For very many borrower states, more specialized methods and independent numerical validation are required.

### Larger synthetic state-growth checks (2026-11-21)

Three additional regression tests exercise a 20-borrower equal-severity portfolio against the analytical binomial tail (21 possible loss states rather than 2^20 default masks), confirm fail-closed behavior at a 20-state cap, check deterministic endpoint behavior at the 128-borrower input limit, and compare 32/100/1000-digit settings for a 1e-400 event. These are **synthetic mathematical invariants**, not evidence of historical calibration or general scalability. Run:

```bash
python -m unittest -v test_sparse_monetary_tail.py
python -m py_compile sparse_monetary_tail.py test_sparse_monetary_tail.py
```

Project 51 now contains **45 authored tests**. These three additions have **not been verified by exact-revision CI**; the last verified 36-test checkpoint is documented in the tracker. The sparse state cap bounds retained states, not CPU time or memory to a fixed operational service-level target. Independent mathematical review remains pending.


## Reproducible sparse-state growth benchmark (2026-11-21)

`state_benchmark.py` compares five equal-severity portfolios (4, 8, 12, 20, 40 borrowers) with an **independent combinatorial binomial formula**, and three distinct power-of-two severity portfolios (4, 8, 12 borrowers) with **exhaustive Decimal enumeration**. Default probabilities are fixed at 0.25; all values are synthetic. The equal-severity cases have exactly `n+1` possible loss states, while the distinct-severity cases have `2**n` possible states. These counts describe mathematical support, not measured peak memory. Each case records the probability, independent reference, absolute difference, expected support size, precision, state cap and descriptive elapsed seconds. Timings vary by hardware and are **not** service-level benchmarks. No third-party market data is downloaded.

```bash
cd quant-projects/51-poisson-binomial-credit-loss
python -m unittest -v test_state_benchmark.py
python -m py_compile state_benchmark.py test_state_benchmark.py
python state_benchmark.py --precision 100 --max-states 10000
```

Five new deterministic regression tests are authored, including state-cap rejection and invalid-input checks. Local syntax compilation succeeded for an authored-source copy; full runtime execution and exact-revision GitHub Actions remain **unverified** until checked. The benchmark is intentionally bounded (40 equal-loss borrowers, 12 distinct-loss borrowers); the underlying sparse solver still has exponential worst-case growth. The exhaustive reference uses exactly representable 0.25 probabilities because its legacy validation accepts float inputs. Independent mathematical review, correlated-default modeling, historical calibration and production certification remain pending.
