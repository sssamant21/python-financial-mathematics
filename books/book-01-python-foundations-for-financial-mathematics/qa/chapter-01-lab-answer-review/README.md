# Book 1 V06 — Chapter 1 core answers and project checklist

**Status: scoped review batch passed after corrections; Chapter 1/V06 remain IN PROGRESS.** Reviewer: Codex. Recorded 2026-10-28. Initial source revision: `fb5f6814e8b6da8307d5608bbf65d36af0bda475`; the after-results additionally include the companion corrections published with this record. This uses a separate arithmetic method, not an independent human reviewer or model-approval decision.

## Scope and observed results

| Review unit | Actual result / scope |
|---|---|
| Section 1.13 Exercises 1–48 | Prompt/solution alignment and stated units, conventions, domains and explanations reviewed; 48 hash-bound records retained |
| Answer comparisons | 85 comparison predicates passed; seven rational derivations recorded separately as benchmarks, not counted as tests |
| Section 1.12 project checklist | All 23 checklist items assessed within the recorded source/synthetic-input scope; student checkboxes left unchanged |
| Complete project/applied/capstone programs | 40 controlled subprocess cases passed; actual stdin, output, expected fragments and rationale retained |
| Modified Solution 13 snippet | Conversion/display passed with inputs 10000 / 5 / 3; affected snippet also compiled on actual Python 3.10.22, 3.12.14 and 3.13.16 |
| Source integrity | One Python fence changed, 1,159 unchanged, total 1,160; current ledger updated and changed snippet revalidated |

The 40 process cases include all six calculator operations; zero and meaningful negative rates; a large finite input; annual/monthly compounding; signed percentage changes; profit/loss/break-even; fractional quantities; the subcent-gain regression; posted fees; exact/below/at/above reconciliation; malformed text/integer input; NaN/Infinity; and negative tolerance. They also run all four applied reference programs and the capstone's required success, zero, invalid-input, rounding-boundary and reconciliation-boundary demonstrations. This is a bounded fixture set, not exhaustive domains or every prose instruction.

The case outputs are compared after whitespace normalization, with zero process exit and empty stderr required. These educational programs can print a rejection and exit zero; a passed rejection case means the expected message appeared, not that they implement a production CLI exit-code policy.

## F26 — incorrect unrounded compound-growth answer

**Severity:** Low, numerical answer transcription. **State:** CORRECTED. **Owner:** Codex.

Solution 12 originally printed `6842.845252608`. Its actual code and exact rational calculation give:

`5000 × (26/25)^8 = 6842.845252026368`.

The final cent answer remains **$6,842.85** under the stated half-up policy. The textual exact answer is corrected; the formula and source calculation are unchanged. The original failing comparison is retained in [answer-checks-before.json](answer-checks-before.json), and the corrected comparison in [answer-checks.json](answer-checks.json).

The benchmark engine uses `fractions.Fraction` and integer quotient/remainder rounding. It does not call the manuscript's Decimal growth or rounding helpers to produce expected values. Decimal source execution is then compared with the rational expectations. Exact annual/monthly growth fractions and cent outputs are retained in [rational-benchmarks.json](rational-benchmarks.json). Monthly growth is not claimed to be an exact finite decimal: its rational result is rounded by integer arithmetic.

## F27 — incomplete prompt/answer alignment

**Severity:** Low, instructional completeness. **State:** CORRECTED for the listed items. **Owner:** Codex.

Solution 13 converted inputs without displaying the interpreted values requested by the exercise. Its existing Python block now prints principal, annual decimal rate and years before any calculation. The before-run output was empty; the after-run output is:

```text
Interpreted principal: 10000
Interpreted annual decimal rate: 0.05
Interpreted years: 3
```

This remains a conversion/display teaching snippet for valid inputs; the later applied programs supply validation and calculation-specific domains. The changed block is revalidated and its new hash is in the [current coverage ledger](current-coverage-ledger.json); its previous source-selection record is retained as old-payload evidence, rather than carried forward as unchanged.

