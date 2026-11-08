# Section 17.8 — scoped numerical integration review

Affected baseline: `dd7886091994f886f0c6842a2a0bb3d7ff4e2b33`. F165, severity medium (educational numerical correctness), owner Book 1 manuscript maintainers. Decision repair accumulation/coordinate/financial arithmetic, expose actual payoff discounting and constrain/disclose CDF behavior. Reviewer: automated execution and mathematical/prompt/step review, not external independent acceptance. Corrected revision is the containing publication commit.

One workflow,40 local answers and twelve lab steps are separate from four exact-source command records,52 supplemental predicates and twelve existing unittest methods. Zero historical unique methods added. [results.json](results.json) retains raw stdout/stderr, actual values/tolerances, model, Python/platform/SciPy versions, source/listing SHA256 and finite-grid lab outputs.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-integration-review/review.py
```

Reproduce unchanged source (expected nonzero exit; requires history):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-17-integration-review/review.py dd7886091994f886f0c6842a2a0bb3d7ff4e2b33
```

[baseline.json](baseline.json) retains22 failed predicates; the twelve existing tests and exact SciPy snippet already passed. Failures include overflow before quadrature weighting, underflowed positive outputs, wide/repeated/unrepresentable coordinates, exponential overflow before multiplication by a small cashflow, irrelevant overflow for zero cashflow, payoff-density product overflow, typed integrand/PDF/coordinate handling and panel validation bypass at CDF(0).

Some baseline predicates mark explicit contract additions rather than violations of original promises: nonnegative density and finite typed payoff checks, new rate/horizon keywords for the misleadingly named formerly undiscounted payoff helper, and CDF domain restriction to|z|≤6. Unsupported discount keywords originally raised TypeError; the reference had no discount feature. The original prose already disclosed extreme-tail cancellation. The correction does not claim that relative-tail accuracy is solved; within-domain CDF error remains unbounded by this code, and specialized tail functions are still required for tail-sensitive work. Twenty-two failed predicates are not22 distinct defects. No observer failures occurred.

## Source execution and independent expectations

Four isolated commands execute the verbatim demonstration/twelve tests, silent import, compilation and separate verbatim SciPy quad snippet. A second unchanged-snippet execution permits supplemental inspection of returned polynomial/cashflow values against rational/Decimal expectations. SciPy's reported error is not an independent correctness certificate. No supplemental quadrature implementation replaces source execution.

For x² on[0,1], exact finite composite rules are midpoint M_n=1/3−1/(12n²), trapezoid T_n=1/3+1/(6n²), Simpson S_n=1/3. Source n2/10/100 outputs match these independently derived finite-grid formulas. For x⁴, Simpson S_n=1/5+2/(15n⁴), checked at n10/20; this supports the smooth leading-error factor16 on halving spacing. Midpoint/trapezoid leading error scales as n^-2, hence factor4 on doubling panels. These are smooth polynomial identities, not universal guarantees for kinks, discontinuities or oscillation.

Cashflow fixture C100 currency/year, horizon2 years, constant continuous rate.05/year: analytic PV=2000(1−exp(−.1)), evaluated independently with Decimal100. Source Simpson result and SciPy quad match within recorded budgets. Zero-rate PV200 is distinct. For the numerical stress fixture C1e−308,r−400,T2,n1000, integrand grows by q=exp(.8) each panel. The finite Simpson oracle is C*h/3*[1+q^n+4q(q^n−1)/(q²−1)+2q²(q^(n−2)−1)/(q²−1)], h=.002. It is not the limiting integral C(exp(800)−1)/400; using that limiting value as a strict finite-grid oracle would misclassify ordinary quadrature error.

Uniform[0,1] terminal payoff max(x−.5,0) has undiscounted expectation1/8. Explicit continuous discount rate.05/horizon2 gives exp(−.1)/8. Defaults0/0 retain prior expectation behavior. PDF normalization/valuation measure remain caller responsibilities; a nonnegative integrand alone does not validate a probability model. Product-scale stress uses a uniform density1e308 over a tiny interval≈1e−308 and payoff1e308; multiplication and integration precede final float reporting.

Normal CDF±1 uses independent standard-library erfc references; density0 uses a high-precision known constant. Missing normal mass outside[−3,3] is erfc(3/sqrt2)≈.00269979606326019, retained as a supplemental tail calculation, not infinite-domain source quadrature. Source normal CDF remains zero-centered Simpson on a restricted domain; no arbitrary tail/error certificate is inferred.

## Numeric and domain contracts

Input/callback types are finite Python int/float, booleans excluded. Nodes come from rational binary endpoint coordinates before rounding and must remain distinct, with midpoint nodes interior. Unrepresentable integer coordinates reject rather than losing input identity. Public fixed-grid rules require increasing bounds; orientation reversal is conceptual or explicit negation of a swapped-domain result. No fixed-grid tolerance/error-bound/automatic refinement API is implemented.

Callback values retain integer/displayed-decimal quantities through rational weights and accumulation. Own financial wrappers combine rational payoff/density/quadrature with Decimal100 exponentiation before final float conversion. Required nonzero final values cannot silently underflow; all final values must be finite. Exact accumulation does not undo error already inside a user callback or establish model validity. Nonfinite typed callbacks, negative densities, invalid panels, unsupported normal-CDF tails and unreportable outputs reject. Cashflow wrapper validates the original horizon under the same float-coordinate protocol. Zero cashflow avoids irrelevant exponentiation.

## Forty worked-answer records

