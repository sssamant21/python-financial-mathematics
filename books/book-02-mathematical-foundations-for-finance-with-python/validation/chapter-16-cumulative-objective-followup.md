# Section 16.10 — Exact cumulative-objective scope

**Date:** 2026-10-30  
**Category:** COV-75, partially addressed; independent review pending.  
**Original main:** `73d698d5956c8b65a7f36f1d786586420b5f5622`  
**Executable snapshot:** `692e8ffd8425c2fab1a0695f8c647b4fc5a128d7`

## Baseline and scope change

[Machine evidence](chapter-16-cumulative-objective-followup.json) retains the original missing-evidence assertion failure, original source hashes, final scoped manifest and all twenty-two script outputs. The baseline reported aggregate curvature14 without separate executable evidence for Exercises1–5 or11–13. This was a coverage gap, not a demonstrated arithmetic error in the existing aggregate solver.

Source change `6c93ed8e5134ed4de94f3d29fefb391e7b65b66c`, blob `ee88d1d685a38db8a326cdf108717d3b05ce50eb`, adds `exercise_objectives()` to the final lab output. It evaluates the actual single-observation calibration through the existing loss/gradient/Hessian APIs and runs the actual Sections16.5/16.6 gradient-descent/Newton helpers for the curvature-one shifted quadratic.

| Written objective | Actual executable scope | Curvature |
|---|---|---:|
| Exercises1–5: half-squared normalized residual at time2/price1100 | Only observation `(2,1100)` | 4 |
| Exercises11–13: `0.5*(x-3)^2` | Center3, supplied curvature1 | 1 |
| Exercise17 / ProblemA calibration | Three original observations | 14 |

A common minimizer does not make the first and third objective equivalent.

## Independently derived references

[Runnable checker](../chapter-16/code/check_cumulative_objectives.py) derives the single-observation objective by expanding the written polynomial:
`L(r)=2*r^2-r/5+1/200`, `g(r)=4*r-1/5`.
Eight loss/gradient fields at four dyadic rates match independent Fraction expectations within three loss ulps and two gradient ulps. The stationary rate1/20, zero represented-price loss/gradient and curvature4 are separately checked.

For the curvature-one shifted quadratic, the independent recurrence is
`x_k=3*(1-(1-alpha)^k)`.
Four real gradient-descent runs at steps0.5,1,2,3 validate **33 exact history fields** (point, objective and gradient over eleven rows), their stopping statuses and iteration counts. The half-step history is `0,1.5,2.25`; the unit step terminates at3 after one iteration; step2 oscillates `0,6,0`; step3 gives `0,9,-9`. The actual Newton helper reaches3 in one iteration with history gradients-3,0.

Two deliberately wrong variants are detected: replacing single-observation curvature4 with aggregate curvature14, and replacing the first half-step point1.5 with the curvature-two point3. These demonstrate sensitivity to the specific scope confusion.

Finite numerical examples do not prove the global-convexity claims in Exercise5 or the complete stability theorem in Exercise12. Those proofs and remaining worked solutions still require review.

## Actual execution and reproduction

**32/32 Chapter16 Python files compiled; 22/22 check scripts exited zero**, Python3.12.14/Linux, assertions enabled, cwd each script's parent, 15-second timeout. Original unchanged source bytes matched pinned blobs; the complete corrected scoped manifest matched the published executable snapshot.

[V-44 full refresh](runtime-refresh-2026-10-30-r8.md), at the same executable snapshot, compiled **476 files**, passed **265 scripts**, and verified **477 required source/fixture hashes before and after**. It also covers the preceding Section16.10 per-candidate assessment change/checker.

From a checkout of `692e8ffd8425c2fab1a0695f8c647b4fc5a128d7`:
```bash
cd books/book-02-mathematical-foundations-for-finance-with-python/chapter-16/code
python check_cumulative_objectives.py
```
For the missing-evidence baseline, copy only this checker into a separate checkout of the original revision and run before adding the new lab output; its first exercise-scope assertion fails.

Twenty-eight selected COV categories remain partially addressed; none closed by the register. No independent sign-off, supported-platform validation, release acceptance or canonical approval is inferred.

Next executable item: COV-74 Sections16.9/16.10 normalized objective/loss intermediate range and false-zero cases, using exact represented-residual expectations before corrections. Other exercise proofs, model assumptions, threshold/configuration and conditioning obligations remain open.
