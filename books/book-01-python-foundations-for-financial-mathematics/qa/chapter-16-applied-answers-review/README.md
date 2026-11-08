# Section 16.16 — scoped final answers and applied-case review

Baseline assessment manuscript: `affb1442a6416ddce58240601a5045a266d1a913`. One assessment workflow, all50 chapter-wide answers, five applied cases, twelve final-lab steps and seven rubric-area records reviewed within the limits below. These are separate from local-section prompts, test predicates, core workflows and historical unique methods.

Run from repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-applied-answers-review/review.py
```

Reproduce unchanged-assessment failures (requires baseline in Git history; intentionally exits nonzero and writes baseline.json):

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-16-applied-answers-review/review.py affb1442a6416ddce58240601a5045a266d1a913
```

The runner extracts the exact assessment Python fence, runs its printed twelve unittest methods, checks silent import and executes printed compileall in isolation. Final results.json: three successful commands,78 passing supplemental predicates, raw output, hashes, runtime/platform and independent rational/Decimal expectations/tolerances. No new historical unique methods. Its metadata records zero local prompts and50 chapter-wide answers.

## Baseline, correction and source boundaries

baseline.json retains20 failed predicates against unchanged assessment source; all twelve original methods already passed. F157 corrects Exercises17–19's half-gradient answers and Exercises20–22's downstream labels, implicit relative budget tolerance/residual amplification, integer mean/sample loss, moment overflow, tiny drift-return loss, large-NAV turnover, false total-loss reporting and output/container contracts. One PSD-extension predicate adds full-matrix screening beyond the original disclosed limit. Exercise31 now correctly calls its ordered counts compositions rather than integer partitions, and caseD's doubled SD rounds to28.22%, not28.23%.

observer-failure.json separately retains the initial QA AttributeError: a template replacement had pointed the linked project stress call at Section16.16, which has no stress export. Restoring the linked path to Section16.15 corrected the observer; no assessment source change was involved. No complete baseline report was emitted before the error. To reproduce in a throwaway copy, set the observer's file15 variable to16.16-exercises-and-applied-problems.md. Baseline/final predicate inventories use the corrected observer.

The assessment adopts the project's integer/displayed-decimal rational arithmetic,80-digit Decimal roots, absolute unit-budget tolerance1e-10 with normalization, full scale-relative Schur-complement covariance screen, exact requested-form nonnegativity and finite/nonzero-preserving output contracts. Required report fields must all be representable. VC/RC outputs reconcile to variance/SD within relative1e-10, no absolute floor. Zero-risk RC remains None. Positive wealth cannot be reported as a total loss, and frictionless turnover is formed from weight changes before dollar conversion.

The full numerical PSD screen is not exact model certification. Real IDs/timestamps/horizon/currency/NAV/forecast vintage remain external contracts. Supplied synthetic cases do not establish empirical model accuracy or independent acceptance.

## Linked exact source execution

results.json records source/listing hashes for five additional current chapter files and16 individual calls:14 successful results and two expected rejections. Those call records are separate from three assessment commands and twelve assessment unittest methods; no other unittest suite is counted as rerun.

| Source | Executed calls |
|---|---|
| Section16.9 | minimum_variance_weight, target_return_weight and expected infeasible-target rejection. |
| Section16.12 | sharpe_ratio, expected zero-volatility rejection, two dominates comparisons and simplex_grid. |
| Section16.13 | two check_constraints proposals and two necessary_budget_bounds conflicts. |
| Section16.14 | three band_trigger cases. |
| Section16.15 | stress(k=2). |

These are current-source local calls on labelled synthetic fixtures, not external implementations or independent reviewer acceptance. Replaying a baseline assessment revision uses the linked files in the checkout; their exact hashes are recorded. The baseline commit already contains these corrected linked sources. A strict whole-tree replay can be made in a throwaway checkout of that baseline with this observer copied in.

## Independent references and all50 answers

Rational sums/quadratics, two-asset complete-square reasoning, signed exposure formulas and high-precision roots independently establish expectations. Source exports are used where available; normalization/gaps/derivatives/fees are supplemental derivations, not invented assessment functions.

