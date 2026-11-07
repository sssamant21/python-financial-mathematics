# Section 15.4 — scoped shape lab and worked-answer review

Baseline manuscript revision: `6d14c3b1c34447c91d9400ac44788d97c2185b20`. Scope: one core workflow, twenty-four local answers and one ten-task mini-project. Test predicates, workflow records, exercise records and historical unique methods are separate measures.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-shape-review/review.py
```

The runner extracts the single Python fence unchanged, executes the exact printed demonstration and twelve existing unittest methods, imports without demonstration output, and runs the printed compile command in an isolated temporary directory. Three commands pass. Its supplemental observer then imports the same code and checks 49 predicates; all pass. No historical unique methods added. Raw outputs, Python/platform, expected values, tolerances and source/listing SHA-256 are in `results.json`.

## Retained baseline and F130

`baseline.json` retains ten failed predicates against the baseline revision above, plus the passing original twelve methods and three commands. Replacing the manuscript with that revision reproduces the baseline using this runner. The failures comprise three fields each for lost integer-offset spread, overflowing fourth powers and underflowing fourth powers, plus an unreportable required variance that raised raw OverflowError instead of the declared ValueError. Ten predicates are not ten distinct root causes.

F130 preserves integers, uses rational centered powers and cancels scale in standardized ratios before float conversion. Finite floats follow their displayed-decimal interpretation. Square roots use 80-digit Decimal. Every required returned field must be representable as a finite float without silently rounding a nonzero value to zero. A combined report can therefore reject an unreportable m₂ even if dimensionless shape measures are representable; adjusted-estimator functions calculate their ratios directly. This policy is explicitly documented, not a binary-float compatibility or throughput promise. Baseline failures and corrected rerun are both retained.

## Independent derivation and local answers

The observer derives moments using raw-moment expansions, independently of the source's centered-power sums: m₂=E[X²]−μ², m₃=E[X³]−3μE[X²]+2μ³, m₄=E[X⁴]−4μE[X³]+6μ²E[X²]−3μ⁴. Inputs and polynomial operations are rational; square-root expectations use Decimal. Source values are compared with recorded tolerances. For the project μ=.01, m₂=.0016, m₃=.000042, m₄=.000006088, g₁=.65625, b₂=2.378125 and g₂=−.621875. The rational oracle and source share the mathematical definition and declared decimal convention, but use different moment algorithms; neither constitutes independent human acceptance.

| Prompts | Reviewed contract and evidence |
|---|---|
| 1–3, 6–9 | Symmetric [−1,0,1] mean and m₃ zero, m₂=m₄=2/3; b₂=3/2, g₂=−3/2. Source shape fields executed; m₃/m₄ derived in oracle because source does not expose them. |
| 4–5 | [0,0,0,4] m₂=3, m₃=6, g₁=2/√3; reflection reverses sign. Both source signs and magnitudes compared. |
| 10–12 | Translation/positive scaling preserve standardized measures; negative scaling reverses skewness and preserves kurtosis. Checked against the independently derived 2/√3 and 7/3 references. |
| 13–14 | Normal population values 0,3,0 follow symmetry and E[Z⁴]=3. A fourth moment cannot uniquely specify every tail probability. Conceptual mathematical review, not fitting a normal model. |
| 15–17 | Constants rejected; adjusted skew requires n≥3 and excess requires n≥4. Exact commands and supplemental rejection predicates executed. |
| 18 | Two of four strictly negative returns give 1/2. Source executed; zero is not negative. |
| 19 | Both explicit positive/negative stresses compared against rational raw-moment expectations, demonstrating outlier sensitivity. |
| 20–22 | Positive skew does not exclude losses; kurtosis does not identify VaR; windows require frequency/adjustment/estimator alignment. Design review only, no real data windows or tail model accepted. |
| 23 | n=4 adjusted excess defined: [0,0,0,4] gives 4. Source checked; estimator stability is not established by definition. |
| 24 | Five observations justify exploratory summary only. No operational risk certification claimed. |

## Lab-step and prerequisite contracts

| Task | Evidence and limit |
|---|---|
| 1 | Synthetic fictional strategy and decimal simple-return units recorded. Dates/frequency unspecified in the manuscript and report; no invented market metadata. |
| 2 | Source exposes μ and m₂. Supplemental rational oracle supplies m₃/m₄, explicitly labeled in project report; the lab now directs learners to these formulas. |
| 3 | Source skewness .65625, kurtosis 2.378125 and excess −.621875 recorded. |
| 4 | Source adjusted skew and excess recorded and compared to the displayed correction formulas with n=5. |
| 5 | Prompt now specifies .08→.28; source positive-stress report retained and checked against independent rational expectations. |
| 6 | Separate original copy with −.04→−.24; source negative-stress report retained and checked. It does not compound the positive stress. |
| 7 | Source mean and m₂ plus supplemental population SD=.04, median=0 and type-7 Q05=−.034 recorded. These compare location, spread, quantile and shape without interchanging their meanings. |
| 8 | n=5 cannot validate stationarity, extreme-tail probabilities, dependence assumptions or forecast quality. Conceptual review. |
| 9 | Fixture hash, source/listing hashes, runtime and generated output retained. Baseline revision above; corrected revision is the containing commit. |
| 10 | Exploratory sample shows positive skew and negative excess; separate signed stresses show sensitivity. This does not imply absence of downside risk, a forecast or causal explanation. |

Prerequisites: standard-library Python/functions/sequences, prior return-unit and mean/quantile/variance sections. No SciPy/NumPy dependency, feed, notebook or external runtime is required. The printed commands and twelve existing methods are exact-source executions. The report assembly, raw-moment oracle, missing metadata declarations and supplemental SD/median/quantile are observer work, not a complete previously published executable lab. The manuscript now makes the stress values, absent metadata, population SD, type-7 convention and supplemental calculations explicit.

## Remaining scope and resume checkpoint

Scoped local Linux CPython execution and mathematical/design review only. F28 notebook/platform, F32 shared-input integration and other unresolved findings remain open. No Windows/macOS/notebook execution, real-data integration, exhaustive branch coverage, independent reviewer acceptance, performance benchmarking or certification. Chapter 15 now has four workflows and 96 local answer records reviewed. Next pending formal lab/answer review: Section 15.5 — Covariance.
