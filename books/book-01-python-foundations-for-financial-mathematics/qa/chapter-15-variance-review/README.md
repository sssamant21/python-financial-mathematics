# Section 15.3 — scoped variance lab and worked-answer review

Baseline source revision: `3b2c1f184be47b19b6e9f96f873b241ef6f8cef0`. One core workflow, twenty-four local prompt/answer records and one ten-task project reviewed. Counts of workflows, exercises, project tasks, predicates and historical methods are distinct.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-variance-review/review.py
```

The runner extracts the exact single Python fence into an isolated directory, runs the printed demonstration and twelve existing unittest methods, imports it without demonstration side effects, and runs the printed compile command. Three commands pass. The supplemental observer imports that same code and evaluates 47 predicates, all passing. No historical unique methods added. Raw outputs, runtime/platform and manuscript/listing hashes are in `results.json`; the project assembly is supplemental, not a previously published report generator.

## Retained failures and corrections

`observer-initial.json` retains the first run, including a QA-observer mistake: stress variance was transcribed as 31/7500. Re-derivation gives (225+2025+9025+1225)/1000000/3 = 1/240. The runner was corrected and rerun against unchanged manuscript source; `baseline.json` retains this corrected-observer baseline with twelve failed predicates. The observer mistake is not a manuscript defect. The baseline is reproducible by running this observer against the manuscript at the revision above; `observer-initial.json` differs only in that original reference. All twelve original unit methods passed on the baseline.

F129 corrects a nonzero residual on constant observations (three separate predicates, not three distinct defects), integer precision lost before centering, premature sum/square overflow, squared underflow before downside square root, covariance-bound overflow, absolute covariance tolerance admitting infeasible matrices and negative variance, unreported infinite annualization, and raw `OverflowError` for unreportable moments. Exact rational intermediate arithmetic follows the documented displayed-decimal float interpretation. Square roots use 80-digit Decimal arithmetic before float reporting. Infeasible covariance is rejected without a scale-independent tolerance. All required report fields must be representable as finite floats, with nonzero outputs not rounded to zero; otherwise ValueError is deliberate. These routines are educational, not a throughput or binary-float compatibility guarantee.

## Independent numerical expectations and local prompt alignment

The independent centered-sum benchmark uses the pairwise identity Σ(x−mean)² = Σ(i<j)(xi−xj)²/n, with rational inputs. It gives .001; divide by 4 or 3 for population or sample. Square-root expectations use Decimal at 80 digits. Tests compare source results to independently derived rational/Decimal values with recorded tolerances. Metamorphic transformation checks are identified separately from independent calculations.

| Prompts | Reviewed answer and evidence |
|---|---|
| 1–4 | Sum .04 / 4 = .01; deviations .01,−.02,.02,−.01; squares .0001,.0004,.0004,.0001; total .001. Deviations/squares are an independent derivation, not source-exposed output fields. |
| 5–8 | Population .00025, sample 1/3000; square roots ≈.0158113883 and .0182574186, reported SD in pp after ×100. |
| 9–11 | Constant variance exactly zero; singleton population zero and sample rejected; two-point sample variance .0002. |
| 12–14 | Shift invariance and scaling checked against rational benchmarks; doubled variance factor 4 and SD factor 2 follow the formula. Percent-unit variance 10/3 versus decimal 1/3000 verifies the factor 100², not 100. |
| 15–16 | All-n zero-threshold downside .005; only one squared shortfall .0001 contributes. Ordinary SD centers all observations. Conceptual distinction reviewed. |
| 17–18 | .01√252≈.158745; correlated-return variance adds twice the autocovariance, so a universal √T forecast claim is invalid. The source scaling call is executed; assumptions and correlated counterexample are mathematical/design review, not data estimation. |
| 19–22 | Portfolio variance 13/400, SD √(13/400); covariance ±.06 is feasible, giving variance 1/16 and 1/400, hence SD .25 and .05. Exact boundary validation and small-scale infeasibility tested. |
| 23–24 | Outlier population variance .0012 = 12 squared pp; n=4 summary does not provide forecast confidence. The numerical calculation is executed; adequacy/uncertainty is conceptual review. |

## Lab/project step contracts and prerequisites

The source uses only standard-library modules, with Python sequence/functions, return units and the previous statistics sections as prerequisites. Inputs reject booleans, missing/nonfinite observations, invalid ddof, thresholds and annualization factors. No feed, market prices or platform-specific notebook is used.

| Task | Executed result or scoped review |
|---|---|
| 1 | Input copied unchanged; source synthetic, hypothetical daily, units decimal simple returns. Manuscript now explicitly leaves dates unspecified; price/corporate-action evidence is unavailable. |
| 2 | Source mean .01, population variance .00025 and sample variance 1/3000 recorded. |
| 3 | Source population/sample SD recorded; unit conversion explained above. |
| 4 | Source downside .005, zero threshold, all-n denominator. |
| 5 | Manuscript now specifies 252 days and uncorrelated equal-variance assumptions; source annualized sample SD √.084≈.2898275 recorded. Actual financial dependence is not tested. |
| 6 | Manuscript now fixes stress .03→.13. Source stressed sample variance 1/240 recorded, versus 1/3000 baseline (12.5×). No silent replacement of original fixture. |
| 7 | Manuscript now fixes weights/variances/covariance as in the worked portfolio; source result .0325 recorded. Bound checked mathematically, including exact ±.06 cases. |
| 8 | Formulas above, Python version, fixture SHA-256 and source/listing hashes retained; corrected revision is the containing Git commit. |
| 9 | Four observations do not establish stationarity, tail adequacy, confidence intervals or forecast validity; conceptual review only. |
| 10 | Runnable observer, original failures and corrected report retained here for broader QA. |

The executable project report is a supplemental assembly of source calls and metadata. The manuscript tasks do not supply a complete separate lab script. Its unspecified stress, annualization factor, portfolio inputs and metadata were clarified to make acceptance reproducible. The source commands and existing tests are exact-source executions; the rational oracle, stress assembly, metadata/hash and design records are supplemental.

## Limits and checkpoint

Scoped local Linux CPython validation only. No independent reviewer acceptance, Windows/macOS/notebook execution, real-data provenance/integration, performance benchmarking, exhaustive branch coverage or certification. F28 notebook/platform, F32 shared-input integration and other unresolved findings remain open. Next: Section 15.4, Skewness and Kurtosis. Chapter 15 now has three reviewed workflows and 72 local answer records; those are not unique test methods.
