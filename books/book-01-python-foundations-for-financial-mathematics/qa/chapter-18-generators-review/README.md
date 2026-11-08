# Section 18.2 — Random number generators: scoped review

Baseline: `6b97432aee50e8bd1216c1498ed9453645baaa46`. Source: [18.2](../../chapter-18/18.02-random-number-generators.md). Date: 2026-11-08. Reviewer: Codex, not an external independent reviewer. Fictional annual simple-return model, initial common-currency value 100, returns +10%/−10%, up probability .6. No market data, valuation date, calibrated measure or production model approval.

Run from the repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-generators-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-generators-review/review.py 6b97432aee50e8bd1216c1498ed9453645baaa46
```

The second command intentionally exits 1 and regenerates the original failures; it requires the baseline git object. [Baseline](baseline.json) and [corrected results](results.json) include source/listing hashes, full command output, environment, explicit predicate results and tolerances. Eight exact-source command records passed in each run: six verbatim Python listings (including both NumPy examples), quiet reference import and reference compile. The reference demo invokes ten existing unittest methods; those ten remain ten unique methods, not eight workflows or 78 tests. One workflow, 40 local answers and twelve lab-step records were reviewed. The corrected run passes 78 supplemental predicates; the baseline fails thirteen. No historical unique methods added.

## Findings and provenance

F174: original terminal arithmetic loses `10**18 + 1` when formed from initial `10**18` and return `1e-18`; zero-SD normal draws also lose the original integer mean. Normal output can be infinite despite finite inputs; nonzero terminal values and variance can underflow silently. Huge integer inputs or unreportable variance leak OverflowError, and noniterable samples/outcomes leak TypeError. Corrected finite numeric/reporting helpers normalize these cases to ValueError, preserve exact integer reports, use rational displayed-decimal arithmetic for model quantities, and guard generated affine normal outputs. All ten original methods still pass. Source now explicitly documents representability restrictions: e.g. an unreportable variance raises even if its square root could be reported. This deliberately narrows the original ambiguous contract.

One of the thirteen baseline failures is a **new policy probe**, not a defect under an already explicit promise: unused terminal branches now need not be reportable. Both returns are validated, but only outcomes actually present are computed. Empty outcomes return an empty list. Normal sampling now applies a guarded affine transform to standard-normal draws, which can change last-bit results relative to direct `normalvariate(mean, sd)`. These choices are documented rather than silently advertised as identical arithmetic.

[Initial observer failure](observer-initial-failure.txt) records a Fraction JSON serialization error before the first evidence write; serialization alone was corrected and all baseline/source probes rerun. It is separate from the thirteen manuscript/policy predicates, not an additional source failure. No failed attempt was relabeled a pass.

## Evidence boundaries and independent expectations

Exact-source execution comprises the six fenced listings and two module commands. The runner's additional calls execute the source functions, but its expected values and state/spawn demonstrations are **supplemental probes**, not additional manuscript implementations or new exported methods.

Independent algebra: for ideal continuous U, E[U]=integral(u du)=1/2 and Var(U)=1/3−1/4=1/12. For X∈{90,110}, E[X]=.4(90)+.6(110)=102 and Var(X)=.4(90−102)²+.6(110−102)²=96. Normal variance is .15²=.0225. A sample SD of 10 with N=10000 gives SE=.1; four times N halves SE under the IID/finite-variance assumptions. For independent standard normals, Var(ρZ1+sqrt(1−ρ²)Z2)=1 and Cov(Z1,Y)=ρ; these are algebraic checks, not an executed joint-normal source API.

For each observed up count k at N=1000, independent rational count formulas give mean `90+20k/N`, unbiased variance `400k(N-k)/(N(N-1))`, and SE equal to the square root of variance/N. Uniform/normal sample statistics are separately recomputed with Fraction/Decimal; relative arithmetic tolerance is 1e-12 with zero absolute tolerance. These are arithmetic tolerances, **not statistical acceptance bands**. Binary Python uniforms lie on a 53-bit grid, so arbitrary probabilities only approximate the ideal Bernoulli law.

Seeded replay, threshold mapping, state restoration, duplicate-worker and spawned-stream checks use the same generator libraries. They do not independently validate randomness, distribution quality, stream non-overlap or statistical independence. The NumPy examples actually ran with 2.3.5/PCG64; child assignments 0–3 and spawn keys/draws are recorded. Python was 3.12.14 on Linux. No cross-version/platform replay claim.

## Twelve lab-step contracts

Prerequisites: Python with standard library; NumPy is optional for the chapter but present in this run. Save the final reference fence as random_generators.py, preserve seed/count/operation order, and interpret returns as decimals and SD as SD. No notebook/server/parallel deployment is implied.

| Step | Action, evidence and outcome |
|---|---|
| 1 | Recorded Python/platform, random.Random, seeds 2026/42/43/44, NumPy/PCG64 and source hashes in JSON. |
| 2 | Extracted exact final fence to isolated temporary random_generators.py; import was silent. |
| 3 | Source uniform_draws(1000,2026): every value in [0,1); mean .4983659359955837, unbiased variance .08027719072879945. |
| 4 | Compared descriptively with .5 and 1/12≈.0833333. Sampling discrepancy is recorded, not used as a deterministic pass/fail quality threshold. |
| 5 | Recreated identical local generator and operations; full list equality. Global random state unchanged. |
| 6 | p=.6,N=1000,seed42: k=580, frequency .58. p=0/1 endpoint checks passed. |
| 7 | Source terminal mapping gives 110/90, mean101.6 and SE .31231000230145933; count formulas checked. Analytical expectation102 remains separate. |
| 8 | Seeds43/44 yield k=607/599, mean102.14/101.98, SE .30905649308163047/.31012219490996734. Observed variation; no proof all seeds differ or estimates are independent. |
| 9 | Source normal_draws(.05,.15,1000,42): mean .051545071072600854, sample SD .14938620509469047. Source summary and independent sample arithmetic compared. |
| 10 | Zero of these 1000 normal draws below−1. This does not prove zero tail probability. R=−1.1 gives terminal−10 in the supplemental elementary formula; source terminal_values explicitly forbids that return. No tail truncation performed. |
| 11 | Ran verbatim SeedSequence.spawn example and supplemental ten-draw child replay/assignment checks; identically seeded workers demonstrated duplication. Finite non-duplication is not independence certification. |
| 12 | Ten existing methods, import/compile and all other exact examples passed. Baseline and corrected supplemental runs retained; broad QA remains open. |

## Forty local prompt-to-answer records

All forty prompts and stated answers were read in source order. Numerical checks refer to runner labels; conceptual rows are design/algebra reviews, not fabricated runtime tests.

| Answer | Alignment and validation |
|---|---|
| 1 | Deterministic given state: correct PRNG definition; conceptual. |
| 2 | Seed initializes state: correct; conceptual. |
| 3 | Draw advances state: correct; state/extra-draw probe supports the example. |
| 4 | Same state and operations replay in compatible implementation: state restoration observed. |
| 5 | random() in [0,1): source range checked; API definition reviewed. |
| 6 | Ideal uniform mean .5: independent integral. |
| 7 | Ideal uniform variance1/12: independent second-moment derivation. |
| 8 | P(U<.6)=.6 under ideal uniform: correct with ideal qualifier; finite grid caveat retained. |
| 9 | p=0 gives zero: source endpoint checked. |
| 10 | p=1 gives one: source endpoint checked. |
| 11 | 100(1+.1)=110: source mapping/count oracles. |
| 12 | 100(1−.1)=90: source mapping/count oracles. |
| 13 | .6(110)+.4(90)=102: independent rational expectation. |
| 14 | SD.15 implies variance.0225: rational square. |
| 15 | Sample mean need not equal target: observed discrepancy; conceptual general claim. |
| 16 | Sample variance need not equal target: observed discrepancy; conceptual general claim. |
| 17 | Equal seeds across libraries do not guarantee equality: correct compatibility limitation; not a universal numerical inequality claim. |
| 18 | Extra draw changes later position: selected stream probe. |
| 19 | Local generator reduces global interference: source global-state preservation checked. |
| 20 | random.Random is not a security-token source; secrets is appropriate: conceptual library-purpose review, no security certification. |
| 21 | Long period alone insufficient: correct design distinction. |
| 22 | Same-seeded workers may duplicate: duplicate NumPy streams demonstrated. |
| 23 | Different seeds do not prove independence: correct; observed different draws are not used as proof. |
| 24 | Documented spawning provides supported children: exact NumPy example and supplemental assignments executed. |
| 25 | Independent streams do not automatically model correlated assets: correct model distinction. |
| 26 | ρ=0 gives Y=Z2: direct substitution. |
| 27 | ρ=1 gives Y=Z1: direct substitution. |
| 28 | ρ=−1 gives Y=−Z1: direct substitution. |
| 29 | ρ=1.1 invalid: domain check; source provides formula, not callable correlation validator. |
| 30 | s10,N10000 gives SE.1: exact rational arithmetic. |
| 31 | Fourfold N roughly halves SE: algebra under same variance/IID assumptions, not a guarantee of closer individual estimate. |
| 32 | More draws do not remove model bias: correct conceptual distinction. |
| 33 | Return below−1 yields negative terminal in elementary formula: supplemental R=−1.1 illustration. |
| 34 | Discarding lower-tail draws changes distribution: correct conceptual conditioning/truncation point. |
| 35 | Passing a finite mean check does not prove quality: correct evidence limit. |
| 36 | 102 is model-specific analytical benchmark: independently derived. |
| 37 | Constant sample SE0 with at least two observations: source check. |
| 38 | NumPy version helps reproduction: captured version/generator, not seed-only guarantee. |
| 39 | One draw is not a forecast: correct modeling interpretation. |
| 40 | Model, seed, generator and software version are valid records; inputs/results also needed: captured for scoped fixture, acceptance provenance still broader. |

## Remaining scope / resume

Proceed to **Section 18.3 — Reproducible Simulation**. Chapter18 now has two scoped workflows and80 local answers; later workflows/answers remain. No chapter-wide acceptance or full Book1 certification. F28 notebook/Windows/macOS/server platform gaps, F32 shared-input integration, F165 CDF-tail limits, rare-event/statistical validation, broader branch coverage, copyright/editorial/model and external independent acceptance remain open. No production or external messaging actions performed.
