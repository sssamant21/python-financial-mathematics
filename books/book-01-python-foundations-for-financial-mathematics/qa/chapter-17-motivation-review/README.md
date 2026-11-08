# Section17.1 — scoped numerical motivation lab and answer review

Baseline manuscript: `768cafb968d261c3c801f8e8d5af71d7f2c5feca`. One core workflow, all35 local worked answers and twelve lab steps reviewed. Predicate, workflow, answer and historical unique method counts remain separate.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-motivation-review/review.py
```

Reproduce unchanged-source failures (requires baseline in Git history; expected nonzero exit writes baseline.json):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-motivation-review/review.py 768cafb968d261c3c801f8e8d5af71d7f2c5feca
```

Exact-source execution: printed demonstration/twelve existing unittest methods, silent import and printed compileall in isolated temporary directories. Final results.json retains three successful commands,51 passing supplemental predicates, hashes, raw output, runtime/platform and independent rational/Decimal references/tolerances. No new historical unique methods. Standard-library only; no SciPy backend run in this section.

## Baseline, observer policy and corrections

baseline.json retains16 failed predicates with the final observer. The twelve original unittest methods already passed. F158 corrects sign-product underflow admitting same-sign brackets, overflowing midpoint/grid construction, false stagnation convergence, callback/coordinate schemas, NPV cancellation/power overflow, quadrature accumulation/reporting overflow/underflow and huge-input contracts. The diagnostic-extension predicate adds reported bracket-radius/termination fields rather than treating their former absence as an arithmetic bug. All-zero IRR rejection is an explicit non-identifiability policy: every valid rate solves that equation, so returning an arbitrary endpoint is not a unique financial IRR.

initial-zero-tolerance-baseline.json preserves the initial48-predicate inventory with16 failures. Three known-zero NPV probes required exact zero even though their ordinary binary-float errors were below1e-12 dollars. observer-tolerance-correction.json records that overly strict observer policy; final comparisons use the explicit1e-12 absolute dollar budget for those three examples. The final observer also adds three coordinate/diagnostic probes, producing51 checks and16 failed baseline predicates. These inventories are not added; the three harmless roundoff differences are not counted as source defects. No observer crash occurred.

NPV uses integer/displayed-decimal rational discount arithmetic and finite/nonzero-preserving final float reporting. Rates exceed−1 and cashflows occur at equally spaced integer periods starting t0. No irregular-date/XIRR convention or empirical cashflow calibration. Tiny NPV−1e-308 is preserved rather than reported as zero; nonzero results outside float reporting range reject.

Bisection compares signs without multiplying endpoint values. Callback coordinates are finite floats; exact midpoint/grid arithmetic is based on their binary values. Callback results are finite int/float, excluding booleans. Integer bounds whose displayed float conversion loses their distinction, collapsed grid nodes, float stagnation and invalid stopping rules have explicit rejection/failure contracts. `iterations` counts midpoint evaluations; general n-halvings error formulas refer to bracket reductions, not an interchangeable evaluation count.

Reported x_error_bound is the maximum distance from the actual rounded midpoint to current endpoints for width termination. It is conditional on a continuous function and valid accurately evaluated bracketing signs, not proof of continuity/existence/uniqueness or the unrounded model. Callback-zero termination is numerical evidence about that callable. The discontinuous step example terminates by width with residual magnitude1: the observer records it as a precondition counterexample, not an accepted root.

Quadrature accumulates weighted callback values exactly under the displayed-value policy, then reports. Callbacks still run at rounded float nodes; exact accumulation does not erase callback or discretization error. Grid optimization returns a discrete optimum, retains the supplied objective value type and chooses the earliest exact tie. It is not a general continuous optimizer.

## Independent expectations and all35 answers

References use rational discount equations, polynomial factorization, analytic sqrt(2) at80-digit Decimal precision, bracket-halving bounds and exact finite-grid formulas. For x² on[0,1], trapezoid_N=1/3+1/(6N²), so error shrinks by100 when N multiplies by10. These derivations are supplemental oracles, not extra manuscript solvers.

