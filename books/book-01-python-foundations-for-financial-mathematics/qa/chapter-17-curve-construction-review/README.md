# Section 17.10 — scoped curve-construction concepts review

Affected baseline: `bec5525056393e537ce1338c667f93682b97fc78`. F167, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers; decision repair discount/log/bootstrap/cashflow range and input/reporting contracts. Reviewer: automated execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow,40 local answers,twelve lab steps and twelve separate acceptance-control records are distinguished from four exact-source commands,43 supplemental predicates and twelve existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains runtime/platform/SciPy, raw stdout/stderr, actual values/tolerances, model and source/listing SHA256.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-curve-construction-review/review.py
```

Reproduce unchanged-source baseline (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-curve-construction-review/review.py bec5525056393e537ce1338c667f93682b97fc78
```

[baseline.json](baseline.json) retains16 failed predicates under the final observer; original twelve methods and exact SciPy example already passed. Numeric defects include lost integer cashflow/bootstrap differences, intermediate signed accumulation/denominator overflow, discount underflow before multiplication by a large cashflow, overflowed opposite log-node products that should cancel, forward-ratio loss/overflow and silently zero/infinite public reports. Malformed-input exceptions are standardized. Explicit reusable-list/tuple cashflow policy is a contract addition: generators originally worked in some cases, while an empty generator could silently price as0. This scoped policy does not resolve F32's broad shared-input integration gap. Sixteen failed predicates are not16 distinct defects. No observer failures occurred.

## Exact execution and independent equations

Four isolated commands execute the verbatim demonstration/twelve tests, silent import, compilation and printed SciPy brentq bootstrap snippet. A separate unchanged-snippet execution in a namespace supports two independent bootstrap/repricing predicates, with stdout retained. No supplemental curve bootstrapper substitutes for source execution.

Fictional one-year zero bond: face100,price95 implies D1=19/20. Fictional two-year annual coupon bond: face100,coupon5,price100 implies D2=(100−5*19/20)/105=127/140. Independent repricing5*19/20+105*127/140=100. The returned floating discounts are checked with recorded tolerances; a separate source API chain converts DFs to continuous zero nodes and prices the cashflow list, with absolute1e−12 currency tolerance. This local roundtrip is not a multi-instrument/general bootstrap or exact floating transcendental identity.

Fictional continuous annual zero-node table tenors[1,2,3] years,rates[.04,.05,.055]. Node log discounts are−.04,−.10,−.165; log-linear at2.5 gives−.1325 and DF exp(−.1325). Average forward1→2=(.10−.04)/(2−1)=.06. Coupon price5exp(−.04)+105exp(−.10) is independently evaluated with Decimal400. Negative rates/forwards remain valid under stated continuous convention, not an automatic arbitrage finding.

A parallel direct zero-node shift+.0001 changes price to5exp(−.0401)+105exp(−.1002), independently checked. For positive future payments this decreases PV. This is a fixed zero-node sensitivity experiment, NOT quote-bump/rebootstrap DV01; no contractual market-quote instrument set or general rebuilding procedure exists here. E33/E34/E36 market-quote/rebuild/sign controls remain design scope.

Rational integer/displayed-decimal arithmetic precedes zero-node products, log interpolation, elementary bootstrap ratios and signed accumulation. Decimal exponentials are retained internally when public discount factors would underflow/overflow, so a reportable amount-weighted PV can survive. For example1e308*exp(−800) remains positive/reportable even though exp(−800) alone is not a nonzero float. A public discount report still rejects a nonzero unreportable value. Internal exponentials/forward logarithms use scale-aware Decimal precision; no arbitrary-conditioning/correct-rounding proof is implied.

The extreme cancellation probe uses tenors[1e308,1.5e308], zeros[1.5e308,−1e308], query1.25e308. Exact log ordinates±1.5e616 cancel to0, yielding DF1; naive float products produced nonfinite logs. This is a numeric stress fixture, not a meaningful market curve. Other scale probes preserve signed integer cashflows and exact bootstrap numerator differences. Dates/conventions are still supplied year fractions, with no calendar engine.

