# Chapter 14 — Independent QA Validation Tracker

**Curriculum:** Book 1 — Python Foundations for Financial Mathematics  
**Chapter:** 14 — Probability for Financial Mathematics  
**Manuscript:** 17/17 sections published as drafts  
**Certification:** **NOT CERTIFIED**  
**Audit phase:** Phase 1 — GitHub manuscript inventory and structural review  
**Scope:** Sections 14.01–14.17 only. Book 2 is out of scope.

## Verified structural observations

- All 17 expected section Markdown files were retrieved from the GitHub default branch.
- Each section includes at least one Python fenced code block and exactly 12 `def test_` methods in the fetched manuscript.
- Total reference test methods located: **204**.
- Each section's Markdown has an even number of triple-backtick fence markers in this initial structural scan.
- The Chapter 14 index lists all 17 sections and indicates 100% manuscript publication.
- These are **static inventory findings only**; Python syntax, runtime behavior, mathematical correctness, and link targets have **not** been independently verified by this scan.

## Section-by-section QA matrix

| Section | Manuscript | Reference tests | Python runtime | Numerical/editorial review | Acceptance |
|---|---|---|---|---|---|
| 14.01 | Located | 12/12 passed in transcribed local reference implementation | Initial smoke PASS; source fidelity pending | Pending | NOT CERTIFIED |
| 14.02 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.03 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.04 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.05 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.06 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.07 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.08 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.09 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.10 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.11 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.12 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.13 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.14 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.15 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.16 | Located | 12 test methods found | Not executed | Pending | Pending |
| 14.17 | Located | 12 test methods found | Not executed | Pending | Pending |

**Interpretation:** For 14.01, 12/12 tests passed on a manually transcribed reference implementation in Python 3.13.5; byte-for-byte source fidelity to the published Markdown is still unverified. The other 16 sections have only been statically inventoried. All sections remain **NOT CERTIFIED** until independent source-fidelity runtime and editorial evidence is collected. See [14.01 initial runtime evidence](qa-evidence-14.01.md).

## Phase 2 — Python extraction and execution

For each section, extract Python fenced blocks, distinguish standalone code from snippets, and execute each documented standalone lab using an isolated supported Python 3 environment. Record:

1. File path, blob SHA, and repository commit.
2. Python version, operating system, and dependency versions.
3. Syntax compilation result and exit code.
4. `unittest` execution count, failures, errors, and skips.
5. Captured stdout/stderr, execution duration, and seed.
6. Any manual or environment-dependent steps.
7. Reviewer and date.

Do not label a section "runtime validated" if its tests were only read or counted.

## Phase 3 — Mathematical and editorial review

- Independently recalculate all probability examples, distribution moments, default probabilities, and portfolio risk formulas.
- Check probability bounds and normalization.
- Review sample versus population variance, units, horizons, and sign conventions.
- Review normal VaR caveats, tail accuracy, bootstrap assumptions, and reproducibility.
- Validate all internal Markdown links and headings.
- Ensure exercise statements and solutions reconcile.
- Confirm Chapter 14 status is consistent across root README, Book 1 README, MASTER-TOC, and Chapter 14 README.

## Phase 4 — Integrated acceptance

- Run the Chapter 14 simulator and final assessment lab in a clean environment.
- Verify deterministic replay with fixed seed and record manifest.
- Execute negative tests for invalid inputs and nonfinite values.
- Review Monte Carlo sampling tolerances and tail-risk assumptions.
- Obtain independent technical, mathematical/editorial, and application-owner signoff.
- Mark **CERTIFIED** only when all gates have retained evidence and approvals.

## Known issues identified during Phase 1

1. The root README contained unrelated "Next" references for earlier chapters that were changed by overly broad progress-index replacements. Restore those references without changing Book 2 or manuscript content.
2. The Book 1 README displayed "Chapter 14 status: In progress" despite 17/17 manuscript publication. Clarify "manuscript complete; independent QA pending."
3. The earlier publication flow reported reference tests but did not retain independent Python runtime execution evidence for Chapter 14. The tests therefore remain unverified.

## Current decision

**Manuscript publication: COMPLETE (17/17).**  
**Structural inventory: COMPLETE (17/17).**  
**Independent Python runtime: IN PROGRESS (1/17 initial smoke-tested; 0/17 source-fidelity validated or independently certified).**  
**Mathematical/editorial review: PENDING.**  
**Enterprise or academic certification: NOT CERTIFIED.**

**Next action:** Establish source-fidelity execution for 14.01, then extract and execute 14.02 onward, recording results and failures section by section.
