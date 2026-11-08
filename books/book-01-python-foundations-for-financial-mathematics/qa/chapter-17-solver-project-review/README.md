# Section 17.14 — scoped financial numerical solver project review

Affected baseline: `7ea8aeeae79fa6a8157b33657c462eaf8c345749`. F171, severity medium (educational numerical correctness/integration), owner Book 1 manuscript maintainers. Decision repair periodic/sensitivity range and iterable handling, clarify normalized solver diagnostics and non-identifiable flows, preserve setup/runtime boundaries. Reviewer: automated execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One project workflow,40 local answers,twelve lab steps,six separate architecture acceptance records,four worked financial examples and five extension-design records are distinct from four primary exact-source commands,36 supplemental predicates and twelve existing unittest methods. The same twelve methods additionally pass in a clean installed environment; that is24 invocations of12 existing methods, not24 unique methods. Zero historical unique methods added. [results.json](results.json) retains primary runtime/platform/SciPy, raw outputs, values/tolerances, complete reports/model and manuscript/implementation/test SHA256.

Primary review from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-solver-project-review/review.py
```

Reproduce unchanged source (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-solver-project-review/review.py 7ea8aeeae79fa6a8157b33657c462eaf8c345749
```

Reproduce the clean Linux setup/install/exact-source run (requires package-index access, writes its own setup evidence):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-solver-project-review/setup.py
```

## Retained baseline and two runtime paths

[baseline.json](baseline.json) retains ten failed predicates; the original twelve tests and printed project demonstration already passed. Defects/contracts include integer/tiny-rate/discounted-flow NPV loss, one-bp generator consumption twice, subtraction of already-rounded large NPVs, loss of the1/10000 increment at a huge rate, selecting an arbitrary endpoint for all-zero non-identifiable flows, malformed/huge inputs and silently erased nonzero NPV. All-zero-flow rejection is an explicit financial interpretation guard: the zero function has infinitely many roots, not a unique implied rate. Ten predicates are not ten distinct defects. No observer failures occurred.

The primary four commands save the verbatim implementation and separate test file, run the project demonstration, run `unittest -v test_financial_solver`, compile both files and import both silently. They use the available supported Linux runtime: Python3.12.14/SciPy1.17.0. The implementation and test blocks remain distinct artifacts; no supplemental implementation replaces exact-source execution.

[initial-setup-results.json](initial-setup-results.json) retains the earlier environment-only experiment: actual clean `python -m venv .venv`, `python -m pip install scipy` and installed import/version all succeeded. No scientific test execution is claimed for that earlier record.

[setup-results.json](setup-results.json) retains the final clean experiment: three setup/import/version command records plus four exact-source verification command records. It created a fresh temporary Linux venv, installed SciPy1.18.1/NumPy2.5.4 on Python3.12.14, then ran the unchanged corrected project demonstration, the same twelve existing tests, compilation and silent imports. All seven commands returned0. Source/implementation/test hashes bind this clean run to the reviewed files. Temporary environment is removed after recording; `setup.py` faithfully recreates it. The venv Python executable is selected directly; the printed shell activation command itself is not exercised. Pip retry/timeout environment controls bound the setup attempt and are retained in the runnable script. The installation is an actual execution, not evidence that all platforms/dependency combinations or notebooks work. Primary/clean command inventories and duplicate method invocations are separate; they are not new historical unique methods.

## Independent financial expectations and diagnostics

Fictional periodic flows[-100,110],t0/t1,annual-effective decimal rate r>−1. NPV(0)=10, NPV(.1)=0, NPV(.11)=−100/111≈−.9009009. Exact root1/10 is independently derived from110/(1+r)=100. Source root/repricing/report checks retain rate_xtol1e−12 and currency residual tolerance1e−8 as different units. The exact +1bp model change at.1 is110/(1.1001)−110/1.1=−100/11001≈−.00909008, not a derivative per unit rate. With a huge t0 flow, subtracting two rounded NPV reports would erase that finite change; source now forms the whole rational difference first.

`one_bp_change` materializes input once and reuses validated model flows. The generator example now produces the same independently derived finite change rather than consuming input during the first of two NPV calls. At rate1e20, the exact rational increment1/10000 is retained even when adding it directly to a float would leave the float unchanged. These are scoped local API integration checks, not resolution of broad F32 shared-input integration.

For[-100,230,−132], multiplying by(1+r)^2 gives−100(r−.1)(r−.2); separate [.05,.15]/[.15,.25] solves recover each root and independently reprice the original equation. A bracket enclosing both crossings can have same-sign endpoints and reject. The code does not enumerate all roots or choose an investment.

SciPy callbacks now divide exact model NPV by max absolute cashflow. This constant normalization preserves roots while separating callback scale from currency reporting. `residual_scale` and `callback_units` report the distinction. `function_calls` for brentq is SciPy's normalized callback count, excluding two exact bracket-sign checks and final repricing; endpoint path reports two explicit endpoint evaluations,0 iterations and currency units/default scale1. Original bracket is a search-input record, not a returned final Brent bracket/error bound.

A loose rate tolerance.01 on scaled flows[-1e200,1.1e200] converges while its currency residual exceeds1e−8; the retained report correctly has residual_accepted=False. A separate small-scale fixture uses explicit currency budget1e−210; a default1e−8 budget would be economically meaningless at that scale. Final unrounded model residual is compared with the selected currency threshold before float reporting. Required nonzero reports/callbacks reject if unreportable; even an accurate root can lack a representable currency residual. No tolerance is widened after a failure.

## Six architecture acceptance records and four worked examples

| Record | Actual evidence and boundary |
|---|---|
| Architecture1 NPV10% | Exact model zero and independent1e−12 currency benchmark. |
| Architecture2 root | Returned root near.1 with independent absolute rate check. |
| Architecture3 residual | Reported currency residual and accepted flag; loose-tolerance converged/rejected counterexample retained. |
| Architecture4 NPV11% | Source versus−100/111. |
| Architecture5 rate≤−1 | Clear ValueError retained. |
| Architecture6 bracket | Same-sign/no-root bracket rejects; two-crossing bracket distinction explicit. |
| WorkedA baseline | Source price/NPV/root/diagnostics versus analytic1/10. |
| WorkedB rate stress | Source11% NPV and positive-future-flow direction. |
| WorkedC one bp | Source finite change versus−100/11001, generator/large-base-amount tests separate. |
| WorkedD multiple roots | Both roots independently derived and repriced; no global uniqueness claim. |

## Forty worked-answer records

| Exercise | Alignment and execution boundary |
|---|---|
| 01 | C0 is time-zero flow; explicit list convention. |
| 02 | Rate−1 denominator zero; source rejects. |
| 03 | One-year110 PV100 independently derived. |
| 04 | Source NPV0 at.1. |
| 05 | Source root versus exact1/10. |
| 06 |10%=.10 decimal, not10. |
| 07 |1bp=1/10000; source finite difference retains exact increment. |
| 08 | Source11% NPV−100/111. |
| 09 | Positive future cashflow makes baseline NPV decrease; not arbitrary-sign rule. |
| 10 | Sign change plus continuity implies conditional existence. |
| 11 | No uniqueness from sign change; separate multiple-root example. |
| 12 | Same-sign bracket can enclose two crossings; source rejects that bracket without claiming no roots. |
| 13 | Source separate .1/.2 roots and independent repricing. |
| 14 | Rate xtol measures termination in rate coordinates, not currency/model error. |
| 15 | Currency residual distinct from normalized callback units. |
| 16 | Converged-but-residual-rejected report executed. |
| 17 | Endpoint path reports exact callback/model endpoint,0 iterations,2 checks. All-zero case separately rejects non-identifiability. |
| 18 | Source maxiter1 failure raises RuntimeError. |
| 19 | Source doubled flows at.05 versus200/21. |
| 20 | Appended zero leaves original timing unchanged; inserted period delays payment and changes NPV to−100/11. |
| 21 | Rate refinement cannot repair wrong dates; no date engine. |
| 22 | Clean/dirty bond prices not implemented. |
| 23 | Rational one-period/quadratic/finiteshift expectations independent of source solver. |
| 24 | Deterministic root solver requires no seed; no simulation. |
| 25 | Source rate−.05 allowed and gives NPV300/19. |
| 26 | Empty flow input rejects. |
| 27 | NaN flow rejects. |
| 28 | Unreportable numeric calculations raise ValueError; new rational model avoids several old exponential intermediate failures. |
| 29 | Answer updated: unreportable nonzero callbacks/reports reject, not support for every mathematical value. |
| 30 | Absolute residual of−.01 is.01; report retains signed currency residual and separate acceptance. |
| 31 | Source one-bp finite change distinct from derivative. |
| 32 | Inserted zero shifts later period indices; executed contrast. |
| 33 | Root alone does not select an investment; conceptual. |
| 34 | Local price sensitivity helps translate residual to yield error; no error-bound/certification exported. |
| 35 | Criteria chosen before results; baseline failures retained without widening budgets. |
| 36 | Purchase price included once in C0; no separate price subtraction API here. |
| 37 | Inputs/runtime/source/test hashes and versions retained, including actual clean install. |
| 38 | Stable root does not validate schedule; no real instrument acceptance. |
| 39 | Existing tests and clean reruns do not certify production readiness. |
| 40 | Comprehensive mathematical/editorial/model/platform/independent validation remains open after this scoped batch. |

## Twelve project lab-step records

Prerequisites: Python with SciPy, finite typed flow iterable containing at least t0/future period, annual-effective rate>−1, valid representable float bracket, positive rate tolerance/iteration budget, nonnegative currency tolerance. All data fictional/common currency with compatible periods; no dates/accrual/fees/taxes unless supplied in flows. Normalization is numerical scaling, not a different economic model.

| Step | Actual evidence and limit |
|---|---|
| 1 | Actual clean Linux venv creation succeeds; recorded Python version. No Windows/PowerShell/notebook claims. |
| 2 | Actual isolated SciPy install/import succeeds; versions recorded, primary supported runtime remains separate. |
| 3 | Verbatim implementation/test files saved separately in isolated temp directories. |
| 4 | Source NPVs at0/.1/.11 checked independently. |
| 5 | Source report retains method/iterations/input bracket/rate/callback counts. |
| 6 | Independent root1/10 comparison. |
| 7 | Currency threshold and normalized callback units separated, including rejected residual report. |
| 8 | Source exact1/10000 finite change versus−100/11001; no derivative substitution or rounded-NPV subtraction. |
| 9 | Invalid bracket/rate and failed iteration paths exercised. |
| 10 | Separate two-root brackets and original-equation repricing. |
| 11 | Twelve existing methods pass in primary runtime and are rerun in clean SciPy1.18.1 environment. Duplicate invocations not new unique methods. |
| 12 | Primary four source commands/36 predicates, separate three setup plus four clean source commands and ten baseline failures retained; external approval absent. |

## Five extension-design records

| Extension | Scoped status |
|---|---|
| Dated cashflows/day count | Not implemented; new specification/calendar/validation needed. |
| Compare root methods | Brentq plus analytic benchmarks only; no new multi-method project interface. |
| Bracket scan | Separate given brackets tested; automatic candidate scan/all-root proof absent. |
| Independent/property testing | Independent fixed expectations/metamorphic cases executed; no generated property-based framework or universal proof. |
| Underflow/near-singular sensitivity | Scoped numeric range/one-bp/scale checks executed; arbitrary conditioning and near-singular economic analysis remain open. |

## Limits and resume checkpoint

Two actual Linux Python3.12.14 SciPy environments, not a supported-platform matrix. No Windows/PowerShell execution, notebook validation, production schedules/day counts, fees/taxes unless supplied, generalized bracket scan/all-root certification, investment recommendation, arbitrary-conditioning proof, production performance, broad shared-input integration or external independent acceptance. Source execution, supplemental rational derivations and conceptual extensions remain separate above. F28/F32, F165 integrated-CDF tail limits and all unresolved tracker findings remain open.

Chapter17 has fourteen core/project workflows and555 local answers scoped. Next: Section17.15 — Exercises and Applied Problems; resume from fresh main without duplication.