The prose answers now also supply the requested two financial-question examples, category explanations for Python benefits, type-use examples, and an explicitly parenthesized simple-interest expression. The reflection guide now addresses model assumptions and possible later redesigns, which were missing from its 13-question alignment. None of these additions establishes production or financial-model suitability.

## Project checklist and reproducible cases

[project-checklist-review.json](project-checklist-review.json) records each original Section 1.12 checklist item and its evidence links/case identities. Source inspection covers Decimal construction, explicit cent/rounding policy, rounding stages and stated exclusions; controlled runs cover outputs and rejection boundaries. Rational derivations provide a separate numeric comparison method. This is a review by the recorded assistant, not independently signed human verification.

[workflow-checks.json](workflow-checks.json) retains all 40 actual subprocess results, including stdin and stdout/stderr. Some inputs overlap earlier runtime batches, so these 40 lab-review executions are recorded separately. They are **not** added to the earlier 192 source-mapping workflow count as unique new curriculum coverage. No unittest methods were added; the historical 2,996-method total remains unchanged.

[exercise-review-register.json](exercise-review-register.json) binds each of the 48 exercise prompts and solution sections to hashes and applicable checks. Empty automated-check lists identify qualitative items reviewed from their actual text; they are not disguised as executed numeric tests. The record is a technical, scoped review, with independent human/editorial/model acceptance still pending. The scripts regenerate automated results; the per-item assessment notes and checklist dispositions are review artifacts that require fresh review after relevant source changes.

## Harness dispositions

The first answer checker reported the two real source findings above and one false positive: a mathematical percent sign was written as `\%`, so a literal `%` search missed the correct −50% answer. Normalizing that TeX spelling resolved the false positive without a source change. An intermediate harness cleanup also accidentally removed a local interest assignment and raised `NameError`; that harness assignment was restored before the completed acceptance run.

The first process matrix had 38/39 passing cases: the integer-input rejection correctly printed `Invalid input: ...`, but the new oracle expected `Invalid numeric input`. The actual rejection was correct. [The first result](workflow-checks-first.json) is retained; the oracle was corrected, an explicit NaN case was added, and all 40 final cases passed. These harness issues are distinguished from manuscript findings in [harness-dispositions.json](harness-dispositions.json).

## Reproduction

Use CPython 3.12 and [requirements.txt](requirements.txt); [environment.json](environment.json) records the observed runtime. From this evidence directory, choose fresh output directories:

```bash
python review_answers.py ../.. /tmp/book1-ch01-answer-reproduction
python review_workflows.py ../.. /tmp/book1-ch01-workflow-reproduction
```

The first script extracts the exact companion solution blocks, supplies declared context/input fixtures and uses rational/integer oracles. It returns nonzero on any failed comparison. Benchmark-generation records remain separate from pass predicates. The second script extracts the actual complete manuscript programs and runs controlled synthetic inputs with 20-second timeouts. It returns nonzero on an exit failure, stderr or missing expected output. No external financial data or service is required. [Affected syntax results](affected-syntax-checks.json) are compilation only, not cross-version runtime/platform acceptance.

[Source hashes](source-manifest.json) and [the code-change audit](code-change-audit.json) bind this review to the corrected files. The locked structure and fence inventory are unchanged. Python behavior was checked against the official [Python 3.12 decimal documentation](https://docs.python.org/3.12/library/decimal.html) and [built-in functions/input documentation](https://docs.python.org/3.12/library/functions.html#input). The hosted pages showed patch 3.12.16 when consulted; actual executions used 3.12.14. The documentation family and runtime versions are not treated as an exact-version compatibility certification.

## Remaining Chapter 1 work

Chapter 1 is **not complete under V06**. The 40 short section exercises in Sections 1.6–1.10 still need their own formal answer/step records. The three integrated challenge references remain design sketches rather than complete end-to-end implementations. Learner-specific environment/JupyterLab instructions, interpretation of all reflection responses, broader input ranges, alternative decimal contexts and platform behavior remain open. The [V06 chapter tracker](../LAB-ANSWER-TRACKER.md) preserves that queue; no global lab-completion percentage is inferred from the 449-heading candidate inventory.
