# Section 19.8 — Missing and invalid values scoped review

Baseline `f46c548b68ff7426d6d86effc462e352d77ccb35`. [Manuscript](../../chapter-19/19.08-missing-and-invalid-values.md) · [40 answer records](answer-records.json) · [synthetic decoded records](synthetic-records.json).

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-missing-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-19-missing-review/review.py f46c548b68ff7426d6d86effc462e352d77ccb35
```

The baseline invocation intentionally exits 1. [Baseline](baseline.json) and [identical predicate replay](baseline-replay.json) retain three mismatches; [corrected results](results.json) retain 44 passing supplemental predicates and three actual source commands: demonstration with 12 existing unittest methods, compilation, and quiet import. One workflow, 12 lab-step records and 40 local worked answers were reviewed. These counts are separate; zero new historical unique methods are claimed.

## F195 — caller context and complete return

The standalone return copy rounded a near-unity increment of 1e-30 to zero and the ordinary 100→102 return to zero under caller precision 2. Its complete difference/quotient now uses the adjacent modules' private 34-digit HALF_EVEN report. A zero terminal is valid for this helper, while a positive-close classifier rejects zero. Unknown or rejected records are never silently passed into the return formula.

A caller disabling Decimal's InvalidOperation trap changed the malformed text `abc` from malformed to nonfinite. Parsing now uses a private context to preserve this section's classification categories. Text conversion preserves supplied Decimal coefficients and scale; it does not quantize to 34 digits. The lexical policy remains Decimal syntax, accepting positive scientific notation, underscores and padded numeric text. Empty text, exactly N/A, whitespace-only text, lowercase/padded missing markers, nulls and absent keys remain distinct. This classifier does not inherit Section 19.7's price width/scale rules.

The independently derived interval return is (102−100)/100=1/50=.02. The middle absent observation means this is an observed-interval return, with no evidence of a one-day calendar horizon. The synthetic four-row batch has two accepted positions (1,3), two rejections (empty,nonfinite), submitted=4 and complete=False; missing/empty is one of four, not half the batch. Both rejected and accepted positions are retained. Empty input is complete=True by this local policy; it does not prove source completeness or authorize publication. Duplicates and wrong dates/currencies are deliberately not rejected by this close-only example. Caller rows are unchanged; a generator is accepted. Results are held in memory without imputation, freshness, duplicate, source-identity or publication enforcement.

## Twelve lab-step records

| Step | Review and evidence |
|---|---|
| 1 | Already-decoded dictionaries; positive finite Decimal close; exact missing-marker policy. Source identity/units are prerequisites supplied externally. |
| 2 | Verbatim Python fence extracted; Python/platform and manuscript/source hashes recorded. |
| 3 | Four demonstration rows executed; valid,empty,valid,nonfinite. |
| 4 | Submitted 4,accepted 2,rejected 2,complete False; record positions and reasons checked. |
| 5 | Exact independent 1/50=.02, zero terminal -1 and negative return -.02 checked. |
| 6 | Observed-interval horizon only; calendar/availability prerequisites absent. Conceptual review. |
| 7 | Missing key,null,zero,malformed,NaN/sNaN and both infinities checked; types and negative values included. |
| 8 | Empty→empty; whitespace-only→malformed; padded numeric text valid. Explicit Decimal lexical scope. |
| 9 | Quarantine is the returned rejected list; a consumer must block publication when required. No publication gate implemented. |
| 10 | A proposed fill policy must bound gaps, retain originals/flags and require calendar/instrument/event/availability data; no filling executed. |
| 11 | Twelve unchanged reference methods executed; source commands and supplemental predicates counted separately. |
| 12 | Synthetic decoded input identity, source hashes, actual results, reasons and scoped limits retained. No external raw-byte provenance claim. |

## Forty local prompt-to-answer records

| Exercise | Topic | Worked answer | Review scope |
|---|---|---|---|
| 1 | Missing key: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 2 | Null: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 3 | Empty text: | empty. | Direct classification/batch/return execution plus source-contract review |
| 4 | N/A: | source_missing. | Direct classification/batch/return execution plus source-contract review |
| 5 | Whitespace: | malformed. | Direct classification/batch/return execution plus source-contract review |
| 6 | abc: | malformed. | Direct classification/batch/return execution plus source-contract review |
| 7 | NaN: | nonfinite. | Direct classification/batch/return execution plus source-contract review |
| 8 | Infinity: | nonfinite. | Direct classification/batch/return execution plus source-contract review |
| 9 | Zero close: | nonpositive. | Direct classification/batch/return execution plus source-contract review |
| 10 | Negative yield: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 11 | 100→102: | .02 or 2%. | Direct classification/batch/return execution plus source-contract review |
| 12 | Missing middle day: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 13 | Zero substitution: | It can create a false −100% return. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 14 | Quarantine: | Separate invalid records for review. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 15 | Fail-fast: | Stop or reject according to policy on a violation. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 16 | Rejected row: | No. | Direct classification/batch/return execution plus source-contract review |
| 17 | Empty batch: | Complete; real policy must define this case. | Direct classification/batch/return execution plus source-contract review |
| 18 | Forward fill: | Yes. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 19 | Backward fill: | Yes. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 20 | Stale quote: | Yes. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 21 | Freshness: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 22 | Outlier: | No; investigate. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 23 | Split: | Yes. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 24 | Duplicate: | Depends on key and revision semantics. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 25 | Latest correction: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 26 | Decimal: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 27 | NaN: | No. | Direct classification/batch/return execution plus source-contract review |
| 28 | Starting price zero: | No. | Direct classification/batch/return execution plus source-contract review |
| 29 | Ending price zero: | Yes. | Direct classification/batch/return execution plus source-contract review |
| 30 | Negative return: | No. | Direct classification/batch/return execution plus source-contract review |
| 31 | Missing count: | To interpret the scope and rate. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 32 | Hash: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 33 | Source marker: | No; consult the contract. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 34 | Partial batch: | No. | Direct classification/batch/return execution plus source-contract review |
| 35 | Sensitive input: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 36 | Price type: | No. | Direct classification/batch/return execution plus source-contract review |
| 37 | Dates: | No. | Direct classification/batch/return execution plus source-contract review |
| 38 | Memory: | Yes. | Direct classification/batch/return execution plus source-contract review |
| 39 | Tests: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |
| 40 | Source quality: | No. | Conceptual/policy only; not source-quality/point-in-time acceptance |

F28 notebook/platform, F32 shared-input integration, F165 tails, F185 signed-normal-terminal integration and independent review remain open. Coefficient/exponent resources, external input decoding, source quality, currency/price semantics, timestamps/calendar, corrections, imputation and publication acceptance are outside this batch. Next: Section 19.9 Date and Timestamp Normalization formal workflow and local answers.
