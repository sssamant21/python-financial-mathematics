# V272 — Section10.9 fixed assessment/report/units/lab crosswalk

Pin: `bf827d7f8351c0d99cfe5760540964dd31fbbe0b`. [Observer](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](corrected.json), [replay](replay.json), [crosswalk](crosswalk.json), [chapter runner](native-runtime.txt), [chapter results](chapter-runtime.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-assessment-2026-11-23/review.txt baseline baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-assessment-2026-11-23/review.txt baseline baseline-replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-assessment-2026-11-23/review.txt candidate corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-assessment-2026-11-23/review.txt candidate replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-engine-assessment-2026-11-23/native-runtime.txt
```

Baseline/replay **36 pass /14 fail**. All fourteen failures are missing report/metadata/refinement contracts;the existing fixed-scenario numerical checks pass. They are not fourteen numerical defects. Corrected **50 predicates pass twice**,identical rows and complete assessment reports. Four final native CLI/compile commands pass. EarlierV264–271 range failures,policy decisions,observer transitions and scope remain retained. All financial helper bytes before assessment() match the pinned source exactly;the hash in crosswalk.json supports source-identity reuse,not a claim that all previous external observers were rerun.

## Independent fixed-model references

The oracle integrates the degree40 Taylor polynomial of exp(u*t+v*t²),multiplied by a+b*t or its time-weighted moments,using exact rational coefficients of validated binary inputs. This differs from the source scaled-exponential/combined antiderivative formulas. For the selected fixed models,|u|T+|v|T²<.3 and exp(abs exponent)<2;the integrated tail bound is2*T^(m+1)*(|a|+|b|T)*z^41/41!,less than1e−55. A separate rational exponential series values the dated500 payment. Full rational references/tail bounds are retained,not shared source formula outputs.

For each flat/affine continuous stream at n256/512,a fourth-derivative polynomial recurrence yields a conservative Simpson bound T*h^4*M4/180. Native errors satisfy that bound plus a declared2e−10 currency floating allowance. Component/total/analytic report fields match the independent integrals. This is evidence for the specified deterministic scenario,not all cash-flow models or universal floating error certification.

The flat sensitivity reference is the independent negative time-weighted integral plus the dated-payment derivative. Its accuracy predicate combines a central-difference third-derivative truncation bound,a Simpson contribution and a declared2e−9 currency allowance per valuation. Observed error is about.000144158 currency*years against a combined bound about.000164266. The explicit floating allowance is not a proved platform-wide rounding bound.

## Report and manuscript fixes

The manuscript promised resolution,bump,tolerance,assumptions and affine refinement evidence but the baseline JSON omitted them. assessment() now records512 panels,an explicit1bp bump used in the call,derivative units,currency reconciliation tolerance1e−6 and its local result,model assumptions and the discrete-date policy. Affine256/512 totals,difference and difference/15 are recorded with error_estimate_certified=False. Report composition checks are distinct from independent numerical accuracy. The default affine difference is about1.76442e−10 and the heuristic fine-error estimate about1.17628e−11;neither is labelled a universal proof.

T bounds continuous streams only;all supplied nonnegative discrete dates are valued even if outside T. A native zero-continuous-horizon/future-payment check makes this explicit. The prose now describes companion dependencies and complete linear PV arithmetic accurately;escaped command/code fences are repaired. Selected runtime evidence is checked off separately from the pending full pinned refresh,independent review and canonical approval.

| Exercises | Disposition |
|---|---|
|1–4|Continuous/discrete definitions and flat/affine discount references verified for the fixed model;deterministic-year-fraction assumptions explicit.|
|5–8|Zero-rate/growth-rate identities checked;time-zero identity retained fromV271.|
|9|Positive even Simpson constraint retained/native check.|
|10–11|Currency*years derivative units and explicit.0001 annual-rate bump now reported.|
|12|Independent component/discrete reconciliation.|
|13|Heuristic refinement separated from the independent fixed-model bounds.|
|14|Production calibration,controls,independent model/code review and operational acceptance remain external;no such operations performed.|

The specified lab scenario,fourteen worked answers and acceptance categories are crosswalked without new global answer/workflow or completion percentages. Functional limits fromV264–271,subclass/stateful-model boundaries,finite report fields,precision/cutoffs,resource budgets and quadrature assumptions remain. The JSON keeps runtime_certified=False and independent_review_completed=False.

Chapter10 compiles21 files and passes11 checkers/10 CLIs with before/after source hashes verified. Fresh inventory remains642 Python files/429 check-test scripts/643 required blobs. Five executable blobs differ fromV263;this is a scoped chapter run. Next:V273 full pinned accumulated-code runtime refresh before advancing to10.10. All38 COV categories remain partial,none closed;no supported-platform,independent reviewer,release or canonical acceptance. Book1 tracked separately.
