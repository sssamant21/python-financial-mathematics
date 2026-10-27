# Book 1 — Validation Plan and Progress Tracker

**Scope:** Book 1 — Python Foundations for Financial Mathematics  
**Status:** IN PROGRESS — manuscript complete; comprehensive validation and canonical acceptance pending.  
**Tracker initialized:** 2026-10-27.  
**Baseline:** The initial inventory used manuscript revision `f429fb81b8d8f7d228100333c76019d583200d64`; later corrections and evidence commits are identified below. Results apply only to the recorded revision, environment and scope. Changes to a reviewed file may require affected checks to be rerun.

## How to use this tracker

Work through the validation checklist and chapter matrix. For each check, record the actual command or review method, input or controlled data reference, expected and actual outcome, environment, source revision or artifact hash, reviewer, date, evidence link and finding disposition. Update the relevant status and evidence link when work is completed. Do not describe unrun, skipped or blocked work as passed; include the reason and owner or next action.

**Statuses:** NOT STARTED; IN PROGRESS; PASS (scoped check only); FAIL; BLOCKED; NOT APPLICABLE (with rationale). A runtime PASS is not mathematical review, model approval or canonical acceptance. Earlier canonical and validation claims in the manuscripts remain historical claims until independently reconciled with their evidence and current revisions.

## Current snapshot

- **Manuscript inventory:** 322 of 322 locked section numbers have matching manuscript files at the initial baseline. This is a filename inventory, not a content or QA pass.
- **Initial syntax screening:** 1,152 fenced Python blocks parsed without syntax errors at that baseline; execution, numerical correctness and illustrative fragments were not established by this check.
- **Reference runtime evidence:** Scoped runs exist for Chapters **10–21**: 2,196 passing test methods in the recorded runs (174 + 168 + 204 + 180 + 204 + 180 + 192 + 160 + 154 + 158 + 204 + 218). Chapter 18.15 and 19.15 have separately executed snippets rather than reference test suites. This is **12 chapters with scoped evidence**, not twelve comprehensively validated chapters.
- **Visualization:** One Chapter 21 synthetic chart was rendered and visually inspected; a complete visualization and accessibility review is pending.
- **Certification:** No Book 1-wide canonical, production, mathematical or model certification is implied.

## Validation checklist

| ID | Validation area | Required work / acceptance evidence | Status |
|---|---|---|---|
| V01 | Inventory and locked structure | Confirm 322 section files, exact titles, companion files and index consistency against the locked TOC; investigate duplicate or missing materials. | IN PROGRESS — file-number inventory only |
| V02 | Markdown and internal links | Check document structure, fences, relative paths and anchors with a suitable parser; reconcile false positives. | IN PROGRESS — initial heuristic only |
| V03 | External references | Check availability, relevance, authoritative source attribution and version sensitivity; record unavailable links. | NOT STARTED |
| V04 | Python syntax and dependencies | Parse relevant code, identify complete files versus fragments, verify declared dependencies and supported versions. | IN PROGRESS — initial syntax screen only |
| V05 | Reference runtime by chapter | Run documented reference suites and snippets in isolated environments; preserve failures, skips, commands and results. | IN PROGRESS — Chapters 10–21 have scoped evidence |
| V06 | Labs and exercises | Execute feasible labs, independently verify worked answers and outputs, and record prerequisites and unresolved cases. | NOT STARTED |
| V07 | Mathematical and financial correctness | Independently derive formulas and benchmarks; verify units, signs, timelines, rates, assumptions and edge cases. | NOT STARTED |
| V08 | Numerical behavior | Assess precision, cancellation, overflow, underflow, convergence, tolerances and supported ranges. | IN PROGRESS — Section 10.7 and other scoped numerical findings addressed; broader review pending |
| V09 | Integration and data validation | Check module contracts, limits, data alignment, timestamps, availability, revisions, missingness and security boundaries. | IN PROGRESS — scoped Chapter 21 tests and DST fix |
| V10 | Simulation and statistical review | Review model assumptions, generator and seed, distribution behavior, sampling uncertainty and reproducibility. | NOT STARTED — reference runtime evidence exists |
| V11 | Visualization and accessibility | Render representative outputs and inspect data, labels, units, time zones, scale, readability and accessibility. | IN PROGRESS — one Chapter 21 chart inspected |
| V12 | Packaging and platform | Build and hash artifacts, install in clean environments, run outside checkout, review dependency versions and test supported operating systems. | NOT STARTED |
| V13 | Security and privacy | Review secrets, sensitive data, file/network behavior, dependencies and evidence handling appropriate to the work. | NOT STARTED |
| V14 | Editorial, source and copyright | Review clarity, consistency, accessibility, attribution, original expression and verified references. | NOT STARTED |
| V15 | Findings and remediation | Assign severity and owner, preserve failing evidence, fix or explicitly accept limitations, rerun affected checks and record disposition. | IN PROGRESS — ten corrections and one open audit finding recorded |
| V16 | Final acceptance | Reconcile all evidence against agreed criteria and obtain required independent review and decision. | NOT STARTED |

