# Section5.12 — formal project review

29 derived records:11 acceptance criteria,10 test-purpose mappings and8 workflow/prerequisite units. These are review records, not29 tests or unique workflows.

## ACCEPT-01 — Reusable API

financial_inflows.analyze re-exported from core; source eight-method suite runs against installed code in external runtime. Input/config bytes validated; no new API change.

## ACCEPT-02 — Explicit input

Both entry points require --input/--config. Missing arguments produce nonzero status and no stdout, independently probed in both fresh retained-wheel runtimes.

## ACCEPT-03 — Defined calculation

10.005+20.005=30010/1000USD, exact rational cents ties-to-even gives3001=30.01. Source sums then quantizes once; per-record rounding would3000 cents. Existing bound/context tests rerun.

## ACCEPT-04 — Installable project

Unchanged pyproject declares setuptools84.0.0; exact original verifier builds a regular wheel. Separate declared dist build retains a wheel; no editable installation.

## ACCEPT-05 — Source separation

Exact src layout and explicit package discovery; no sys.path changes. Runtime tests copied outside project; fixtures passed via explicit absolute paths and not bundled.

## ACCEPT-06 — Installed validation

Exact original verifier eight methods passes; same retained wheel installed into two further fresh venvs, each runs unchanged copied eight-method source suite. These24 invocations represent8 existing unique methods.

## ACCEPT-07 — Import evidence

All original/retained runtime checks require package under child purelib. Raw origin/prefix JSON retained for both follow-up runtimes; not merely an import from source checkout.

## ACCEPT-08 — CLI parity

Installed python -I -m financial_inflows and generated console command output identical bytes and independent expected complete schema. Both fresh retained-wheel runtime checks pass.

## ACCEPT-09 — Failure behavior

Missing args and malformed[ JSON return nonzero with empty stdout and specific diagnostics. Expected errors retained separately from unexpected-failure count0.

## ACCEPT-10 — Repeatable tooling

Builder3.12.14/pip25.0.1/setuptools84.0.0 recorded, backend wheel matched fetched PyPI metadata. Project builds/installs local --no-index/--no-deps/--no-build-isolation. This is not byte-reproducible independent builds.

## ACCEPT-11 — Cleanup

Original verifier cleanup message inspected; its context manager removes temporary wheel/runtime. Additional owned work/runtime directories absent after context. Deliberately retained wheel remains in QA artifacts for reuse, with recorded hash.

## TEST-MAP-01 — Known answer

Complete output schema/30.01 checked in source tests and external CLI; independent rational computation supplies expectation.

## TEST-MAP-02 — Distribution metadata

Source test reads book1-financial-inflows0.1.0 from installed metadata; imported financial_inflows and console financial-inflows are distinct namespaces.

## TEST-MAP-03 — Context isolation

Existing hostile precision2/ROUND_DOWN/Inexact trap test passes; local fresh precision28 sufficient for≤1000*1000000 and four-place addition. No arbitrary division/powers/numerical-domain claim.

## TEST-MAP-04 — Amount contract

Original negative tests reject unsupported amount texts and JSON types; grammar/domain limits are separate from wheel compatibility.

## TEST-MAP-05 — Identity and currency

Original tests reject duplicate/padded IDs, unknown fields and nonUSD; cannot infer completeness/authenticity of external input.

## TEST-MAP-06 — Schema/configuration

Exact policy object and duplicate JSON-member hook exercised by source suite. No implicit env override or silent coercion.

## TEST-MAP-07 — Bounds

Source tests accept1000 max rows→1000000000.00 and reject1001; bounded sum is not unbounded precision certification.

## TEST-MAP-08 — Input stability

Original bytes immutable and source-suite assertion retains inputs; all extracted project files compared by SHA before/after builds and acceptance.

## TEST-MAP-09 — External installed import

Fresh venv regular install, external copied tests and -I origin address flat-checkout masking. No arbitrary PYTHONPATH repair or editable substitute.

## TEST-MAP-10 — CLI parity/failure

Module/console parity, missing required args, malformed-input no-success boundary checked; no exception suppression or successful zero-total fallback.

## WORKFLOW-01 — Prerequisites

Python3.10+ source syntax with venv/ensurepip; actual3.12.14 Linux. Fresh temporary project; preserve exact names. Source files outside disposable builder/runtime. No previous lab imports required.

## WORKFLOW-02 — Assemble exact listings

All11 paths reconstructed: metadata/README/gitignore, four package modules, test, two fixtures, verifier. Per-file SHA values recorded; synthetic source-side tests/fixtures not installed package resources.

## WORKFLOW-03 — Prepare builder

Prior scratch builder absent, so recreated dedicated builder through existing provenance-checking prepare script; downloaded exact84.0.0 and verified published SHA. Shared interpreter not modified. Existing F13 remains resolved, no backend guard loosened.

## WORKFLOW-04 — Run original verifier

Unchanged verifier invoked by explicit builder path from outside project; ROOT derives from file. Require actual8 tests/OK and return0, then read origin/hash/CLI/failure/cleanup evidence.

## WORKFLOW-05 — Retain artifact

Run declared local pip wheel build into empty dist. Check exactly one wheel and archive contains financial_inflows/core.py but no tests/fixtures; persist exact bytes/digest. No public upload.

## WORKFLOW-06 — Recipient-style validation

Install exact same retained artifact into two fresh local environments. Pip check, origin, source eight-method suite, both entry points, bad args/malformed input and quiet imports pass. No independent human recipient or different platform implied.

## WORKFLOW-07 — Review troubleshooting

Backend/version errors corrected by declared builder, missing pip/venv by supported setup; stale-source/entry-point issues addressed by regular install and explicit origin. No simulated missing backend/console fault in this batch.

## WORKFLOW-08 — Limit acceptance

No source-distribution rebuild, signing, dependency-update assessment, supported OS/version matrix, static checker, untrusted backend sandbox, production or registry release. Quiet output check does not prove absence of all application file reads; extension4 remains pending.
