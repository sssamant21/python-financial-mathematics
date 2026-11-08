# Section18.6 — Price-path simulation: scoped review

Reviewed2026-11-08 by Codex, not an external independent reviewer. Baseline `79a67421b80bb7393bdc86169cad62dffa33b79f`; [source](../../chapter-18/18.06-price-path-simulation.md). One workflow, forty local answers, twelve lab steps. No new historical unique methods.

Run from the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-paths-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-paths-review/review.py 79a67421b80bb7393bdc86169cad62dffa33b79f
```

The baseline command intentionally exits1 and requires that git object. [Baseline](baseline.json) retains fourteen failed supplemental predicates; [corrected results](results.json) retains76 passing supplemental predicates and three passing exact-source command records: verbatim reference demo/ten existing methods, quiet import and compile. Commands, predicates, workflow/steps, exercise records and existing methods remain separate. Source/listing SHA256, actual stdout/stderr, CPython3.12.14/Linux and seeded run metadata are in JSON. Source decimal exponentiation makes this small review slower than the original binary64 demo; no speed benchmark or production suitability claim.

## Finding F178 and observer provenance

Original barrier validation consumes a one-pass path iterator and then checks the exhausted iterator, missing a hit. Repeated binary multiplication loses zero-dynamics initial integer identity, including the zero-horizon benchmark. Float horizon/steps can become zero and silently discard nonzero drift. Huge numeric inputs leak OverflowError; malformed path collections leak TypeError. These substantiate input/iterator and numeric contract corrections.

Source now uses finite int/float inputs in finite float range, excluding booleans; displayed-decimal floats and exact integers; rational time steps/log drift; reported square-root shock scale; accumulated log increments with scaled Decimal exponentials from original initial value; guarded exact whole-number reports; and rational summary statistics with direct SE. It supports one-pass collections, validates the barrier's entire observed path once, and raises ValueError on invalid inputs or unreportable nonzero outputs. Source now explicitly states that terminal summary validates **only terminal prices**, not all intermediate prices, grids or times. The supplemental `[[None,90],[None,110]]` fixture tests this narrow terminal-summary policy, not approval of such a path for other uses.

One of fourteen baseline failures is a **labeled support extension**, initial1e-308×exp1000. The earlier source explicitly disclaimed support for all finite extremes; supporting a finite final scaled result when exp alone overflows is not retroactively called a promise violation. Decimal exponent precision is finite, and accumulation/shock-scale conventions can change last-bit outputs from earlier binary64 recurrence. Inputs outside the described report range and continuous monitoring remain unsupported.

The [initial observer baseline](initial-observer-baseline.json) retains three additional failed QA arithmetic expressions that mixed Fraction and Decimal (shock scale and two log-SD oracles). Those were converted to Decimal arithmetic, and the unchanged original source rerun to produce the final fourteen-failure baseline. They are observer defects, not manuscript failures; the earlier76-predicate/17-failure inventory is a transition, not three additional unique methods or new source defects. Original ten unittest methods were not rewritten and pass both revisions.

## Analytical and supplemental evidence boundaries

Exact execution is the entire unmodified listing per source revision, including demo/tests, plus import/compile. Additional source calls are supplemental probes. Shared-shock replay uses the same random.Random normalvariate stream to compare update algebra; it does not independently establish normality, step/path independence or RNG quality.

Independent rational algebra gives compounded100×1.1×.9=99 (−1%), dt1/12 or2/8=.25, log drift.05−.2²/2=.03, and shock scale.2sqrt(.25)=.1. For GBM, log(S_T/S0) is Normal((mu−sigma²/2)T,sigma²T), so completing the square gives mean S0exp(muT), while normal median0 gives median S0exp((mu−sigma²/2)T). Thus mean100exp(.05)=105.1271096… and median100exp(.03)=103.0454534…, with printed105.12711/103.04545 explicitly checked. Log SD is.2 at1year and.4 at4years. Decimal exp/root expected values use a separate algebraic observer, but share Python's Decimal backend with source helpers; no independent arithmetic-library certification.

The deterministic path sigma0 is checked at grid points0,1,6,12 against100exp(.05j/12). A two-path, four-step shared-normal replay computes each cumulative increment with an independently written100-digit Decimal GBM expression. Both comparisons use rtol1e-12,atol0; exact integer identity uses equality. Actual terminal sample mean/SE is recomputed with Fraction(str(price)) and Decimal sqrt independently of the summary function. These are numerical predicates, not statistical acceptance bands. No requirement that sample mean equal the model target or that a larger individual run be closer.

## Twelve lab-step contracts

Prerequisites: Python standard library; save exact reference as price_path_simulation.py. Fixture: initial100 fictional common-currency units, annual mu.05/sigma.2, horizon1year,12 equal steps,10000 paths. Measure is an uncalibrated illustrative GBM measure, not a validated real-world or risk-neutral pricing setup. No external dataset/date, dividend, jump, transaction-cost or continuous-monitoring model.

| Step | Action and observed result |
|---|---|
| 1 | Python/platform/generator, seeds42/43, fixture, source hashes and measure limitation retained in JSON. |
| 2 | Constant GBM and log increment reviewed; mu annual price drift, sigma annual volatility, T in years. |
| 3 | Exact dt1/12year; scale uses sqrt(dt), not dt. |
| 4 | Independent mean105.1271096… and median103.0454534…; printed rounding checked. |
| 5 | Exact reference demo/ten methods executed; source generated10000 paths for seed42, separately seed43. |
| 6 | Seed42 mean105.08580059649347, SE.21254296482289836; descriptive comparison with model mean. No statistical pass/fail or coverage claim. |
| 7 | All paths start100 and have13 prices; first two paths/hashes retained. Positivity checked by original source method; source summary's narrower terminal validation documented. |
| 8 | Sigma0 grid path compared at selected grid dates and terminal against100exp(.05t); zero dynamics integer identity checked separately. |
| 9 | Seed43 mean105.06879175122633, SE.21305464403766847; variation recorded, not independence proof merely from seed changes. |
| 10 | Barrier95: seed42 has6267 hit paths and36463 observed prices≤95; seed43 has6349 hit paths and36785 observed prices≤95, each out of130000 recorded prices including time zero. Path-hit count and observation count are separate; source checks equality/time0/iterators. No claim of between-grid detection. |
| 11 | Invalid input/output probes, ten original methods, import/compile passed after corrections; original failures and observer transition retained. |
| 12 | Model/units/commands/runtime/results/limits recorded; no deployment or external acceptance. |

## Forty local prompt-to-answer alignment records

All forty prompts and answers read in order. Conceptual/design reviews below are not fictitious callable exports or extra runtime methods.

| Answer | Scoped disposition |
|---|---|
| 1 |100 then+10%,−10% gives99, exact fractions. |
| 2 |Cumulative return−1%, exact fractions. |
| 3 |Log returns add across periods, correct multiplication/log identity. |
| 4 |T1,n12 givesdt1/12, rational calculation. |
| 5 |T2,n8 givesdt.25, rational calculation. |
| 6 |GBM log drift.03, rational mu−sigma²/2. |
| 7 |Shock scale.1 atdt.25, Decimal root. |
| 8 |Zero-vol terminal105.12711, deterministic source grid/oracle. |
| 9 |Mean105.12711 even withsigma.2, source benchmark versus GBM moment. |
| 10 |Median103.04545, independent lognormal moment/rounding. |
| 11 |Log SD.2 atT1, model formula. |
| 12 |Log SD.4 atT4, model formula. |
| 13 |Grid-time exactness does not remove model risk, correct distinction. |
| 14 |Discrete grid can miss barrier crossings, correct monitoring limit; no bridge implementation claimed. |
| 15 |Time0 included, source equality test. |
| 16 |Step count differs from path count, source shape10000×13 and original method. |
| 17 |More paths do not fix assumptions, correct model distinction. |
| 18 |Fourfold independent paths approximately halves SE under same variance, factor check. |
| 19 |Fixed seed does not prove accuracy, correct; replay evidence separately labeled. |
| 20 |Non-overlapping Brownian increments independent by model assumption, not proved by pseudorandom replay. |
| 21 |Exact GBM positive, exponential form; source positive/reporting guards. |
| 22 |Binary64 can underflow to0, actual source-rejection extreme case. |
| 23 |Exponential can overflow, actual source-rejection extreme case. |
| 24 |Risk-neutral drift not generally historical drift, correct measure requirement. |
| 25 |No dividends in code, source design review. |
| 26 |Average-price payoff path-dependent, supplemental different-average/same-terminal example. No source average-payoff API. |
| 27 |Call payoff depends on terminal and strike, supplemental max(120−110,0)=10. No pricing API. |
| 28 |Each path includesS0, shape/first-observation check. |
| 29 |12steps gives13 recorded prices, shape check. |
| 30 |Negative volatility invalid, source rejection/original method. |
| 31 |simulate_paths rejectsT0, explicit probe. |
| 32 |expected_terminal allowsT0 and returnsS0, exact integer-identity probe. |
| 33 |Fixed seed alone not variance reduction, correct design distinction. |
| 34 |Constant GBM lacks jumps, correct model inspection. |
| 35 |Finer grid no guarantee of every crossing, correct monitoring distinction; no continuous-monitoring validation. |
| 36 |Lognormal right skew when sigma>0 explains mean>median, analytic formulas. |
| 37 |Annual mu/sigma and year-basedT must match, recorded fixture. |
| 38 |Generator/version/input order/parameters also matter, metadata and replay recorded; no portable bitwise claim. |
| 39 |Sigma0 path deterministicS0exp(mu t), selected dates checked independently. |
| 40 |No guaranteed realized path, correct simulation interpretation. |

## Remaining scope / resume

Next: **Section18.7 — Scenario Analysis**. Chapter18 now has six scoped workflows and240 local answers; later scope remains. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, monitoring/rare-event/coverage/independence, broader input/branch coverage, financial model/editorial/copyright and external independent acceptance remain open. No certification, production or external messaging action.
