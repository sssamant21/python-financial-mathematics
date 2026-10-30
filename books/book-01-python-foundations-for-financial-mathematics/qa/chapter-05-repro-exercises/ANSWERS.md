# Section 5.11 — eight scoped exercise answers

Prerequisites: Python 3.10+, writable owned temporary/output directories; no third-party dependency. Actual CPython 3.12.14/Linux. The runner reconstructs the original four sibling files, uses explicit interpreter/paths and separates the original source from experiments.py. Numerical expectations use integer units and quotient/remainder half-even rounding independently of the Decimal implementation.

## 5.11-E1 — SOURCE+INTEGER_ORACLE

**Prompt:** Add a third inflow and independently derive the expected rounded total.

Append CF-3 USD 0.005 to 10.005 and 20.005. In units of 0.0001 the exact sum is 300150; dividing by 100 gives 3001 cents plus a halfway remainder 50. Half-even increments odd 3001 to even 3002 cents: USD 30.02. Exact original analyze and CLI agree with the integer benchmark and count 3. Input and output snapshots are retained.

## 5.11-E2 — SOURCE+INTEGER_ORACLE

**Prompt:** Add a boundary test at 1,000 rows and at the maximum permitted amount.

Construct 1000 distinct MAX-i rows, each USD 1000000.0000. Exact integer benchmark is 1000000000.00 with count 1000; original analyze and CLI agree. Reject 1001 rows and a single 1000000.0001 amount. This tests the joint maximum and just-outside bounds; it does not prove arbitrary-scale arithmetic. The largest sum has at most ten integer and four fractional places, comfortably inside the fixed 28-digit calculation precision. The repetitive maximum input is regenerated exactly by review.py; its consumed size/digest and actual output are retained.

## 5.11-E3 — SUPPLEMENT+INTEGER_ORACLE

**Prompt:** Implement a separately named round-each-then-sum experiment and show its different answer on the supplied fixture.

Separately named round_each_then_sum first reuses original schema/configuration validation, then rounds each Decimal to cents in its own precision-28 half-even context and sums. Original 10.005 and 20.005 independently round to even 1000 and 2000 cents, total 30.00, compared with sum-then-round 30.01. Supplemental method label is round_each_then_sum, never silently substituted into the original output artifact. Executed under hostile caller precision/rounding/Inexact trap; malformed negative inflow still rejected. This alternate procedure is a separate teaching policy, not a universal accounting preference.

## 5.11-E4 — SOURCE

**Prompt:** Change whitespace only in a copied input file; compare the result and digest.

Copied input adds only leading/trailing JSON whitespace. Decoded rows and original result remain equal; SHA-256 and full artifact differ only through input_sha256 for this controlled runtime. Original and whitespace bytes and both artifacts are retained; digest identity and numerical agreement answer different questions.

## 5.11-E5 — DESIGN+CONCRETE_MANIFEST

**Prompt:** Propose a bundle manifest that also identifies tests, documentation, and dependency artifacts.

Proposed versioned manifest entries identify normalized relative path, byte size, SHA-256, role and reviewed revision for input/config/source, tests, documentation, command evidence, generated output and interpreter/dependency artifacts. Add package name/version/filename/hash and origin/build policy for every actual dependency artifact; distinguish runtime from build dependencies and retain artifacts or an explicit retrievable retention location. Never infer no dependencies from pip freeze alone. The concrete evidence-bundle/manifest.json binds four exact lab files, outputs and copied inputs, identifies QA runner/extension/documentation hashes and a deterministic maximum-input generator/digest. dependency_artifacts=[] is scoped to this standard-library-only lab; interpreter/system binaries, a full repository and an authenticated trust root are not preserved. Manifest creation is evidence bookkeeping, not artifact signing or independent reproduction.

## 5.11-E6 — SUPPLEMENT

**Prompt:** Add schema validation for a loaded output artifact before accepting it as a completed run.

validate_artifact rejects unsuccessful process status before acceptance, parses UTF-8 with duplicate/nonfinite rejection and requires exact version/result/evidence keys and exact scalar types (bool is not accepted as int). Enforce count 1..1000, fixed USD/sum_then_round/ROUND_HALF_EVEN policy, canonical two-place nonnegative total within 1000000000.00, lowercase 64-hex digests, nonempty runtime strings and empty dependency profile. Bind input/config/source digests to retained bytes, runtime to the controlled runner, and result to a caller-supplied independent benchmark. Five actual CLI artifacts accepted. Mutated schema/types/policy/numbers/runtime/dependencies/digests, duplicated members, empty/truncated files and nonzero status are rejected. Passing schema is necessary but not sufficient; exit status plus reviewed bindings/benchmark are required. This is not a signature or attestation that code was unchanged in memory.

## 5.11-E7 — SOURCE+RESEARCH_NOTE

**Prompt:** Write a research note explaining what the local repeat test establishes and what remains untested.

Question: same-currency untimed total of supplied synthetic nonnegative USD inflows. Fixed policy: sum all supplied precision then round half-even to cents; known result 30.01, contrasted with separately labeled 30.00 policy. Two subprocess runs of the same retained code/input/config on this CPython 3.12.14/Linux environment produce byte-identical complete validated artifacts. Original nine-method suite passes. This establishes local deterministic repeat execution and snapshot/benchmark agreement only. It does not establish independent reproduction, economic suitability, market-data availability, timing, FX/discounting/outflows, stochastic robustness, security, cross-platform support or certification. Initial QA filename collision and correction are retained under F34; source correctly refused overwrite.

## 5.11-E8 — DESIGN_NOT_RUN

**Prompt:** Design a fresh-kernel notebook acceptance procedure without using hidden interactive variables.

Fresh-kernel procedure: preserve notebook/source/input/config and dependency artifacts/hashes; use an explicitly selected kernel whose executable/prefix/origins match the prepared runtime; launch from documented working directory with controlled environment and no live endpoints; clear saved outputs, restart kernel, run all cells in order with a timeout and fail on error. Cells load explicit snapshots and import tested module functions, never assume variables from prior interactions. Validate resulting artifact schema, process/kernel success, bindings and independently derived results; rerun from another fresh kernel and compare claim-appropriate result/artifact levels while documenting runtime differences. Retain executed notebook, cell logs and kernel/runtime metadata. A notebook port, server/UI and kernel launch were not executed; F28 remains open, including other supported platforms and independent acceptance.

No manuscript file was changed. Local checks do not establish independent reviewer acceptance.
