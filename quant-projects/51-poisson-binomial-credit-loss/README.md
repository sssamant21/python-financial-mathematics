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
