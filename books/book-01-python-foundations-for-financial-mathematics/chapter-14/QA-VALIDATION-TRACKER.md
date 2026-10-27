# Chapter 14 — Independent QA Validation Tracker

**Curriculum:** Book 1 — Python Foundations for Financial Mathematics  
**Chapter:** 14 — Probability for Financial Mathematics  
**Manuscript:** 17/17 sections published as drafts  
**Certification:** **NOT CERTIFIED**  
**Audit phase:** Scoped source-extracted reference runtime complete; independent mathematical and editorial review pending.  
**Scope:** Sections 14.01–14.17 only. Book 2 is out of scope.

## Initial structural observations (historical)

- All 17 expected section Markdown files were retrieved from the GitHub default branch.
- Each section includes at least one Python fenced code block and exactly 12 `def test_` methods in the fetched manuscript.
- Total reference test methods located: **204**.
- Each section's Markdown has an even number of triple-backtick fence markers in this initial structural scan.
- The Chapter 14 index lists all 17 sections and indicates 100% manuscript publication.
- These were **static inventory findings only**. A later scoped runtime run is recorded below; mathematical correctness and link targets remain outside that run.

## Section-by-section QA matrix

| Section | Manuscript | Reference tests | Python runtime | Numerical/editorial review | Acceptance |
|---|---|---|---|---|---|
| 14.01 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.02 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.03 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.04 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.05 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.06 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.07 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.08 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.09 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.10 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.11 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.12 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.13 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.14 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.15 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.16 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |
| 14.17 | Located | 12/12 passed in scoped run | PASS — extracted reference suite, Python 3.12/Linux | Pending | NOT CERTIFIED |

**Interpretation:** All 17 reference unittest blocks were extracted from the pinned manuscripts and run with Python's unittest module: 204 tests passed in the recorded Linux/Python 3.12 environment, including Section 14.03 after its standalone exit-status fix. This is scoped runtime evidence, not comprehensive validation or certification. The earlier manually transcribed 14.01 smoke remains historical evidence; see [14.01 initial runtime evidence](qa-evidence-14.01.md) and the [new Chapter 14 runtime record](../qa/chapter-14-runtime/README.md).

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


## Phase 2 automation — source-fidelity workflow published

- [Source-fidelity Python runner](../../../tools/chapter14_source_qa.py) — extracts the published Markdown Python unittest block verbatim, compiles it, executes it, checks for 12 tests, and writes JSON evidence with source/code SHA-256 hashes.
- [GitHub Actions workflow](../../../.github/workflows/chapter14-source-qa.yml) — configured for Python 3.13, on relevant pushes and manual dispatch, with JSON artifact upload.
- **Workflow publication:** complete. **GitHub Actions run and artifact verification:** pending; no additional section is marked passed until actual results are retrieved and reviewed.
- **Caveat:** The runner focuses on the single reference unittest block in each section; additional Python example snippets require separate editorial and execution review.

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

## Known issues identified during Phase 1 (historical)

1. The root README contained unrelated "Next" references for earlier chapters that were changed by overly broad progress-index replacements. Restore those references without changing Book 2 or manuscript content.
2. The Book 1 README displayed "Chapter 14 status: In progress" despite 17/17 manuscript publication. Clarify "manuscript complete; independent QA pending."
3. The earlier publication flow reported reference tests but did not retain independent Python runtime execution evidence for Chapter 14. At that stage the tests remained unverified; the later scoped runtime record above now provides execution evidence.

## Current decision

**Manuscript publication:** COMPLETE (17/17).  
**Reference runtime:** PASS — 17/17 extracted suites, 204 tests in the recorded environment; broader labs and platforms pending.  
**Mathematical, data and editorial review:** PENDING.  
**Enterprise or academic certification:** NOT CERTIFIED.

**Next action:** Independent mathematical and editorial review and additional lab, platform and source checks; continue Book 1's runtime sequence with Chapter 13.
