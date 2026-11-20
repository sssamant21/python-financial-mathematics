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