## Chapter-by-chapter progress

The runtime column reports only evidence explicitly reviewed for this tracker. **Not assessed here** means the tracker has not yet verified historical chapter-specific runs; it does not assert that no earlier tests were performed. The remaining review columns are intentionally not inferred from runtime results.

| Chapter | Topic | Reference runtime status and evidence | Math / model / data | Editorial / sources | Acceptance |
|---|---|---|---|---|---|
| 01 | Introduction to Python for Financial Mathematics | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 02 | Python Control Flow for Financial Models | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 03 | Functions and Reusable Financial Models | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 04 | Python Data Structures for Financial Information | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 05 | Modules, Packages, Environments, and Reproducibility | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 06 | NumPy for Financial Mathematics | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 07 | pandas for Financial Data Analysis | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 08 | Visualization for Financial Mathematics | Not assessed here; historical canonical claims need evidence reconciliation | Pending | Pending | Pending review |
| 09 | Time Value of Money with Python | Not assessed here | Pending | Pending | Pending |
| 10 | Cash Flows, Annuities, and Perpetuities | PASS — 174 extracted reference tests after corrections; [evidence](chapter-10-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 11 | Loans, Mortgages, and Amortization | PASS — 168 extracted reference tests; [evidence](chapter-11-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 12 | Fixed-Income Mathematics and Bond Analytics | PASS — 204 extracted reference tests; [evidence](chapter-12-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 13 | Returns and Investment Performance | PASS — 180 reference tests after correction; [evidence](chapter-13-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 14 | Probability for Financial Mathematics | PASS — 204 extracted reference tests; 14.03 exit-status fix; [evidence](chapter-14-runtime/README.md) and [chapter tracker](../chapter-14/QA-VALIDATION-TRACKER.md) | Pending | Pending | NOT CERTIFIED |
| 15 | Statistics for Financial Data | PASS — 180 reference tests after corrections; [evidence](chapter-15-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 16 | Portfolio Mathematics | PASS — 192 reference tests after two corrections; [evidence](chapter-16-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 17 | Numerical Methods with SciPy | PASS — 160 reference tests after correction; 17.15 snippet ran; [evidence](chapter-17-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 18 | Monte Carlo Simulation for Finance | PASS — 154 reference tests; 18.15 snippet ran; [evidence](chapter-18-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 19 | Financial Data Engineering Foundations | PASS — 158 reference tests; 19.15 snippet ran; [evidence](chapters-19-20-runtime/README.md) | Pending | Pending | NOT CERTIFIED |
| 20 | Testing and Engineering Financial Python | PASS — 204 reference tests across 16 suites; [evidence](chapters-19-20-runtime/README.md) and [initial run](initial-2026-10-27/README.md) | Pending | Pending | NOT CERTIFIED |
| 21 | Integrated Capstone: Financial Mathematics Toolkit | PASS — 218 reference tests, including DST regressions; one chart inspected; [evidence](initial-2026-10-27/README.md) | Pending | Pending | NOT CERTIFIED |

A chapter's runtime entry does not mean all snippets, lab steps, exercise answers, platforms or dependencies have been tested. Refer to each evidence record for the exact scope.

## Findings register

| ID | Finding | State / evidence | Remaining work |
|---|---|---|---|
| F01 | Section 21.13 could compare repeated local times in the wrong instant order during a daylight-saving transition. | Corrected to compare UTC instants; two regression checks passed in the scoped [Chapter 21 run](initial-2026-10-27/README.md). | Broader timestamp, data and platform review pending. |
| F02 | Section 17.12 asserted a price residual tighter than warranted by its default rate-width stopping tolerance. | Test requests a tighter width and separately checks residual; original failure and rerun are retained in [Chapter 17 evidence](chapter-17-runtime/README.md). | Independent solver, tolerance and range review pending. |
| F03 | Initial link scan returned ten candidates subsequently identified as notation false positives. | Initial heuristic reviewed in [initial QA](initial-2026-10-27/README.md). | Parser-based internal-link and anchor audit plus external-link review pending. |
| F04 | Section 16.6's short-position test and worked answer omitted net covariance effects and expected 0.0576 instead of 0.0564. | Corrected test and worked calculation; original failure and rerun are retained in [Chapter 16 evidence](chapter-16-runtime/README.md). | Independent covariance and numerical review pending. |
| F05 | Section 16.9's invalid-input test expected an exception for a valid degenerate case where all weights have identical variance. | Test now checks the documented result; original failure and rerun are retained in [Chapter 16 evidence](chapter-16-runtime/README.md). | Broader review of degeneracy and numerical tolerances pending. |
| F06 | Section 15.3 compared a tiny floating-point variance of constant observations to zero exactly. | Test now uses an illustrative absolute tolerance; original failure and rerun are retained in [Chapter 15 evidence](chapter-15-runtime/README.md). | Broader numerical range and tolerance review pending. |
| F07 | Section 15.4 used an incorrect adjusted-kurtosis expected value, and centering identical decimal floats could produce a spurious nonzero moment. | Corrected benchmark and added a constant-input guard and regression case; [evidence](chapter-15-runtime/README.md). | Broader estimator and numerical stability review pending. |
| F08 | Section 14.3's standalone test runner returned exit code zero even when a test failed. | Runner now exits nonzero on failure; intentional failure probes and scoped rerun retained in [Chapter 14 evidence](chapter-14-runtime/README.md). | Broader automation and CI review pending. |
| F09 | Section 13.14 compared computed float returns with decimal literals using exact list equality. | Test now checks length and uses an absolute return tolerance; original failure and rerun retained in [Chapter 13 evidence](chapter-13-runtime/README.md). | Broader financial, numerical and performance-method review pending. |
| F10 | Section 10.1 used escaped Markdown backticks, preventing its reference code fences from rendering. | Markdown fences and inline code corrected; the extracted suite passed in [Chapter 10 evidence](chapter-10-runtime/README.md). | Broader Markdown and link review pending. |
| F11 | Section 10.7 lost precision near equal discount and growth rates when subtracting nearly equal logarithms. | Uses a stable log-ratio where representable; Decimal benchmark and fallback regressions passed; original failure retained in [Chapter 10 evidence](chapter-10-runtime/README.md). | Extreme inputs, error bounds and financial review pending. |

Add new findings with an ID, affected revision, severity, owner, reproduction, evidence, status, decision and rerun result. Do not delete historical failures when corrected.

## Execution order and update rule

1. Continue the current reference-runtime sequence with **Chapter 9**; reconcile the previously recorded evidence for Chapters 1–8 and Chapter 14 rather than treating historical claims as automatically current.
2. Perform the cross-book checks V01–V14, using risk and dependency order to prioritize mathematical, data, numerical, lab and integration reviews.
3. Record each scoped run or review in a durable evidence directory, link it from this tracker, and update the chapter row and checklist only to the scope actually verified.
4. Track corrections in the findings register; preserve original failure evidence and record the corrected revision and rerun.
5. Complete V15–V16 only after agreed criteria, independent reviews and acceptance decisions are documented.

**Next action:** Chapter 9 reference runtime validation. Broader Book 1 QA remains in progress.
