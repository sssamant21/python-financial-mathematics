# Section18.12 — Risk simulation: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `ade7da5b8c157c23f8b3be32c06af57add8602f4`; [source](../../chapter-18/18.12-risk-simulation.md). One workflow, forty local answers, twelve lab steps; no new historical unique methods.

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-risk-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-risk-review/review.py ade7da5b8c157c23f8b3be32c06af57add8602f4
```

Run from repository root. Baseline command intentionally exits1 and requires the git object. [Baseline](baseline.json) retains fourteen failed predicates; [corrected results](results.json) retains58 passing supplemental predicates and three passing exact-source commands: verbatim reference demo/twelve existing methods, quiet import and compile. Source/listing SHA256, actual stdout/stderr and Python/platform retained. Commands, supplemental predicates, answer/lab/workflow records and historical unique methods are separate. No observer correction needed.

## F184 — numerical/reporting correction; two explicit policies

Original ES overflows intermediate tail sums although a finite average exists, loses exact constant integer identity, and leaks TypeError/OverflowError for malformed or oversized inputs. Source now combines complete signed rational tail sums before reporting; inputs are finite int/float in finite float range, bool excluded, integers exact and floats interpreted as displayed decimals. Guarded nonzero reports reject overflow/underflow; exact whole-number ES and loss reports remain integers. Public finite predicate returns False on oversized inputs. Iterables are consumed once; a single empirical observation is allowed, not a basis for uncertainty acceptance. All twelve existing unittest methods unchanged and pass.

Two of fourteen baseline failed predicates establish explicit policies rather than retroactive promise violations. First, alpha.14,N50 now has exact displayed-decimal rankceil7=7, whereas binary multiplication produces7.000000000000001 and rank8 in the original. The earlier manuscript warned of boundary rounding; the extension now fixes its chosen decimal interpretation. Second, a mathematically positive ES below float report range is rejected instead of silently reporting zero. Neither policy certifies general software compatibility or sampling uncertainty.

## F185 — OPEN cross-section integration/design limit

Section18.11 deliberately retains negative terminal values implied by normal simple returns. This section's losses_from_values explicitly requires nonnegative terminal values and rejects them. The scalar loss definition itself remains valid for a signed terminal, and the empirical loss APIs accept signed losses, but the two reference interfaces are not automatically compatible for those paths. The existing rejection is retained and tested. No clipping, dropping paths or silently changing the upstream distribution was introduced. Reconcile a supported shared model/conversion contract before claiming an integrated normal-portfolio risk pipeline. This is an open integration/design finding, not a newly inferred financial-model defect; F32 also remains open.

## Independent expected values and execution boundaries

Exact execution comprises the whole reference fence per revision plus module commands. All extra source calls and rational quantile-integral calculations are supplemental. This deterministic source has no market sampler or seed, no unequal weights, backtest, bootstrap or risk-measure interval implementation.

At initial100, terminal[110,100,80,60] yields losses[-10,0,20,40]. Mean12.5, P(L>0)=.5. At alpha.75 rank3 gives VaR20 and the highest one observation gives ES40. At alpha.625 tail mass1.5 gives(40+.5×20)/1.5=100/3. At alpha.8 both VaR/ES40; P(L>VaR)=0 because of the atom at40. A99% tail with10000 equally weighted observations contains100 observation-equivalents, not a guarantee of precision.

The independent oracle integrates every sorted empirical quantile cell's overlap with[alpha,1], then divides by1−alpha. It differs from the implementation's full-tail/fractional-boundary algorithm. Tests cover ties, gains-only negative VaR/ES, constants, singleton, ordering, signed extremes, exact integer identity and the explicit decimal rank boundary. For finite losses ES is within their range; individually overflowing sums should not invalidate its finite average. Fraction is a shared arithmetic backend, so independent algebra is not arithmetic-library certification. Numeric comparisons use rtol1e-12,atol0 plus exact ranks/integers. No confidence/coverage or model-acceptance interpretation.

## Twelve lab-step contracts

Prerequisites: standard Python, save source as risk_simulation.py; equally weighted observations. Fixture is one hypothetical common-currency period with no external cash flows, no actual duration/market date/calibrated measure supplied. Positive loss=initial−terminal, strict loss excludes zero. Negative terminal inputs require the unresolved F185 integration decision; the fixture's terminals are all nonnegative.

| Step | Actual result / scope |
|---|---|
|1|Position100, sign, common hypothetical period/currency, levels.75/.625/.8 recorded. No RNG/seed exists in this deterministic source.|
|2|Source conversion100−[110,100,80,60]=[-10,0,20,40].|
|3|Sorted input and exact mean50/4=12.5; sorting invariance checked.|
|4|Source strict positive-loss frequency2/4=.5; zeros excluded.|
|5|VaR75 rankceil3=3, value20, independent quantile-cell reference.|
|6|ES75=40, full upper observation.|
|7|ES62.5=100/3, exact1.5 tail mass and half-weighted boundary20.|
|8|VaR80/ES80=40, strict exceedance0; discrete-mass interpretation reviewed.|
|9|Exact tail observation-equivalents100 atN10000,alpha.99; no10000-path simulation claimed.|
|10|Zero exceedances not proof of zero probability; conceptual sampling limit, no binomial interval implemented.|
|11|Twelve original methods plus invalid input/report probes run; baseline fourteen failures and corrected rerun retained.|
|12|Model/dependence/equal-weight/quantile/metadata/uncertainty limits retained, including F185; no independent acceptance.|

## Forty answer-alignment records

All forty prompts/answers read in order; conceptual rows are not additional callable tests.

| Answer | Disposition |
|---|---|
|1|Loss10, source initial100−90.|
|2|Loss−10 gain, source100−110.|
|3|Loss0, source100−100.|
|4|Positive-loss frequency.5, exact count/source.|
|5|Mean12.5, exact sum/4.|
|6|VaR75=20, lower empirical quantile.|
|7|ES75=40, integrated upper quantile.|
|8|Rank3, exact ceiling.|
|9|VaR80=40, empirical atom.|
|10|Strict exceedance above40=0, exact count.|
|11|Discrete atoms invalidate universal1−alpha exceedance equality, correct.|
|12|Tail mass1.5, exact4(1−.625).|
|13|ES100/3≈33.3333, independent overlap integral/source.|
|14|VaR is not maximum loss, correct definition.|
|15|ES not guaranteed maximum, correct.|
|16|N10000,alpha.99 tail mass100, exact arithmetic only.|
|17|Zero observed exceedances do not prove zero probability, correct.|
|18|More draws do not remove model misspecification, correct.|
|19|Loss=−P&L absent external cash-flow differences, correct sign contract.|
|20|One-day and ten-day VaR distinct, correct horizon requirement.|
|21|Square-root time scaling conditional, not universal.|
|22|Deterministic stress no inherent probability, correct.|
|23|Stress dependence can differ, correct model caution.|
|24|No liquidity model in source, inspected.|
|25|Unequal weights unsupported, inspected equal-cell method.|
|26|Zero excluded byL>0, source probe.|
|27|Alpha1 rejected, source.|
|28|Empty sample ValueError, source.|
|29|Nonfinite loss ValueError, source.|
|30|Sorting removes input-order dependence for VaR, source.|
|31|Constant ES5, source/oracle.|
|32|Negative VaR possible, gains-only oracle/source.|
|33|Negative ES possible, gains-only oracle/source.|
|34|Mean-SE formula not automatically quantile/ES SE, correct estimator distinction.|
|35|One example no model certification, correct.|
|36|Normal simple returns below−1 possible, correct; converter integration F185 explicitly open.|
|37|Clipping changes distribution, correct; no clipping introduced.|
|38|Measure defines modeled probability/valuation meaning, correct, uncalibrated fixture.|
|39|Boundary weighting averages exactly tail mass, independent cell-overlap reference.|
|40|Position/model/horizon/alpha/convention/results/limits retained. Seed/path provenance belongs to a stochastic caller, not fabricated here.|

## Resume

Next: **Section18.13 — Computational Performance**. Book1 remains in progress: twelve scoped Chapter18 workflows and480 local answers, not full acceptance. F28 notebook/platform, F32 shared-input integration, F165 tails and new F185 conversion integration remain open, along with risk-estimator uncertainty/calibration, broader input/branch, editorial/copyright and external independent acceptance.
