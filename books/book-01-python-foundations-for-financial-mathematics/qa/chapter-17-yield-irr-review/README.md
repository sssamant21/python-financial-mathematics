# Section 17.4 — scoped yield and IRR review

Affected baseline: `7fefe3b7e6ec67aa1690c39efe76d4e3f21dae5a`. Finding F161; severity medium (educational numerical correctness); owner Book 1 manuscript maintainers; decision repair source and clarify contracts. Reviewer: automated source execution plus mathematical and prompt/step review, not external independent acceptance. Final corrected revision is the containing publication commit.

One workflow, 40 local answers and twelve lab-step records are separate inventories. [results.json](results.json) records four successful exact-source commands, 55 passing supplemental predicates and twelve existing unittest methods. Zero new historical unique methods. Source/listing SHA256, Python/platform/SciPy versions, raw stdout/stderr, fixtures, tolerances and actual values are retained.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-yield-irr-review/review.py
```

Reproduce the unchanged-source baseline (expected nonzero exit, requires Git history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-yield-irr-review/review.py 7fefe3b7e6ec67aa1690c39efe76d4e3f21dae5a
```

[baseline.json](baseline.json) retains nineteen failed predicates; the existing twelve methods and exact SciPy snippet already passed. Source defects include integer cancellation, tiny-rate loss, periodic/dated power overflow, coupon overflow before a finite discounted value, midpoint overflow, non-identifiable IRR selection, consumed generator inputs returning a spurious endpoint root, and inconsistent invalid-input/reporting exceptions. The final endpoint-root probe additionally checks that exact displayed-decimal NPV(.1)=0 is not lost before bracketing; final inventories include it. Strict calendar-date inputs are a disclosed contract tightening: original code accepted `datetime` and silently used whole elapsed days, potentially discarding time-of-day information. Original malformed-record, no-bracket, rate-domain and iteration/stagnation guards that already passed are not counted as newly discovered defects. Nineteen predicates do not mean nineteen distinct defects.

Exact listing commands save and run the verbatim demonstration/tests, import silently and compile in an isolated directory. A fourth command executes the verbatim SciPy snippet and parses its printed IRR/residual against an independent expectation. SciPy 1.17.0 is available here. Supplemental predicates call source exports or clearly identified analytic expressions; no supplemental yield solver substitutes for source execution.

## Mathematical expectations and model inputs

For [-100,60,60], put q=1+r. Multiplication by q² gives 100q²−60q−60=0, so r=(3+sqrt(69))/10−1. The positive admissible root is compared with 100-digit Decimal evaluation and the original NPV is independently repriced within 1e−9 currency units. Separate brackets for [-100,230,−132] isolate exact rates .1/.2; direct substitution has a 1e−12 currency budget, root comparison a 1e−12 absolute rate budget. The all-negative case has no admissible root; all-zero cashflows are non-identifiable rather than unique at a bracket endpoint.

Bond fixture: fictional face 100, annual coupon .05, three annual period ends, no accrued interest; prices at .04/.05/.06 are independently sum(5/(1+r)^t,t=1..2)+105/(1+r)^3 using rational arithmetic. YTM reuses this fixed schedule and the calculated dirty price, not a real quote. Zero coupon value is exactly 10000/121 at two years/10%. No irregular bond settlement convention is implemented.

Dated fixture: −100 on 2025-01-01, +110 on 2026-01-01, actual 365 days, annual effective rate .1. The 182-day variant has analytic XIRR 1.1^(365/182)−1. Leap-year 2024-01-01 to 2025-01-01 uses 366/365 years and XIRR 1.1^(365/366)−1. Separate probes cover fractional-day discounting, pre-base negative exponents and unordered duplicate-date integer cancellation. No market-data/as-of or currency conversion inputs exist.

Periodic values, coupons and full price-minus-market residuals use rational arithmetic before finite float reporting. Whole-year dated exponents are rational; fractional ACT/365 exponents use Decimal log/exp with precision increased for small rates and amount scale. This mitigates tested cases, not a correctly rounded arbitrary-cancellation proof. Reusable list/tuple records and exact calendar dates are required; single-pass generators and datetimes reject explicitly. Duplicate dates aggregate; zero date-aggregated streams reject as non-identifiable. Returned bisection diagnostics separate midpoint evaluations from halvings; conditional error bounds require continuity and accurate signs. Callback zero alone is not mathematical certification.

## Forty local answers

