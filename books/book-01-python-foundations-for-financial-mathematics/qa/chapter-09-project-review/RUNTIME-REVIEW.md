# Section 9.16 — Runtime follow-up and candidate disposition

Baseline `0e875ff0c65c8c302bc6b0b04f042710ba246f42`, 2026-11-05. The source Git blob was 7e70580b8b7ad7b3bac06b9192c31be961e1d32d, unchanged from the static checkpoint. Prepared Linux CPython 3.12.14, standard library only. The earlier unavailable environment is available for these CLI checks; this does not close F28 notebook or other-platform gaps.

**Final:** two exact documented commands, 37 additional predicates and twelve existing embedded methods passed. One project workflow and eight local prompts scoped; prompt8 remains design-only. No historical unique methods were added. Four runs are retained, each separately stamped with source/listing SHA-256, raw outputs, environment and per-check dispositions:

| Run | Source | Commands | Supplemental predicates | Outcome |
|---|---|---|---|---|
| [Initial](runs/20261105T161259Z-99e422bec075/results.json) | Original | 2 pass; twelve methods pass | 33 | 14 fail |
| [First corrected](runs/20261105T161350Z-aef5935aa7c8/results.json) | Corrected | 2 pass; same twelve methods | 33 | All pass |
| [Expanded baseline](runs/20261105T161421Z-89af37dc8f3b/results.json) | Original, restored as separate source copy | 2 pass; same twelve methods | 37 | 15 fail |
| [Expanded corrected](runs/20261105T161421Z-2af296d13523/results.json) | Corrected | 2 pass; same twelve methods | 37 | All pass |

The expanded checks add nonfinite nominal log-factor rejection, immutable configuration, literal CSV zeros, and small-amount continuous scaling where the intermediate factor overflows but the final amount is representable. Only the new finite-factor probe fails on baseline. These are repeated invocations of existing source methods, not additional historical methods. The source adds assertions within test_10_invalid_inputs while retaining twelve method names. The baseline copy's temporary absolute path is captured in its JSON; its hash pins the original manuscript content.

## Confirmed and corrected

- C916-01 / F46: nonzero Fraction amount, rate and time underflowed to zero before validation (three probes). real now checks original nonzero input against its converted value.
- C916-02 / F48: overflowed total periods or division underflow returned zero implied rate (two probes). The solver rejects nonfinite total periods and nonzero log change lost to zero inferred rate.
- C916-03 / F49: separate logarithms erased nearby-balance growth, yielding zero times/rates and admitting an opposed target; time division underflow and nonfinite nominal log growth also returned zero (seven probes). Nearby magnitudes use relative change/log1p, separated magnitudes retain log differences; finite-growth and nonzero-time safeguards added.
- C916-04/C916-05 / F50: extra CSV cells were ignored; a nonzero amount became zero and a negative time became signed zero before validation (three probes). Surplus fields are rejected. A Decimal lexical boundary checks finite and nonzero values before float conversion, retaining the original meaning until range checks complete. Valuation remains float-based. Literal zeros remain valid.

F50 has medium instructional/data-integrity severity; owner manuscript maintainer/QA executor. The fifteen original failures and corrected rerun substantiate closure only for these cases. CSV quoting, arbitrary precision, input-size limits and exhaustive schema/domain fuzzing are not claimed.

## Source execution, independent oracles and design scope

The exact single listing is extracted as tvm_engine.py into an isolated directory and executed and compiled. Its JSON stdout and test stderr are captured separately. Additional source calls run the literal CSV→parse→report→JSON pipeline, verify per-event amounts/years/discounts/PVs and reconcile total NPV. Each retained run has the CSV input and a source-generated sample report; the final report NPV matches independent 100-digit Decimal expectation 31.819158817370702… within explicit tolerance. Exact rational powers derive monthly FV and EAR; nearby one-year implied rates derive directly from the represented balance ratio minus one. The prior seven executed JavaScript rational benchmarks remain separate supplemental evidence, not Python source tests.

All twelve source acceptance gates ran in the embedded suite and have supplemental probes where listed in review.py. Same-sign negative roundtrip, continuous inversion, negative/zero rate boundaries, empty schedules and no hidden cost passed. The day-count extension is a conceptual answer; no calendar engine was implemented. No install, Windows/PowerShell, notebook, market-data, independent financial reviewer or production/security approval was executed. F28/F32 and broader Book 1 acceptance remain open.

Reproduce using review.py; every invocation creates a fresh run directory. Use --source with the original manuscript from the baseline commit to reproduce initial failures. Refresh trackers and compare main before publication. Next: Section9.17 chapter-wide answers and companion alignment.