| Exercise | Review and execution boundary |
|---|---|
| 01 | Source Simpson constant1 on[0,3]=3. |
| 02 | Source midpoint/trapezoid linear integral1/2. |
| 03 | Source finite quadratic rules compared to exact1/3 and each rule's finite-grid formula. |
| 04 | Source Simpson cubic1/4. |
| 05 | Reversed-limit sign identity correct mathematically; public rules deliberately reject reversed bounds. Negate swapped-domain result explicitly. |
| 06 | Source one-panel midpoint linear1/2. |
| 07 | Source one-panel trapezoid linear1/2. |
| 08 | Source two-panel Simpson quadratic1/3. |
| 09 | Source odd Simpson panel count rejects. |
| 10 | h=(2−0)/10=.2, analytic spacing review. |
| 11 | Rational nodes1/4,3/4 for two midpoint panels; source quadratic n2 uses them. |
| 12 | Trapezoid nodes0,.5,1; source n2 benchmark. |
| 13 | Simpson n4 weights1,4,2,4,1; implementation/general formula reviewed. |
| 14 | Smooth polynomial trapezoid leading error1/(6n²) derives factor4; source finite-grid formula checked. |
| 15 | Source quartic Simpson1/5+2/(15n⁴), n10/20, derives factor16. |
| 16 | Simpson cubic exact in exact arithmetic; source agrees within floating report budget. |
| 17 | Split jumps/kinks when possible; uniform payoff kink at.5 is aligned on chosen even grid. No automatic split detection. |
| 18 | Singular/improper integrals need special handling; conceptual, no such source routine. |
| 19 | Normal density total mass1 analytically; source does not integrate infinite domains. |
| 20 | Source CDF0=.5 with panel validation even on zero branch. |
| 21 | Source CDF−1+CDF1=1; cancellation symmetry is not tail-accuracy proof. |
| 22 | Source density0 versus independent constant; general formula reviewed and bool rejected. |
| 23 | Uniform mean1/2 via source linear rule. |
| 24 | Uniform second moment1/3 via source Simpson. |
| 25 | Supplemental exact variance1/3−1/4=1/12. |
| 26 | Source undiscounted uniform payoff1/8; distinction from discounted amount explicit. |
| 27 | Source optional payoff discount returns exp(−.1)/8 for rate.05,T2. |
| 28 | Source zero-rate continuous PV=CT=200. |
| 29 | Constant-rate analytic formula reviewed and source positive-rate cashflow compared to independent Decimal value. |
| 30 | −expm1(−x) is stable float conventional alternative; new source uses Decimal exp/high precision internally. |
| 31 | Source C100,T2,r.05 PV versus2000(1−exp(−.1)). |
| 32 | Variable cashflow integral correct; source cashflow wrapper only constant intensity, generic quadrature accepts supplied variable integrand. |
| 33 | Risk-neutral pricing requires appropriate measure/no-arbitrage assumptions; no measure calibration/acceptance. |
| 34 | Density-weighted source expectation implemented; nonnegative checks do not certify normalization or measure choice. |
| 35 | Mass.98 requires tail/model investigation, not automatic renormalization; conceptual, no general PDF certification. |
| 36 | Supplemental normal missing tail mass≈.00269979606326; no source infinite integral. |
| 37 | Low-dimensional quadrature/Monte Carlo comparison conceptual; no simulation implemented here. |
| 38 | Tensor-grid m^d complexity analytic; source scalar only. |
| 39 | Refinement difference not absolute error certificate; source returns no rigorous bound. |
| 40 | Domain, panels, units, methods, runtime, benchmark and tail limits retained; independent approval absent. |

## Twelve lab-step records

Prerequisites: Python, callable finite typed integrands, increasing representable bounds, positive integer panel counts/even Simpson panels, integrable model over chosen domain. Financial time is years with compatible continuous rate/intensity; probabilities require a valid normalized density supplied by caller. SciPy is installed for the separate example. No actual market/as-of inputs exist.

| Step | Actual evidence and limit |
|---|---|
| 1 | Verbatim source saved isolated; runtime/source/listing hashes retained. |
| 2 | Source midpoint x²,n2/10/100 versus finite M_n. |
| 3 | Source trapezoid same panels versus finite T_n. |
| 4 | Source Simpson same even panels versus1/3. |
| 5 | All three finite outputs and independent1/3 limit distinguished. |
| 6 | Recorded panel refinement/formula errors; quartic n10/20 provides separate Simpson-order benchmark. |
| 7 | Source cubic Simpson1/4. |
| 8 | Source CDF±1 versus erfc and symmetry; restriction/tail limits explicit. |
| 9 | Source constant continuously paid cashflow fixture. |
| 10 | Independent Decimal analytic PV and exact SciPy snippet; large negative-rate stress uses a separate finite-grid oracle. |
| 11 | Source undiscounted1/8 and explicit discounted exp(−.1)/8; same uniform model, separate outputs. |
| 12 | Four exact commands,52 supplemental predicates and twelve existing methods pass;22 baseline failed predicates retained. |

## Limits and resume checkpoint

Local Linux CPython/SciPy only. No adaptive refinement, automatic singularity/kink detection, infinite-domain source integration, rigorous truncation/roundoff/error bounds, relative-tail CDF acceptance, general probability/market measure approval, production performance, broad shared-input integration, notebook/platform or external independent certification. Known tail limitations remain open within comprehensive numerical review; restricting domain is not resolving them. Source execution, independent finite-grid/analytic derivations and conceptual designs remain separate above. F28/F32 and all unresolved tracker findings remain open.

Chapter17 has eight core workflows and315 local answers scoped. Next: Section17.9 — Interpolation; resume from fresh main without duplication.
