# Section 18.3 — Reproducible simulation: scoped review

Baseline `dec9471c2922ca82f4f0b28c61137bb7ff0bc0fa`; reviewed 2026-11-08 by Codex, not an external independent reviewer. [Source](../../chapter-18/18.03-reproducible-simulation.md). One workflow, forty local answers and twelve lab steps. No new historical unique methods.

From repository root:

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-reproducibility-review/review.py
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-18-reproducibility-review/review.py dec9471c2922ca82f4f0b28c61137bb7ff0bc0fa
```

The second command intentionally exits1 and requires the baseline git object. [Baseline](baseline.json) retains six failed supplemental predicates; [corrected results](results.json) retains the passing rerun, complete stdout/stderr, commands, SHA256 of source/listings, manifests/digests and runtime. Six exact-source commands pass in both runs: four verbatim Python listings, quiet reference import and compile. Ten existing methods execute in the reference listing. The 63 supplemental predicates are not 63 new unittest methods, workflows or exercise answers.

## Finding F175 and contract decisions

The original additive tolerance rule can accept an error larger than the limit when **both sides overflow to infinity**, and can falsely pass a subnormal boundary when the tolerance product rounds up. Oversized integer probability/comparator inputs raise OverflowError rather than the otherwise stated ValueError. These are substantiated numerical/validation defects.

Two of the six baseline failures additionally establish an **explicit displayed-decimal boundary policy**, rather than claiming the original binary-float interpretation was inherently invalid: `(1.1,1,.1,0)` and its negative analogue now pass the exact displayed-decimal inequality. The source documents its interpretation (`Fraction(str(float))`, exact integers), finite input range, boolean exclusion, and asymmetric reference scale. This rule is additive `atol+rtol*abs(reference)`, not math.isclose's maximum-scale rule. Rational comparisons avoid overflow/underflow in intermediate bounds. Probability comparisons also use displayed-decimal probability against the actual binary uniform draw. No claim of perfectly continuous Bernoulli sampling; the 53-bit grid caveat is explicit.

No source test was removed or rewritten to hide failure. No observer defect occurred in this batch. The normal/terminal-reporting fixes from18.2 and the serialization correction there remain separate historical records.

## Exact execution, supplemental derivation, design review

The four source listings executed unmodified per recorded revision: local uniform demonstration, state restoration assertion, NumPy two-child spawning example, and reference manifest/demo/tests. Source function calls in the observer are supplemental invocations. Additional state reset, extra-draw, duplicated reset-per-path and stream assignment probes are supplemental implementations, not newly published chapter APIs.

Independent arithmetic: E[X]=.6×110+.4×90=102; at p=.5 it is100. Given an observed count k in N, mean=90+20k/N exactly. The observer derives that value with Fraction. It replays the **same** random.Random generator to verify count/mapping, so that count is not an independent randomness oracle. No threshold requiring sample mean102 or independent seeds to have different means is imposed.

Independent expected encoding explicitly orders manifest fields and assembles the representation, then compares source bytes and digest. This still uses Python JSON scalar encoding and hashlib SHA256; it is not an independent hash implementation or a portable canonical-JSON proof. The known SHA256 of `{}` and literal `{"a":1,"b":2}` encoding provide fixed fixtures. Key order, changed fields, excluded/added timestamps, and distinct encodings for1 and1.0 are checked. A changed digest prompts field/byte investigation, not an automatic accusation of bad data. Arbitrary non-string key manifests and external audit schema enforcement are outside this fixed source-generated manifest contract.

A supplemental paired example uses X=[110,90,110,90], Y=[120,100,120,100]. Differences are constantly10 and have sample variance0, while separately adding the two sample variances yields a positive value. This verifies why paired differences matter; the source exports no paired-SE API. Pairing can also increase difference variance for oppositely responding outputs, so no universal variance-reduction promise is accepted. Floating-point nonassociativity is demonstrated separately.

The fixture uses fictional one-period annual simple returns, initial100 and common-currency terminal110/90. There is no external dataset, market timestamp or calibrated real-world/risk-neutral measure. Horizon/units/code hash/command are retained here and in JSON alongside the intentionally small source manifest; the source now states its omitted metadata. The manifest hash does not automatically hash code/data. Model conventions and provenance remain prerequisites for real use.

Environment: CPython3.12.14, Linux; NumPy2.3.5/PCG64, parent seed42, spawn keys[0]/[1], task assignments0/1 and five draws each are retained. Version/platform differences and actual parallel scheduling are not exercised. This is single-process stream-construction/replay evidence, not deployment or independence acceptance.

## Twelve lab-step contracts

| Step | Prerequisite/action and actual evidence |
|---|---|
| 1 | Python available; implementation/version/platform recorded in JSON and source manifest. |
| 2 | Exact final fence saved in isolated temporary reproducible_simulation.py; assumptions fixed to110/90 and one-period simple returns. |
| 3 | Independent Fraction expectation at p=.6 is102. |
| 4 | Seed42,N10000,p.6: k5957, mean101.914. Full canonical manifest and digest retained; digest `e01929a9367342d652ee617ccc88fb4b30bae184f179c18e6e494effe840d62e` in this environment. |
| 5 | Repeated identical source inputs: manifest and digest equality; independent field-order encoding compared. No cross-platform guarantee. |
| 6 | Seed43,N10000,p.6: k6027, mean102.054; parameters and digest differ. Observation, not proof of independent replications. |
| 7 | p.5 with seed42,N10000: k4990, mean99.98; independent expectation100. |
| 8 | N1000,seed42,p.6: k580, mean101.6; full new manifest/digest retained. No guarantee each larger run is closer. |
| 9 | Exact source state assertion plus supplemental twenty-draw save/restore replay passed. Compatible state format only. |
| 10 | Supplemental extra draw shifts the selected twenty-draw sequence by one, demonstrating mapping dependence. No source file artificially mutated. |
| 11 | Ten existing reference methods, quiet import/compile and all other source examples passed; baseline/corrected results separate. |
| 12 | Seed/state/operation order, parameters, generator/runtime, source checksum, command and fixture convention recorded; statistical/model/platform/acceptance limits documented below. |

## Forty prompt-to-answer alignment records

All forty source prompts/answers were read. Conceptual statements are reviewed as such; no runnable API is invented for them.

| Answer | Scoped disposition |
|---|---|
| 1 | State, algorithm, operations, inputs and compatible environment: correct exact-replay contract; selected replay observed. |
| 2 | Seed alone insufficient: correct; other fields must accompany it. |
| 3 | Different generators need not match equal seeds: correct compatibility statement. |
| 4 | Extra draw advances state: shifted sequence probe. |
| 5 | Local generator reduces shared-state interference: global-state preservation checked. |
| 6 | Restore state replays from that point: source assertion and twenty-draw probe. |
| 7 | Mean102: independent exact rational expectation. |
| 8 | Mean100 at p.5: independent exact rational expectation. |
| 9 | Finite estimate need not equal102: observed101.914; no statistical quality threshold inferred. |
| 10 | Reset each path can repeat draw: supplemental duplicate first-draw demonstration. |
| 11 | Same-seeded workers risk duplicated streams: same construction as reset-per-path; actual parallel execution not claimed. |
| 12 | Different seeds do not prove independence: correct limit. |
| 13 | Parent seed, child mapping, generator/configuration: source NumPy and supplemental assignments recorded. |
| 14 | Worker count/assignment can affect replay: correct design warning; no scheduler experiment claimed. |
| 15 | Checksum identifies hashed bytes: literal/digest fixtures. |
| 16 | Hash does not prove correctness: correct conceptual limit. |
| 17 | Sorted keys stabilize chosen representation: source digest equality and explicit encoding. |
| 18 | Timestamps vary and should be separated from deterministic comparisons: adding different timestamps changes identity in probe. |
| 19 | 100.01 vs100,atol.02 passes: source comparator plus rational rule. |
| 20 | 100.02 vs100,atol.01 fails: source comparator plus rational rule. |
| 21 | Absolute tolerance useful near zero: explicit zero-reference probes. |
| 22 | Floating addition nonassociative: supplemental large-cancellation example. |
| 23 | Numerical agreement need not imply identical bytes: correct distinction; comparator accepts nonidentical values. |
| 24 | Statistical agreement does not require same draws: correct definition; no formal replication-agreement test claimed. |
| 25 | Fixed seed assists debugging/regression: selected replay/digest probe supports example. |
| 26 | Replications assess sampling variability under assumptions: correct; different-seed outputs recorded without independence certification. |
| 27 | Sampling cannot remove model bias: correct model distinction. |
| 28 | Replay does not prove model correctness: correct; benchmark review separate. |
| 29 | Common random numbers pair configuration comparisons: correct design concept; supplemental paired vectors illustrate. |
| 30 | Paired differences determine paired SE: constant-difference rational variance0. |
| 31 | Pairing not guaranteed to reduce variance: correct covariance-dependent statement. |
| 32 | Dataset source/version/time/units/identity: valid design requirement; no external dataset in this fixture. |
| 33 | Sensitivity reveals dependence on assumptions: p.6→p.5 model expectation102→100 illustrates. |
| 34 | Python version helps compatibility: recorded; not sufficient by itself. |
| 35 | Code revision identifies implementation: baseline/current SHA256 retained outside minimal source manifest. |
| 36 | Manifest digest does not automatically hash external data: correct; no external-data hashing claim. |
| 37 | Simulation PRNG unsuitable for secret tokens; cryptographic source needed: conceptual purpose review, no security testing. |
| 38 | Changed digest requires comparing fields/inputs: changed seed/count/p representations retained; no automatic correctness conclusion. |
| 39 | Illustrative results are not execution evidence: this batch supplies actual command output, separately labeled. |
| 40 | Reproducibility does not replace model validation: correct scope boundary. |

## Resume and open scope

Next: **Section18.4 — Simulating Financial Outcomes**. Chapter18 has three scoped workflows and120 local answers, not full acceptance. F28 notebook/platform, F32 shared-input integration, F165 CDF tails, rare-event/stream independence, broader branch/input tests, financial model/editorial/copyright and external independent acceptance remain open. No production or external messaging actions. Automation continues while feasible tracked work remains; do not treat this review as certification.