## Forty local answer records

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | Source DF exp(−.1) for2y/.05. |
| 02 | Source zero recovery≈.05 from supplied float DF. |
| 03 | Source negative zero rate gives exp(.02)>1. |
| 04 | Supplemental100*.9=90; scalar PV equation reviewed. |
| 05 | Source coupon PV and independent Decimal two-payment sum. |
| 06 | Source one-year bootstrap19/20. |
| 07 | Source two-year bootstrap127/140, independent algebra. |
| 08 | Source nonpositive bootstrapped discount rejects. |
| 09 | Direct rational repricing and source zero-node/API-chain repricing executed within stated budgets. |
| 10 | Deposit/OIS/swap/bond quote conventions differ; conceptual, only elementary annual bond equations exported. |
| 11 | Year fractions explicit; no assumption every six months=.5 or automatic conversion. |
| 12 | ACT360/365 accrual differences conceptual; no day-count library. |
| 13 | Business-day adjustment requires calendar convention; not implemented. |
| 14 | Trade/settlement valuation basis must be aligned; no actual dates provided. |
| 15 | Calibration maturity as knot is a design concept; explicit fictional nodes only. |
| 16 | Geometric DF midpoint identity follows log interpolation; same mathematical derivation as prior section, source zero-node representation tested here. |
| 17 | Source forward from exp(−.04)/exp(−.10)=.06 within input/report rounding. |
| 18 | Source increasing discounts yield negative forward. |
| 19 | Increasing D in negative-rate model not inherently invalid; conceptual convention review. |
| 20 | Source nonpositive discount rejects; underflowed public nonzero DF also rejects. |
| 21 | Different interpolated quantity gives different intermediate DF; log-node midpoint exp(−.1325) checked, linear-zero convention remains distinct. |
| 22 | Par swap PV equality is conceptual; no swap pricing engine. |
| 23 | Projection/discount separation is conceptual; no multi-curve system. |
| 24 | OIS/collateral statement is conditional conceptual context, not a current contractual recommendation or tested feature. |
| 25 | Appropriate floating index projection curve required; unsupported by this fixed-flow reference. |
| 26 | Earlier D1 feeds D2 bootstrap equation; source elementary chain executed. |
| 27 | Exact SciPy brentq snippet runs on a valid bracket; no general nonlinear/bootstrap library claimed. |
| 28 | Root economic selection/repricing remains model responsibility; current scalar bond equation unique and linear in unknown DF. |
| 29 | Overdetermined weighted least squares conceptual; not implemented. |
| 30 | Sparse long-end interpolation/extrapolation risk conceptual. |
| 31 | Source out-of-domain query/cashflow rejects; no approved tail rule implemented. |
| 32 | Piecewise-linear log discount permits forward jumps; analytic, no smooth-forward guarantee. |
| 33 | Market quote+1bp rebuild remains design; direct zero-node bump is executed separately and labeled. |
| 34 | DV01 requires explicit bump/sign convention; no production DV01 acceptance inferred. |
| 35 | Source parallel upward zero shift lowers positive-CF PV and matches independent bumped price. |
| 36 | Key-rate risk depends on rebuild; design only, no market quote sensitivity export. |
| 37 | Mixed quote timestamps can be inconsistent; no actual market snapshot used. |
| 38 | Market-appropriate arbitrage constraints remain conceptual/external acceptance. |
| 39 | Fixture/algorithm/version/units/residual evidence retained; no actual quote timestamp or production deployment. |
| 40 | Numeric repricing/positivity/domain controls executed; calendar, sensitivity/rebuild and approval gaps kept separate. |

## Twelve lab-step records

Prerequisites: Python; finite typed quantities; positive strictly increasing reusable zero-node tenors; compatible year fractions/continuous rates; valid annual coupon equations; nonempty list/tuple time/amount records within curve domain. SciPy installed for separate snippet. All inputs fictional; no actual valuation date, currency selection, settlement, accrual, collateral or market close supplied.

| Step | Actual evidence and limit |
|---|---|
| 1 | Exact reference saved isolated, runtime/hashes retained. |
| 2 | Source discount at2y/.05 versus independent exp(−.1). |
| 3 | Source zero recovery from that supplied DF. |
| 4 | Source D1=.95 from price95/face100. |
| 5 | Source D2=127/140 from coupon price100/coupon5/face100. |
| 6 | Direct rational repricing; separate source bootstrap→zero→price chain within1e−12 currency budget. |
| 7 | Explicit three-node table[1,2,3]/[.04,.05,.055]. |
| 8 | Source2.5y DF versus exp(−.1325). |
| 9 | Source1→2 forward.06 and negative-forward case. |
| 10 | Source coupon cashflow list priced with independent Decimal expectation, plus numeric accumulation stress probes. |
| 11 | Invalid tenors, negative discount, out-of-domain/malformed flows and output range reject as retained. |
| 12 | Four commands,43 supplemental predicates and twelve existing methods pass;16 baseline failed predicates retained. |

## Twelve acceptance-control records — scoped dispositions

| Control | Evidence or unresolved boundary |
|---|---|
| 1 Valuation/currency/close | Not supplied; fictional common units only, no market acceptance. |
| 2 Quote snapshot/source | Fixed synthetic quotes recorded; no feed/time-source verification. |
| 3 Instruments/maturities | Elementary one-year zero and two-year annual coupon bond defined; no security master. |
| 4 Quote/compounding | Continuous node rates, positive price/face and annual coupon equations explicit; no mixed-quote conversion. |
| 5 Calendars/day count | Unsupported; numeric years only. |
| 6 Ordering/duplicates | Source validation/errors executed. |
| 7 DF positivity | Source public reports/range validation executed; private amount-weighted discount may lie beyond float range. |
| 8 Repricing | Two fictional calibration instruments/direct equations and local source API chain only; not every real calibration instrument. |
| 9 Forwards/interpolation | Source average forwards/log interpolation tested; economic plausibility/curve-wide arbitrage review open. |
| 10 Extrapolation | Source rejection tested; no tail method implemented. |
| 11 Quote risk/stress | Numerical range/cancellation and direct zero-node shift executed; market-quote rebuild/key-rate stress remains design. |
| 12 Settings/version/approval | Source/runtime/residuals retained; separate SciPy bracket/assertions executed; external approvals absent. |

## Limits and resume checkpoint

Local Linux CPython/SciPy only. No general market bootstrap, calendar/day-count/schedule support, multi-curve/collateral pricing, credit adjustments, market-snapshot approval, rigorous arbitrage/conditioning proof, quote-rebuild risk engine, production performance, broad shared-input integration, notebook/platform or external independent certification. Exact source execution, supplemental equation/Decimal derivations and conceptual designs remain separate above. F28/F32, F165 CDF-tail limits and every unresolved tracker finding remain open.

Chapter17 has ten core workflows and395 local answers scoped. Next: Section17.11 — Numerical Stability; resume from fresh main without duplication.
