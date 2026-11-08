# Section18.7 — Scenario analysis: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `312497c76e305beccddcd91b1dffb5d667e7c806`; [source](../../chapter-18/18.07-scenario-analysis.md). One workflow, forty local answers, twelve lab steps. No new historical unique methods.

From the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-scenarios-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-scenarios-review/review.py 312497c76e305beccddcd91b1dffb5d667e7c806
```

The baseline command intentionally exits1 and requires that git object. [Baseline](baseline.json) retains21 failed supplemental predicates; [corrected results](results.json) retains69 passing predicates and three passing exact-source commands: entire verbatim reference demo/ten existing methods, quiet import and compile. Source/listing SHA256, full command outputs, CPython3.12.14/Linux and source scenario outputs are retained. Commands, supplemental predicates, answers, workflow/step records and historical unique methods are separate inventories. No observer correction was needed in this batch; the18.6 observer transition stays in its own evidence.

## Finding F179 and contract clarification

Original binary arithmetic loses initial/terminal integer identity and rounds a±1 currency P&L on a1e18 exposure with±1e-18 return to zero. That also misclassifies a true modeled loss in weighted_summary. Nonzero scenario and weighted outcomes can silently underflow. The finite predicate and huge numeric inputs leak OverflowError; noniterable inputs leak TypeError, and missing result keys leak KeyError.

Source now uses displayed-decimal float/exact integer arithmetic, guarded finite input/report range, exact whole-number reports and ValueError for invalid/unreportable values, computing P&L before rounding its reports. The public finite predicate returns False on oversized/invalid inputs. Fully funded nonnegative exposures, returns≥−1 and nonnegative terminal fee remain enforced; zero exposure total is allowed because no portfolio-return ratio is computed. All original ten unittest methods remain unchanged and pass.

**Two of21 failed baseline predicates establish a new explicit normalization policy:** probabilities already accepted within the1e-12 sum tolerance are normalized to exactly1 internally. The original code could return all-loss probability1+5e-13 or biased constant expectation100(1−5e-13). Rather than call the prior unstated normalization choice a universal defect, the source documents this extension and the displayed-decimal tolerance boundary. Arbitrary probabilities are not accepted as calibrated market likelihoods.

Common baseline, horizon, units and P&L reconciliation remain external prerequisites, as the original source stated. The observer deliberately demonstrates that inconsistent baseline metadata is **not rejected** by weighted_summary. This is a recorded design limit, not an acceptance pass or closed integration gap. Every row still needs finite terminal/P&L fields, even at zero weight. No baseline/horizon metadata schema, overlapping-scenario correction, Monte Carlo sampler or instrument-pricing API was added.

## Independent arithmetic and scope

Exact execution is the complete reference fence per revision plus its commands. Supplemental source calls check additional cases; independent Fraction formulas provide expectations. For exposures60/40:

| Case | A terminal | B terminal | Portfolio terminal | P&L |
|---|---:|---:|---:|---:|
| Base |63|40.8|103.8|3.8|
| Downside |48|36|84|−16|
| Upside |69|43.2|112.2|12.2|

Weighted probabilities1/2,3/10,1/5 give expected terminal4977/50=99.54, expected P&L−23/50=−.46, and strict loss probability3/10. The observer compares each source row and weighted field against these independently derived numbers. A1pp A-return shock gives60/100=.6;1bp gives60/10000=.006. Sequential+10%,−10% gives−1%, not0.

Separate **supplemental** instrument examples, not source exports: a one-year annual-effective zero-coupon price at5% is2000/21≈95.2381 and at6% is5000/53≈94.3396. Revaluation P&L is−1000/1113≈−.8985; printed rounding is checked. EUR100 times1.10USD/EUR givesUSD110; at1.05 givesUSD105 and P&L−USD5. No market data, yield curve/day-count/calibration or FX quotation inversion API executed.

Arithmetic predicates use rtol1e-12,atol0 or exact integer/normalized-probability equality. They are not statistical confidence bands. The source is deterministic: discussion of Monte Carlo, correlations and rare events is conceptual/design review, not execution of a scenario sampler or independent acceptance of the assigned probabilities.

## Twelve lab-step contracts

Prerequisites: Python standard library; save reference as scenario_analysis.py; positions are fully funded exposures in one common fictional currency, held fixed for a common portfolio period, no rebalancing, taxes or additional cash flows. Baseline model has no actual market valuation date/dataset and does not specify a duration for the portfolio period; execution date is not a fabricated valuation date. The separate bond example explicitly has a one-year horizon. Those omissions are acceptable for this fictional arithmetic fixture but must be supplied for real use.

| Step | Review and actual evidence |
|---|---|
| 1 | Positions60/40 and common currency/period conventions recorded. No actual valuation date or market-input source supplied; limitation retained rather than invented. |
| 2 | Independent baseline100; source baseline compared in all three cases. |
| 3 | Independent table above versus actual source terminal/P&L for base/down/up. |
| 4 | Source A-return sensitivity at1pp=.6 and1bp=.006; B held at zero return. |
| 5 | Fee2 paid once at period end gives zero-shock P&L−2; source test/probe. No time-zero-fee convention inferred. |
| 6 | Illustrative probabilities.5/.3/.2 sum exactly1 in rational arithmetic; source validation/normalization policy tested. |
| 7 | Source weighted expected terminal99.54 and P&L−.46 versus independent sums. |
| 8 | Strictly negative P&L selects only downside: probability.3. Zero P&L and zero-weight losses separately checked; tiny loss classification preserved after fix. |
| 9 | Independently recalculated simplified bond prices and P&L using Fraction; not a callable source valuation implementation. |
| 10 | Explicit USD/EUR direction and EUR100 unchanged exposure; independent multiply/P&L checks. Not a live FX or source conversion API. |
| 11 | Ten existing methods, invalid-input/output probes, quiet import/compile pass;21 baseline failures and corrected rerun retained. |
| 12 | Source hashes, commands, versions, assumptions, external baseline/horizon dependencies and result records retained. Model probabilities/dependence and external acceptance remain open. |

## Forty local prompt-to-answer alignment records

Every source prompt/answer read in order. Conceptual statements below are reviewed without inventing runtime APIs.

| Answer | Scoped disposition |
|---|---|
|1|Baseline100, exact exposure sum/source field.|
|2|Base A63,60×1.05.|
|3|Base B40.8,40×1.02.|
|4|Base terminal103.8, independent component sum versus source.|
|5|Base P&L3.8, terminal minus100/source.|
|6|Down A48,60×.8.|
|7|Down B36,40×.9.|
|8|Down P&L−16, source versus84−100.|
|9|Up terminal112.2, independent60×1.15+40×1.08/source.|
|10|Up P&L12.2, independent terminal minus100/source.|
|11|A1pp sensitivity+.6, source/source-oracle.|
|12|A1bp sensitivity+.006, source/source-oracle.|
|13|100bp=.01 decimal, exact units.|
|14|Sequential+10%,−10% cumulative−1%, exact fractions.|
|15|.5+.3+.2=1, exact fractions.|
|16|Weighted terminal99.54, source versus independent weighted table.|
|17|Weighted P&L−.46, source versus weighted table.|
|18|Strict-loss probability.3, source versus downside weight.|
|19|Unweighted stress no automatic probability, correct scenario distinction.|
|20|Overlap must be accounted for, correct probability requirement; source cannot detect overlapping definitions.|
|21|End fee2/zero shocks gives P&L−2, source.|
|22|Zero shocks/no fee gives P&L0, source.|
|23|Bond5% price95.2381, separate exact rational calculation/rounding.|
|24|Bond6% price94.3396, separate rational calculation/rounding.|
|25|+100bp bond P&L−.8985, exact revaluation difference/rounding.|
|26|FX baselineUSD110, explicit units and exact arithmetic.|
|27|FX shockUSD105, explicit units and exact arithmetic.|
|28|FX P&L−USD5, independent subtraction.|
|29|Quote direction determines multiply/divide, correct dimensional requirement.|
|30|Joint scenario alone establishes no frequency, correct conditional-model distinction.|
|31|Correlation does not prove causation, correct conceptual limit.|
|32|Zero observed loss does not prove zero probability, correct statistical limit; no source sampler or rare-event interval.|
|33|More paths do not remove bias, correct model distinction.|
|34|Nonlinear assets may need full revaluation, correct sensitivity limit; source linear fully funded model only.|
|35|Horizon needed for consistent period, correct prerequisite; no actual portfolio-period duration is supplied by this fixture.|
|36|Return−1 yields terminal0 for100 asset, source case.|
|37|Below−1 rejected, source domain/test.|
|38|Baseline reconciliation ensures comparable positions/values, correct external contract; weighted function intentionally does not enforce it.|
|39|Weighted expectation is model-dependent, correct; assigned probabilities are illustrative.|
|40|Positions/shocks/units/assumptions/version/outputs/limits are required records; scoped fixture evidence supplied, real-world provenance/acceptance still needed.|

## Remaining scope / resume

Next: **Section18.8 — Monte Carlo Estimation**. Chapter18 now has seven scoped workflows and280 local answers. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, scenario metadata consistency/dependence/calibration, broader branch/input and financial model/editorial/copyright/external independent acceptance remain open. No certification, production or external messaging action.