| Exercise | Review and execution boundary |
|---|---|
| 01 | Source IRR versus analytic 110/100−1=.1. |
| 02 | Source periodic IRR [-100,0,121] versus sqrt(1.21)−1=.1. |
| 03 | Source NPV(0)=20. |
| 04 | Source NPV(.1)=500/121≈4.1322314. |
| 05 | Source endpoints 20 and −25/3 justify [0,.2]; analytic root and independent repricing checked. |
| 06 | Source zero-coupon PV=10000/121≈82.6446281. |
| 07 | Source yield for rounded price82.64463 compared to inverse sqrt(100/price)−1, approximately .1. Rounding is not ignored. |
| 08 | Source coupon=yields=.05 bond prices exactly100 under rational model. |
| 09 | Source price at.06 below100, independently rationally repriced. |
| 10 | Source price at.04 above100, independently rationally repriced. |
| 11 | Supplemental exact coupon1000*.04=40; source coupon construction also tested with extreme finite discounted value. |
| 12 | Independent rational three-payment sum matches source prices. |
| 13 | Correct residual P(y)−98; source YTM performs whole-residual subtraction. No real quote98 used in lab. |
| 14 | Source .04/.05/.06 price ordering plus conceptual positive-CF monotonicity. |
| 15 | Each derivative term −tCFt/(1+y)^(t+1) is negative for positive future CF; analytic review. |
| 16 | Decimal .06 annual effective matches source annual periods. |
| 17 | Semiannual frequency conversion remains design, not an implemented feature. |
| 18 | Supplemental clean99+accrued1.25=dirty100.25; no accrued-interest engine. |
| 19 | Fractional settlement/accrual effects reviewed; actual bond calendars remain absent. |
| 20 | Source both .1/.2 bracket roots and original-NPV substitution, not global enumeration. |
| 21 | Source all-zero periodic/date-aggregated XIRR rejects non-identifiability. |
| 22 | Existence conditional on continuous residual and trustworthy opposite signs. |
| 23 | All-negative source no-bracket rejection; algebra proves NPV<0 for r>−1. |
| 24 | Scale/timing can reverse IRR versus NPV rankings; conceptual, no investment recommendation. |
| 25 | IRR defines discount-rate zero, not guaranteed realized/reinvestment return; conceptual. |
| 26 | 365 actual days divided by365 gives1; source annual dated fixture. |
| 27 | Source 182-day case uses182/365, independently discounted and inverted. |
| 28 | Source XIRR evaluates explicit dated-NPV formula and recovered rates. |
| 29 | Source leap-year XIRR compared to1.1^(365/366)−1. |
| 30 | Exact endpoint .1 returned by source periodic IRR on [.1,.2]; endpoint callback zero remains numerical evidence. |
| 31 | Source positive-endpoint no-bracket example rejects. |
| 32 | Supplemental exact98.00001−98=.00001 currency units. |
| 33 | Supplemental exact half-width1e−10/2=5e−11 conditional rate error bound. |
| 34 | Small derivative increases inverse uncertainty; conceptual, no condition-number estimate exported. |
| 35 | First-order duration formula reviewed with compatible rate convention; no duration export here. |
| 36 | Supplemental −(−.02)/.01=2 modified duration. |
| 37 | Conventional investment's decreasing NPV crosses at.09, hence NPV(.12)<0; conceptual restriction matters. |
| 38 | Source r=−1 rejects. |
| 39 | Omitted coupon changes economic equation even if solver converges; schedule completeness remains input acceptance. |
| 40 | Fictional fixture/conventions, source hash, runtime, bracket, residual and raw commands retained; independent acceptance open. |

## Twelve lab steps

Prerequisites: installed Python, reusable cashflow lists/tuples, finite typed quantities, valid rates>−1, positive face/market price and integer years; exact calendar dates for dated model. SciPy is only needed for the separate optional snippet. This execution does not validate notebook installation or supported platforms.

| Step | Actual evidence and scope |
|---|---|
| 1 | Exact isolated listing saved; interpreter/platform/hash recorded. |
| 2 | Source single-receipt NPV at.1 versus exact0. |
| 3 | Source single-receipt IRR versus.1; NPV substitution and embedded test. |
| 4 | Source [-100,60,60] bracket [0,.2], algebraic root and independent repricing. |
| 5 | Source separate [.05,.15]/[.15,.25] brackets recover both rates; no root enumeration. |
| 6 | Source three-year par bond100 with explicit annual schedule. |
| 7 | Source .04/.06 prices and direction versus independent rational sums. |
| 8 | Source YTM recovers.06 within absolute1e−12 rate units. |
| 9 | Source two-year zero coupon matches10000/121. |
| 10 | Source dated 365-day fixture XIRR=.1, plus separate leap/182-day probes. |
| 11 | Source invalid domain, no bracket, all-negative/all-zero, malformed records, generator/date policy and float failure paths exercised. |
| 12 | Twelve existing methods, four commands and55 supplemental predicates pass; nineteen baseline failures retained. |

## Limits and resume checkpoint

Local Linux CPython/SciPy only. No real quote/calendar/accrual/clean-price conversion, semiannual quotation, credit/option/market acceptance, all-root enumeration, arbitrary conditioning proof, broad cross-module shared-input integration, notebook/platform or external reviewer certification. F28/F32 and newer unresolved tracker findings remain open. Supplemental derivations and conceptual financial controls are separate from executed source exports.

Chapter17 now has four core workflows and155 local answers scoped. Next: Section17.5 — Optimization Fundamentals; resume from fresh main.
