# Section 6.13 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling listings; exact caller-owned NumPy Generator, bounded positive exact integer dimensions, compatible PCG64 checkpoint and explicitly retained draw protocol. Review: Codex executor, 2026-10-30; no independent statistical/model acceptance.

## 6.13-E1

Add a test that an invalid Generator argument fails without constructing a hidden replacement stream.

**EXACT SOURCE REJECTION + SUPPLEMENTAL FACTORY TRAPS**. Pass None, integer 42 and a plain object to innovations. Each raises TypeError at the exact-Generator guard. During these calls only, supplemental traps on np.random.default_rng and the module make_rng record no invocation and would fail if used as replacement factories; finally restores both originals. Source review confirms the first executable guard raises before dimension checks or a draw, with no hidden construction path. The traps cover those named factories, not a general proof about arbitrary implementations. No replacement stream is returned or used.

## 6.13-E2

Save a checkpoint before a draw and verify two restorations reproduce the same continuation locally.

**EXACT SOURCE CHECKPOINT CALLS + SUPPLEMENTAL DEEP COPIES**. Create PCG64 with seed 20261030, deep-copy its state before a (4,2) standard_normal float64 draw, then restore independent deep copies into two fresh compatible generators. Both source continuations exactly match the original draw locally; the original successful call advances state and the saved checkpoint stays unchanged. This is tested on the recorded NumPy/Python/build, not a durable cross-version compatibility promise or rollback guarantee after allocation/library failure.

## 6.13-E3

Create three child streams with stable logical names and record the name-to-child mapping.

**EXACT SOURCE CALLS + SUPPLEMENTAL STABLE TASK MAPPING**. Spawn three children once from SeedSequence(20261030). Assign fixed mapping batch-alpha→child0/spawn_key[0], batch-beta→child1/[1], batch-gamma→child2/[2]. Each owns a PCG64 Generator and one (3,2) standard_normal float64 request. Record root entropy, index, spawn key, full pre-draw state and draw-byte hash in replay-manifest.json. Recreate the same mapping and execute tasks in reverse name order; each logical task reproduces its original batch. Ordering tasks after assignment can change while the name-to-child mapping stays fixed. Allocation-order or partition changes require a new protocol. All execution is serial; no live worker/thread/distributed scheduling or statistical independence is established.

## 6.13-E4

Explain why running the same seed in every worker does not create the intended distinct experiment streams.

**EXACT SOURCE DUPLICATION COUNTEREXAMPLE + CONCEPTUAL STREAM REVIEW**. Constructing a fresh generator with seed42 in each of three logical workers, then making the identical (3,2) request, repeats the same batch locally. That is duplicated pseudorandom work, not the intended distinct task streams; copying an initialized mutable state into processes can have the same problem. The three spawned controlled child batches differ, which verifies this fixture mapping only, not a proof of statistical independence or an impossibility of repeated values. Use stable logical child assignment and retain task progress; operating-system worker identity or shared root seed alone is insufficient.

## 6.13-E5

Compare a saved innovation matrix under two scale assumptions without redrawing it.

**SAVED ARTIFACT + SUPPLEMENTAL TRANSFORMS**. Save the original (4,2) innovation matrix in innovations.json with explicit dtype, shape, C-order element-byte hash and JSON values. Reload it exactly, compare round-trip bytes, then compute low=0.01*z and high=0.02*z from that same saved matrix without redrawing. Source bytes remain unchanged, outputs do not share storage with z, and high agrees with 2*low at rtol1e−15/atol0 for the controlled scaling check. These coupled assumptions share draws; they are not independent experiments, calibrated returns or a demonstrated variance-reduction method.

## 6.13-E6

Write a replay manifest containing method, algorithm, seed/state, shape, versions, and task assignment.

**PERSISTED SUPPLEMENTAL MANIFEST + EXACT SOURCE REPLAY**. replay-manifest.json records local schema/scope, Python/NumPy/platform/byte order and NumPy build configuration, source/listing hashes, Generator/PCG64, initialization seed, full compatible checkpoint before the first draw, method standard_normal, dtype float64, shape(4,2), call index0, logical task, completed draw count and half-open scenario row range[0,4), innovation artifact/hash and child-task mapping/checkpoints/output hashes. Replay from the serialized state reproduces saved element bytes; JSON artifact digest and each child checkpoint replay are checked. This manifest is a concrete local QA example, not a universal interchange format, transactional checkpoint store or trusted input parser. No executable state is loaded from an untrusted source; the JSON is generated by this runner. Restoring numerical state alone does not recover external task/sink progress; an application needs consistent code/input/configuration versions and atomic progress/output checkpoints.

## 6.13-E7

Propose statistical checks for a larger sample while stating chance-failure behavior and the claim being tested.

**STATISTICAL TEST PLAN ONLY — NOT EXECUTED**. For a larger predeclared sample, state the null as the requested standard-normal innovation distribution under the chosen draw protocol, not calibrated market returns. Fix sample size, shape, seed/task allocation, diagnostic methods and rejection thresholds before observing draws; do not retry seeds until passing. Check mean, variance with a stated denominator, tail/bin frequencies and distributional shape; add lag/cross-column diagnostics for the dependence claims actually being assessed. For illustration, under independent N(0,1) draws the mean has variance1/n; Chebyshev gives P(|mean|>=sqrt(1/(n*alpha)))<=alpha, a conservative predeclared chance-failure bound, not a calibration test for all distribution features. For variance or goodness-of-fit tests, specify the null distribution, quantile/method, estimated parameters and justified significance level; adjust for multiple tested features/streams or report an exploratory scope. A valid generator can fail a random diagnostic by chance, and a pass cannot prove normality, independence or generator quality. Retain failures and investigate against predeclared rules rather than tightening/relaxing gates after seeing the sample. No larger-sample moment/distribution/dependence test or Monte Carlo acceptance is run in this batch.

## 6.13-E8

List the additional assumptions needed to turn these innovations into a financial price-path simulation.

**FINANCIAL PRICE-PATH MODEL DESIGN ONLY — NOT EXECUTED**. Specify asset/state identities and units, time grid/calendar/day-count/horizon, initial prices and observations, data as-of/adjustment/provenance, dynamics (including whether innovations act on log prices, returns or other states), drift and measure, volatility calibration, dependence/correlation and positive-semidefinite handling, jumps/tails/default/recovery, corporate actions/distributions, currency/FX, path constraints and discretization/numerical-error policy. State parameter-estimation uncertainty, validation/benchmark criteria, scenario probabilities/weights if used, seed/stream protocol and common-draw coupling across comparisons. An additive normal simple-return assumption can imply below−100% returns and must not be silently turned into a positive-price model by clipping; a log-price model changes assumptions and needs its own derivation. Financial risk/performance/valuation conclusions require the relevant payoff, costs/cash-flow and model review. This batch executes generator mechanics only, with no price simulation, financial calibration or independent model approval.
