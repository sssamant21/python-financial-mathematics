# Section 15.9 — scoped hypothesis-testing lab and answer review

Baseline manuscript revision: `30f6c8ebee9d34035cdb81cd740f01141163887a`. One core workflow, 24 local answer records and one ten-task project reviewed. These counts remain distinct from predicates and historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-15-hypothesis-review/review.py
```

The observer extracts the single Python fence unchanged into isolation, runs the printed demonstration and twelve existing unittest methods, imports silently and runs the printed compilation command. Three commands and 35 supplemental predicates pass. No historical unique methods added. It additionally imports the exact Section 15.8 source fence and makes one t-interval call; this is an additional source integration call, not another core workflow or rerun of that section's twelve tests. Both source/listing hashes are retained in `results.json`, along with runtime/platform, command output and expectations/tolerances.

`observer-initial.py` and `observer-initial.json` retain an observer-only failure: multiplying Fraction by Decimal while constructing a cost-hurdle expected value. The expectation was changed to Decimal('1.5') times the Decimal root. This was corrected before any manuscript change; `baseline.json` is the corrected-observer run against unchanged baseline source. Nine failed predicates are retained. All twelve original source methods and printed commands already passed on baseline. The observer error is not a manuscript defect.

F135 corrects integer spread and sign counts lost by float coercion, tiny/huge t ratios failing before scale cancellation, decimal constant samples treated as variable, premature sign-tail underflow (including a reportable final two-sided probability), and unreportable positive probabilities silently reported as zero. Exact rational intermediate arithmetic follows displayed-decimal float inputs; roots use 80-digit Decimal. Final nonzero unreportable t/sign outputs raise ValueError. Normal tail p-values use erfc and reject underflow to zero; the ordinary CDF may still round to 0 or 1 at extreme arguments and must not be subtracted to reconstruct tails. Educational policy only, not performance or binary-float compatibility certification. Exercise 23's post-selection scenario was relabeled to distinguish it from temporal look-ahead leakage.

## Independent numerical derivation and local answers

For [.01,.02,.03], mean=.02, sample variance=.0001, SE=√(1/30000), and t=√12=2√3. Scale-free t expectations follow these rational quantities, not another implementation of source centering. Normal p(1.96) is independently derived by integrating exp(−u²/2) term-by-term in an 80-digit Decimal power series with a recorded π constant; the oracle does not call erfc or a normal CDF. Thirty-two enumerated sign outcomes give two extreme outcomes for five positive signs, p=2/32=1/16.

For df=2, the t CDF is F₂(t)=1/2+t/[2√(t²+2)], so the observed two-sided p is 1−√(6/7)=.07417990022744854. This executable closed-form distribution calculation is supplemental: the Section 15.9 source intentionally supplies a t statistic but no general Student-t CDF. Passing that statistic to the normal p function would be a different, inappropriate reference model here. The exact Section 15.8 source t interval is [−.004841377118437528,.044841377118437525], consistent with not rejecting zero at alpha=.05.

| Prompts | Review, expectation and scope |
|---|---|
| 1–4 | H0 mean zero, two-sided alternative, optional positive one-sided alternative chosen before data and nominal Type I level reviewed. Project now fixes two-sided alpha=.05. |
| 5–9 | Mean .02, SD .01, SE √(1/30000), source t=√12 and df=2 checked/derived. Source returns t, not mean/SD/SE fields. |
| 10–12 | Student-t reference required under iid normal model; source normal p(0)=1 and p(1.96)≈.04999579 checked against independent series integration. No small-sample t p-value claimed from the normal function. |
| 13–15 | Exact source decision branches and p=alpha boundary verified. Failure to reject is not proof of H0. |
| 16–18 | False positive, false negative and power=1−beta definitions reviewed conceptually under specified models; no power study or Type I calibration simulation. |
| 19 | Hypothetical cost hurdle .005 reduces estimated mean excess to .015; source t against that hurdle =1.5√3. Economic adequacy and deployment remain unaccepted. |
| 20–21 | Source p=.0625 for five positive signs, p=.25 for [0,1,2,3] after dropping the tie; exhaustive five-sign outcome check retained. |
| 22 | Twenty true nulls at .05 have expected false count one by linearity of expectation; independence affects the count distribution, not its mean. Mathematical review, not a family-wise-error acceptance. |
| 23 | Selecting test after viewing return signs is post-selection/data-snooping bias, distinct from future information leakage. Prompt and answer now aligned. |
| 24 | Autocorrelation can invalidate iid t calibration; dependence-aware inference is a conceptual requirement, not executed here. |

The exact sign test now forms its two-sided rational probability before float conversion. For 1075 positive signs, p=2^−1074 is reportable (minimum positive subnormal); baseline underflowed the one-sided half first and falsely returned zero. For 2000 positives the two-sided probability itself is unreportable and is explicitly rejected. These two cases distinguish intermediate arithmetic defects from output-range limits.

## Project step and prerequisite contracts

| Task | Executed result and limit |
|---|---|
| 1 | Synthetic daily simple returns and labels 1–3; real dates/calendar unspecified. Hypothetical iid population, H0 mean zero. |
| 2 | Two-sided alternative and alpha=.05 now predeclared. This review cannot establish an actual historical preregistration process. |
| 3 | Independent means/SD/SE/df plus source t retained. |
| 4 | Supplemental documented df=2 closed-form CDF evaluated, p≈.07418. No generic SciPy t runtime or general-df CDF tested/claimed. |
| 5 | One exact Section 15.8 t-CI call with the same return fixture and model; interval contains zero and source decision at proper t p does not reject. This one integration fixture does not close F32. |
| 6 | Separate generic positive-sign diagnostic [1,2,3,4,5], source p=.0625 and decision does not reject. Magnitudes are not claimed as real daily returns. |
| 7 | Type I/II/power definitions reviewed; no power calibration or inference validity certified. |
| 8 | Explicit hypothetical .005 per-period return hurdle, .015 mean excess and source threshold t retained. No actual fees/slippage/risk constraints provided. |
| 9 | Data snooping, point-in-time universe, dependence and future leakage risks reviewed conceptually; no feed or actual strategy research process audited. |
| 10 | Inputs, fixture hash, source/listing hashes for both sections, runtime, null, alternative, alpha and generated results retained. Corrected revision is the containing commit. |

Prerequisites: Python functions/sequences, sample moments/SE, Section 15.8 CI conventions and iid normal assumptions for t inference. Source uses the standard library only. The project report and df=2 distribution calculation are supplemental assemblies, not a complete previously published lab program. Exact source commands/tests, one cross-section CI call, independent mathematical expectations and conceptual model/economic review remain distinct.

## Limits and resume checkpoint

Scoped local Linux CPython only. F28 notebook/platform, F32 broader shared-input integration and other unresolved findings remain open. No independent reviewer acceptance, real-data calibration, generic Student-t library acceptance, external platform run, exhaustive branch coverage or certification. Chapter 15 now records nine workflows and 216 local answer records reviewed. Next: Section 15.10 — Linear Regression.
