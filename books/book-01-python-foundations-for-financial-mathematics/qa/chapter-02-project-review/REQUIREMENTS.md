# Section 2.12 requirement review

These 24 derived review units map the project prose to evidence and limits. They are not a source-authored numbered checklist, test count or acceptance percentage.

| ID | Requirement | Disposition | Evidence / limit |
|---|---|---|---|
| P01 | Constant annual effective return, annual periods, nominal balances | REVIEWED_SPEC | Financial Model and Model Assumptions explicitly define a one-factor deterministic annual recurrence; not forecast probabilities. |
| P02 | End-of-year contribution timing | PASS_SCOPED | Source applies return then contribution; rational annuity benchmark checks terminal values. |
| P03 | Decimal raw-state comparison and display separation | PASS_SCOPED | Raw balance just below target remains not reached while stdout rounds to $100,000.00. |
| P04 | Shared positive finite initial amount | PARTIAL_TYPED_INPUT | Finite Decimal zero/negative/NaN fixtures reject; string principal raises AttributeError, F32. |
| P05 | Shared finite nonnegative contribution | PASS_SCOPED_TYPED | Negative/Infinity fixtures reject; zero contribution accepted; pretyped Decimal contract. |
| P06 | Shared positive finite target | PASS_SCOPED_TYPED | Zero/negative/NaN reject; equal initial target handled at year0; pretyped Decimal contract. |
| P07 | Non-Boolean whole horizon in 1..100 | PASS_SCOPED | True,0,-1,101,1.5 reject;1 and100 valid. |
| P08 | Scenario representation before Decimal methods | PASS_SCOPED | None/string/float/bool rejected with reasons; Decimal zero evaluated. |
| P09 | Scenario finiteness before domain | PASS_SCOPED | NaN,sNaN,Infinity,-Infinity rejected before ordering comparisons. |
| P10 | Return strictly above -100% | PASS_SCOPED | Exactly -1 and below rejected; -.999999 accepted. |
| P11 | Independent state per scenario | PASS_SCOPED | Reversed scenario order matches rational expected values; duplicate scenarios retain separate results. |
| P12 | Period0 before updates | PASS_SCOPED | Already-funded target reports year0 and unchanged initial balance. |
| P13 | Finite inclusive horizon | PASS_SCOPED | Final-year equality reaches; tiny final miss does not;100-year fixture bounded. |
| P14 | Break at first crossing | PASS_SCOPED | Earliest year compared to exact Fraction closed form; stopping balance checked. |
| P15 | Explicit rejection before continue | PASS_SCOPED | One recorded reason/disposition per rejected scenario; accepted/rejected counts reconcile. |
| P16 | Outcome classification and named threshold | PASS_SCOPED | Year0, equal10,after10,and not-reached classifications checked. |
| P17 | Stored accepted/rejected results | PASS_SCOPED | Result/rejection lengths reconcile to counters in every valid fixture, including empty scenarios. |
| P18 | Four reconciliation identities | PASS_SCOPED | Scenario totals, outcome totals and both stored lengths checked independently; source assertions retained. |
| P19 | Explainable console report | PASS_SCOPED | Actual stdout retained per case; validation and rejection messages checked; handled validation retains source exit-zero behavior. |
| P20 | Earliest scenario and ties semantics | REVIEWED_DESIGN_SCOPE | Section2.12 advises explicit tie policy but does not compute an earliest ranking. It reports each scenario; tie-aware ranking is supplied in the Exercise45/59 supplement, not attributed to the exact project. |
| P21 | Educational exclusions and no recommendation | REVIEWED_SPEC | Taxes/fees/withdrawals/inflation/stochastic returns excluded; scenario versus forecast and no-best-investment cautions stated. |
| P22 | External text conversion and arbitrary shared types | OPEN_INTEGRATION | Source initializes shared Decimal literals; no complete external-input parser/type guard is provided. F32 remains open. |
| P23 | Numerical/context/resource bounds | OPEN_BROADER_REVIEW | Default Decimal context, extreme rates/magnitudes and resource limits are not fully specified or certified by these fixtures. |
| P24 | Platform and independent model acceptance | OPEN_BROADER_REVIEW | Executed Linux CPython3.12.14 only; no independent financial/model review or Windows/macOS execution claimed. |