| Answers | Review and executed boundary |
|---|---|
| 1–2 | Source NPV at.1 within1e-12 dollars of0; source IRR within1e-12 absolute rate error of1/10 and original-equation residual re-evaluated. |
| 3–8 | Yield residual formulation and continuity prerequisite reviewed; source x²−2, endpoint root, nonbracketing rejection and independent midpoint/ten-halving width1/512/error1/1024 checked. No market bond/yield calibration. |
| 9–12 | Rational NPV polynomial has roots.1/.2, both verified and solved on separate brackets[.05,.15]/[.15,.25]. All-zero IRR is non-identifiable; source rejects. Discontinuity step residual1 illustrates absent root despite a sign change. Newton derivative failure remains conceptual; no Newton export. |
| 13–17 | Source grid hits.3 at steps10; separate true minimum.34 yields coarse.3 and finer.34. Long-only search interval, constrained QP and variance/SD units reviewed; no actual portfolio optimizer implemented in this motivation file. |
| 18–20 | Source trapezoids integrate x exactly within comparison budget and x² follows the finite-N oracle at10,100,1000. Expected payoff integral is conceptual, not a calibrated density/payoff implementation. |
| 21–23 | Interpolation/curve/calibration conventions and scale-aware tolerance needs reviewed. No interpolation, curve bootstrap or billion-dollar market calibration run here. |
| 24–28 | Residual units differ from coordinate error; relative-only tolerance near0 is unsuitable; returned diagnostics and stagnation checked. Cancellation examples executed, inverse-problem conditioning conceptual; exact arithmetic does not repair model conditioning. |
| 29–32 | Grid/quadrature refinement and original-equation substitution executed. Boundary feasibility/local versus global optimization reviewed; no nonlinear or constrained continuous optimizer acceptance. |
| 33–35 | Invalid discount domain and iteration exhaustion reject/raise. Sensitivity/scenario requirements reviewed; no external market scenario/independent economic approval. |

## Twelve lab-step contracts

Prerequisites: finite scalar callbacks, absolute tolerance units, continuity for bracket inference, known mathematical benchmarks, equally spaced cashflow timing and discrete approximation limits. Fictional USD amounts at t0 and year ends have no actual dates or source provenance.

| Step | Executed result and limit |
|---|---|
| 1 | Exact listing isolated; Python/platform/hash retained. |
| 2–4 | Source cashflows[−100,110], rate.1, IRR≈.1; returned residual/count and independent root-error budget recorded. |
| 5–6 | Source sqrt2 over[0,2] at tolerances1e-6,1e-9,1e-12. Errors independently bounded; tighter requests need no fewer midpoint evaluations. Reported radius/reason/halvings tested separately. |
| 7 | x²+1 nonbracketing interval rejects. Tiny same-sign endpoints also reject without sign-product underflow. |
| 8 | Separate nonunique IRR roots.1/.2 verified through original equations and separate brackets. Default broad bracket need not isolate either root; no unique economic selection. |
| 9 | Source x integral=.5 for several partitions. |
| 10 | Source x² estimates: N10=.335, N100=.33335, N1000=.3333335, matching1/3+1/(6N²). |
| 11 | Exact-hit.3 example separated from.34 grid-refinement example. Grids are discrete and feasibility is just the supplied scalar interval. |
| 12 | Three commands/twelve existing methods, raw outputs, initial/final reports, hashes and limitations retained. Corrected revision is containing publication commit. |

## Limits and resume checkpoint

Local Linux CPython standard library only. Exact source execution is separate from supplemental rational/Decimal expectations and conceptual financial designs. No SciPy run, irregular-date cashflows, actual market data/as-of timing, continuity proof for arbitrary callbacks, empirical conditioning/calibration, production performance, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter17 now records one core workflow and35 local answers within scope. Next: Section17.2 — Closed-Form vs. Numerical Solutions.
