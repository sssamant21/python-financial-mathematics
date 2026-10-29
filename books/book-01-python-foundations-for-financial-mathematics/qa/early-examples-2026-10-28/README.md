# Book 1 — Chapters 1–3 uncovered-example validation

**Status: bounded mapping batch complete; V05/V06 remain IN PROGRESS.** Reviewer/owner: Codex. Recorded 2026-10-28. Source revision: `ea555618814bccae45297a59418ca39b5c1294b9`. All chapter manuscript bytes are unchanged by this work.

## Disposition of the 430 initial gaps

| Disposition | Source fences | Evidence / limit |
|---|---:|---|
| Included in passing scoped runtime workflows | 405 | 98 explicitly configured workflows; exact source payloads retained |
| Placeholder / pseudocode, not run | 23 | Ellipsis or generic `statement` bodies; no complete financial algorithm or termination contract |
| Input-evaluation antipattern, not run | 1 | Section 1.10 explicitly warns against `eval(input(...))`; static disposition only |
| Deliberately invalid typing example | 1 | Mypy 2.4.0 reports the three expected argument-type errors |
| Total classified | 430 | No Chapter 1–3 fence remains in the no-exact-mapping queue |

The [current full-book ledger](current-coverage-ledger.json) still has **169 fences without an exact execution mapping**, elsewhere in Book 1. The earlier 543 unchanged historical selections, 16 source fences from the first gap-closing batch and two loop-context fragments remain separately identified. Counts describe source selection/disposition, not line/branch coverage or completion of every lab step and answer.

A function definition can execute without executing its body. Grouped examples can overwrite earlier names. The source-inclusion label therefore does not claim that every expression, branch or input domain was independently checked. Explicit fixture assemblies and expected outputs/states are recorded in [early_plan.py](early_plan.py). No undefined names were silently guessed at runtime. Common `Decimal`, rounding, `math` and `sys` prerequisites are supplied by the harness; source-specific constants, inputs and supporting blocks are declared in each plan. Some examples run with controlled callback/predicate or security-record test doubles. Those cases demonstrate bounded control-flow behavior, not a real refinement solver, data-processing callback or portfolio model.

## Actual checks and outcomes

| Scope | Actual result |
|---|---|
| Chapter 1 | 52 workflow cases passed, covering 128 previously unmapped source fences |
| Chapter 2 | 31 workflow cases passed, covering 173 previously unmapped source fences |
| Chapter 3 | 15 workflow cases passed, covering 104 previously unmapped source fences |
| Valid typed Section 3.7 lab | Mypy 2.4.0 `--strict --no-incremental` exited 0 with no issues |
| Invalid Section 3.7 calls | Mypy exited 1 with exactly three `[arg-type]` diagnostics for arguments 1, 2 and 3, as expected |

The final 98 runtime workflows all exited zero with empty stderr and passed the stated assertions/output checks. Six workflows expect and check a specific exception type: XOR applied to a float, division by zero, a call before definition, duplicate argument binding and two nonpositive compounding-frequency cases. Additional manuscript-contained exception assertions remain intact. Deliberately wrong percent-unit, precedence and simple-versus-compound examples retain their erroneous calculations; the checks demonstrate their difference from the intended benchmark and do not endorse the formula.

The checks also cover controlled input conversion, formatting, simple/compound arithmetic, fee rounding, reconciliation, finite/nonfinite values, bounded loops, cash-flow traces, nested loops, missing/zero handling, default arguments, mutation, scope, closures, annotations, composition and Decimal context. Million-addition float and Decimal examples both ran with bounded expectations. One additional docstring example executed via doctest and passed. A closed-form rational benchmark checks the range-based cash-flow valuation; its exact numerator/denominator is `8284000 / 9261`, with a declared Decimal tolerance.

These are **98 workflow cases**, not 98 new unittest methods. The earlier 13 gap-closing workflows plus this batch make **111 supplemental workflow cases**; the two static checker cases are separate. The existing **2,996 reference-method total is unchanged**. The final run includes three additional boundary/loop cases beyond the preliminary 95-case run; preliminary reruns are not added again.

## Harness failures and remediation — F25

**Severity:** Low (validation infrastructure). **Owner:** Codex. **State:** RESOLVED for this batch. No manuscript correction was indicated by these failures.

The first attempt completed 67 subprocess checks: 60 passed and seven failed. Five failures came from incorrect newline escaping in the new oracle strings. One came from combining two while-loop examples with shared state, and one from an incorrect hand-entered expected present value. Assembly then stopped before workflow 68 because the harness selected the exercise file instead of its companion solution file. [Initial configurations, outcomes, output and errors](initial-harness-attempt.json) are retained, including source-payload hashes. This incomplete first attempt is not counted as a completed validation run.

The harness now validates oracle/fixture syntax and target source indices before execution, selects companion files explicitly, uses the rational valuation benchmark, and separates the while-loop cases so each tested body executes with its declared starting balance. Supporting function definitions are ordered explicitly before dependent calls. The corrected 83-case run passed, the expanded 95-case run passed, and the final 98-case run passed. [Final structured results](workflow-results.json) and [combined runtime output](runtime-output.log) are the acceptance evidence for this scoped batch. Static results/output are retained in [typing-results.json](typing-results.json) and [typing-output.log](typing-output.log).

## Reproduction and integrity

Use an isolated CPython 3.12 environment with [requirements.txt](requirements.txt). The observed environment is recorded in [environment.json](environment.json). From this evidence directory, choosing new temporary output directories:

```bash
python run_early_examples.py ../.. /tmp/book1-early-reproduction
python check_early_typing.py ../.. /tmp/book1-typing-reproduction
python classify_early_coverage.py ../.. /tmp/book1-classification-reproduction /tmp/book1-early-reproduction/results.json /tmp/book1-typing-reproduction/results.json ea555618814bccae45297a59418ca39b5c1294b9
```

The runner extracts original fences without modifying their contents, assembles declared prerequisites in separate subprocess workspaces, removes inherited Python path overrides, supplies controlled stdin and sets a 20-second timeout per runtime case. It catches expected exception types explicitly. The static checker has a 60-second per-case timeout. The supplied runtime `eval` calls in Section 3.5 evaluate only fixed manuscript strings for argument-binding demonstrations; the warned-against external-input `eval` example is not executed.

The classifier verifies current fence hashes against both the initial ledger and the actual run records; all 430 gaps must receive a disposition, all 405 runtime source identities must match, and the total remains 1,160 fences. [Source-manifest hashes](source-manifest.json) cover all 356 chapter/companion/index Markdown documents. The [per-fence dispositions](early-dispositions.json) expose the exact scope. Original mapping evidence remains in [the first V05/V06 report](../coverage-and-labs-2026-10-28/README.md).

## Remaining work

Next are the **169 unmapped later-chapter fences**: Chapter 4 (49), Chapter 5 (4), Chapter 7 (40), Chapter 8 (21), Chapter 11 (2), Chapter 13 (5), Chapter 14 (3), Chapter 15 (1), Chapter 16 (1), Chapter 17 (15), Chapter 18 (9) and Chapter 21 (19). The separate lab-step/answer queue from the initial coverage report remains open. This batch does not complete independent financial/mathematical review, all worked-answer proofs, installed packaging, notebooks, external data, Windows/macOS or supported-version runtime acceptance. No Book 1 certification is implied.
