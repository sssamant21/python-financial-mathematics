# V256 — Section10.7 finance/report/error-assumption crosswalk

Source pin: `8e2cd8aee2f7497e8da34be3f86c22ce28da3c85`. [Runnable observer](review.txt), [first](first.json), [replay](replay.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-finance-oracle-2026-11-22/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-finance-oracle-2026-11-22/review.txt replay
```

**92 predicates pass twice**, identical rows and full native report. No source failure/change. Native CLI and compilation execute in each run (four command records); direct source assessment, integration and refinement calls are distinct from the independent oracle. Prior V253–255 numerical/policy failures, observer records, corrected56/78/65 predicates, callback/resource/precision limits and original polynomial-order evidence retain their scopes.

## Independent financial integral

For exact manuscript a=3/100,b=1/400,T=4, expand exp(−at)exp(−bt²), multiply by1000+100t and integrate each monomial exactly. The double truncation j,k<=40 is a rational number, not a higher-resolution quadrature or shared Simpson reference. Uniform product-Taylor remainder is bounded by
`11200[(.12)^(N+1)+(.04)^(N+1)]/(N+1)!`, using exp(.16)<2 and integral weight<=5600. N40 tail<1e−80; N30/40 exact results agree within their independent tail bounds. The integral is approximately **4445.5787257519998132758835692750867 currency units**. Full rational reference/remainder and100-digit decimal are retained.

The source callback uses floating constants/math.exp rather than exact symbolic parameters. An explicit2e−10 allowance covers selected callback/report differences; it is a tested allowance, not a proven global floating-error certificate. With q=.03+.005t, t in[0,4], |second derivative of f|<=20.5 and |fourth derivative of f|<=.56875 are conservative derivative bounds. These give standard midpoint/trapezoid/Simpson truncation bounds under the displayed smooth deterministic model;15 report estimates satisfy those bounds plus the explicit allowance and oracle remainder. All five resolutions for each method show decreasing observed error against the independent reference. Every global/row/schema/count/finite/estimator field is accounted for; certification/reviewer flags remainFalse.

The derivative bounds follow explicitly from c=1000+100t, q=.03+.005t, e=exp(−.03t−.0025t²):

- f2=e[−200q+c(q²−.005)], so |f2|<=200(.05)+1400(.05²+.005)=20.5.
- f4=e[400(−q³+.015q)+c(q⁴−.03q²+.000075)], so |f4|<=400(.05³+.015*.05)+1400(.05⁴+.03*.05²+.000075)=.56875.

Here e<=1,c<=1400,0.03<=q<=0.05 on[0,4]. Composite bounds are4h²|f2|/24 for midpoint,/12 for trapezoid,and4h⁴|f4|/180 for Simpson;the separate rounding allowance is added only in the numerical predicates.

| Predicate group | Scope |
|---|---|
|2 | Exact series truncation agreement and reference remainder. |
|6 | Complete global report schema,model label,horizon,method names and two false acceptance flags. |
|78 | Three method row counts,each of15 row schemas/n/finite estimates/independent error bounds,12 complete Decimal estimator comparisons and three selected decreasing-error observations. |
|2 | Applied high-resolution midpoint8192 has its own analytical second-order bound; Simpson128 and midpoint8192 agree within1e−6. This required cross-rule comparison is separately labelled and does not replace the series oracle. |
|4 | Smooth polynomial alias counterexample: exact dyadic roots at both n2/n4 midpoint nodes give native0/0 and estimated error0, while exact integrated polynomial scaled integral=1. |

The alias polynomial is a product of squared linear factors, so it is smooth and nonnegative. Exact monomial integration and dyadic sample roots establish the counterexample without sin/cos rounding. Smoothness alone does not place these particular grids in an asymptotic regime or make their agreement an accuracy proof.

## All14 exercise and applied-lab dispositions

| Exercises | Disposition |
|---|---|
|1–3 | Native midpoint/endpoint/Simpson weights and even-panel validation covered by original checks and retained weighted/grid batches; formulas are mathematical identities in exact arithmetic. |
|4–8 | Prior exact polynomial signed-error/order tests rerun in the full source runtime; t² integral1/3, midpoint.3125/trapezoid.375/Simpson1/3, affine exactness qualified by numerical reporting. No new answer counts. |
|9–11 | C4 and asymptotic leading-error assumptions distinguish fourth-order/halving16 from a universal guarantee; prior signed polynomial and exp(x) selected-ratio tests retained. |
|12 | Integral of rate.03+.005t is.03t+.0025t²; discount factorexp(−that). Units: cash-flow currency/year,rate1/year,slope1/year²,t years,PV currency. No market curve/calibration provenance supplied. |
|13 | Oriented bounds sign verified in prior grid/native regressions; closed-form orientation reviewed. |
|14 | New exact smooth alias demonstrates shared-grid agreement does not prove accuracy. |

Applied lab: all three fixed methods/resolutions,complete refinement reports,independent finance reference,required high-resolution midpoint comparison and original polynomial/failure cases are recorded. Known singularities/discontinuities require splitting; finite-domain quadrature does not certify infinite tails. Truncation bounds assume the displayed deterministic smooth integrand,not noisy/discontinuous feeds. MAX_PANELS100000,MAX_REFINEMENTS32,snapshotted finite counts,represented-grid preflight and final underflow/error policies remain declared limits,not performance/callback-time or arbitrary-resource guarantees. No new native provenance fields, calibration or valuation approval.

**Checkpoint:** Selected10.7 source/report/proof/14-exercise/applied-lab crosswalk recorded. Next V257 full pinned runtime refresh and unchanged executable-identity verification before10.8. Book2 remains IN PROGRESS; all38 selected COV categories partial,none closed,not defect counts/percentages. Independent/platform/model/data/resource/release/canonical gates remain open. Book1 separate.