| Answers | Scoped review |
|---|---|
| 1–6 | Supplemental positions[40,35,25]/NAV100 normalize to[.4,.35,.25]; signed net1/gross1.4; source drift return.01 for[.4,.6]/[.1,−.05]; source base mean.059; supplemental covariance.03 and inverse correlation.1. |
| 7–12 | Source two-asset variance.03168/SD sqrt(.03168), perfect-positive SD.25, exact negative-correlation hedge0; linked GMV9/13 and assessment mean22/325≈.0676923 at that allocation. |
| 13–16 | Asymmetric input is invalid; [[1,2],[2,1]] has eigenvalues3,−1 and new full screen rejects. Source base variance.019916/SD≈.1411240589 verified. |
| 17–22 | Correct unconstrained derivatives2*Sigma-w=[.0436,.06,.00016]. VC problems now identify Sigma-w=[.0218,.03,.00008] as covariance-weighted exposures/half-gradients; source VC=[.0109,.009,.000016] remains correct. No assessment gradient export claimed. |
| 23–26 | Source VC sum.019916 and RC_A=.0109/sqrt(.019916) checked. Linked Sharpe.3; zero-risk Sharpe rejects. |
| 27–31 | Linked strict dominance/tradeoff, target threshold.75, infeasible.10 target and ordered simplex grid count15. Continuous target-minimum follows the quadratic/GMV argument, not arbitrary-grid certification. |
| 32–37 | Supplemental position/sector gaps and net/gross; linked sector exposure.8, individual caps and independent-bound conflicts checked. No signed portfolio-stats or full mandate solver added to assessment API. |
| 38–43 | Source drift.05, weights[11/21,10/21], supplemental NAV105. Separate written NAV100 trades[10,−10], turnover.1, source-derived gross20; supplemental gross-notional fee.001*20=.02. |
| 44–48 | Linked absolute-band trigger/nontrigger; linked engine2x SD/4x variance stress agrees with direct assessment4*covariance route. Source sample covariance2; supplemental T60 sample denominator59. |
| 49–50 | Deposits are external flows, not investment returns; code presence/unrun tests do not establish runtime or independent certification. Conditional instructional question remains valid despite the scoped executions now recorded here. |

## Five applied cases

| Case | Executed evidence and limit |
|---|---|
| A endowment | Assessment mean.059, variance.019916, SD≈.1411241 and contributions; linked individual cap.45 fails at equity.50, supplemental gap.05. Fictional institution only. |
| B two-asset GMV | Linked A weight9/13; assessment mean22/325≈.0676923, variance9/325≈.0276923. GMV misses.07. Linked equality threshold.75 and assessment target variance9/320=.028125; independent convex quadratic proves minimum for w≥.75. No independent/empirical optimizer acceptance. |
| C drift | Assessment NAV100→105 and weights[11/21,10/21]; source frictionless trades[−2.5,2.5], turnover1/42. Linked.05 band does not trigger. Trade calculation is a forced-rebalance counterfactual, not a policy-generated order. |
| D stress | Linked project stress2 and direct assessment4*covariance agree on variance.079664 and SD≈.2822481178, rounded28.22%. Correlation/liquidity/nonlinear-tail changes omitted. |
| E governance | Linked budget/position-cap checks pass but sector.8 breaches.7. Assessment mean.059 misses.06 by.001. These synthetic checks grant no real mandate exception or execution approval. |

## Twelve final-lab steps and seven rubric records

| Step | Evidence and limit |
|---|---|
| 1–2 | Isolated exact listing, Python/platform, source/listing hashes retained. |
| 3–5 | Base mean/risk and both attribution vectors checked against independent rational/root references. |
| 6 | Source three-observation sample covariance2; precision/overflow/underflow probes separately retained. |
| 7 | Linked analytical solver and independent9/13 derivation; target.75 checked under same zero-covariance model. |
| 8–9 | Assessment drift→frictionless rebalance chain at shared synthetic t1 NAV105. No flows/fees/fills. |
| 10 | Linked position/sector checks; expected-return floor checked from assessment mean. |
| 11 | Linked/direct stress routes compared under same model. |
| 12 | Three commands, twelve methods,78 predicates and linked-call records retained; observer/source failures distinguished. |

Rubric records are evidence mappings, not awarded mastery points: weight/return arithmetic(15)→budgets/means; covariance/risk(20)→quadratics/sample; risk contributions/diversification(15)→VC/RC/stress; efficiency/constraints(15)→GMV/target/dominance/caps; drift/rebalancing(15)→NAV/trades/turnover; Python/tests(15)→exact execution/hashes; assumptions/governance(5)→model labels/limits. Nominal rubric total100; no independent grade, certification or accreditation is assigned.

## Limits and resume checkpoint

Local Linux CPython standard library only. Exact source assessment/linked calls are separate from supplemental formulas and conceptual/economic reviews. No actual IDs, as-of forecasts, calendars/FX/NAV/financing, real mandate/source integration, costs/taxes/orders/fills, unseen-period strategy evidence, production performance/conditioning, platform coverage, independent reviewer acceptance or certification. F28 notebook/platform, F32 broader shared-input integration and newer unresolved findings remain open.

Chapter16's listed formal scope is recorded: fifteen core/project workflows plus one assessment workflow,426 local-section answers,50 chapter-wide answers, five applied cases and twelve project-checklist records (Section16.15). This is scoped review completion, not comprehensive acceptance. Next: Chapter17 Section17.1 — Why Numerical Methods Are Needed.
