# V06 — Chapter 2 iteration and loop-control review

Date: 2026-10-29. Source revision: `9f792d034343fc946783af2036c2006a44e49235`.

**PASS (scoped): Exercises 2.13.14–2.13.32 reviewed; 106 predicates passed, zero failed.** Together with the earlier conditions review, Exercises 1–32 now have scoped records; the remaining 28 exercises and project/section-checklist review remain open. This is not full Chapter 2 acceptance or a chapter completion percentage.

| Evidence | What it establishes |
|---|---|
| [Reviewed answers](ANSWERS.md), [hashed register](answer-register.json) | 19 prompts aligned with companion claims and explicit supplemental implementations/reasoning |
| [Supplemental reference](reference.py) | Runnable schedules, bounded while/for searches, loop else, scenario reset, discounted cash flows and reconciliation |
| [Validator](review.py), [actual results](results.json) | 106 finite checks; exact rational oracles, source-claim comparisons, two unchanged companion fragment executions and boundary/counterexample cases |

The companion often provides a result or principle rather than the requested full loop/report. Finding F30 records this completeness gap. This supplement adds runnable implementations and the missing period-0, horizon, output and failure behavior without replacing the existing manuscript code. The published first-crossing values in Exercises 18 and 29 and all four published PV claims in Exercise 22 were checked directly and passed; no numerical manuscript correction was needed.

The source snippets use zero-based fence indices 9 and 10, with the Decimal import and explicit balance/rate/contribution prerequisites recorded in results.json. Other implementations here are newly supplied QA references, not source snippets mislabeled as existing code. Full source hashes bind the answer register to the reviewed revision. The companion receives only an appended link, leaving all existing fence contents and opening positions unchanged.

Benchmark policy: exact Fraction closed forms use P*(1+r)^n+C*((1+r)^n-1)/r (or P+n*C at zero rate). This differs from the iterative Decimal recurrence. First crossing is the earliest integer period whose exact benchmark reaches the target; stopping periods are compared exactly. Balance comparisons use absolute bound max(1, |oracle|)*1e-26 for these 28-digit Decimal fixtures. This is a chosen fixture bound, not a universal monetary tolerance or an error proof for all inputs. Published internal Decimal strings are additionally compared exactly under the stated 28-digit context, and published two-decimal displays are checked separately.

Cases cover period 0, final permitted year, failure just before crossing, zero horizon, stagnation, negative growth, contribution timing, missing versus zero, finite/representation/domain order, scenario-order independence and a deliberate contamination counterexample. Unbounded illustrative loops are not run. Supplemental model inputs assume finite Decimals, supported rates above -100% and bounded whole horizons; no universal business-domain, extreme-magnitude or cross-platform claim is made.

Reproduce from the repository root: `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-02-iteration-review/review.py`. Standard library only; CPython 3.12.14 on Linux x86_64. All 106 checks passed on the first run. These predicates are not 106 exercises, reference unittest methods or new unique historical workflow cases. Existing historical counts remain unchanged.

Next: Exercises 2.13.33–2.13.60 (defensive validation, applied scenarios, debugging, conceptual review and integrated/model-review challenges), then full Section 2.12 requirement and section-checklist review. Independent review, broader input/branch/platform coverage and Chapter 1 notebook/platform gaps remain open.
