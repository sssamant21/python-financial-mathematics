# Section 5.12 — six remaining local exercises

E2 (malformed CLI input) and E3 (retained wheel/fresh runtime handoff) already have [project evidence](../chapter-05-project-review/README.md); their queue records are unchanged. Prerequisites: Python 3.10+, venv/ensurepip, retained exact original wheel and writable owned temporary directory. Actual CPython 3.12.14/Linux. This batch does not build a new distribution.

## 5.12-E1 — SUPPLEMENTAL_COPY

**Prompt:** Add a new public function without breaking analyze and its existing output schema.

Add reports.inflow_count(data_raw, config_raw) -> int, returning the count only after analyze validates all records and configuration. Export it explicitly beside analyze; preserve the existing analyze signature arguments, runtime errors, five-key result schema, rounding/context/ownership and CLI behavior. Execute the original eight-method suite before and after modifying an owned installed package copy; run independent expected count 2 and total 30.01, invalid later-record/config/empty-data checks, explicit exports and input/context stability. This is a disposable supplemental copy of an installed wheel, not a rebuilt or released distribution; original artifact bytes and manuscript remain unchanged.

## 5.12-E4 — EXACT_INSTALLED_SOURCE+INTENTIONAL_MUTANT

**Prompt:** Add a test proving import of the package is quiet and performs no application file access.

Run a fresh isolated interpreter against the unchanged regular installed wheel outside the checkout. Preload observer dependencies, capture package/CLI stdout/stderr and deny common application open/read/write/stat/exists interfaces. An open audit hook permits importlib get_data code loading and rejects other open events; normal imports have empty captured streams. Add a deliberate top-level Path(...).read_bytes() to the temporary facade: the same test raises APPLICATION_FILE_ACCESS with no success report. Restore exact facade bytes and rerun successfully. Run again on the supplemental API/type copy. Import loader reads are expected; this is regression instrumentation for these imports, not an OS sandbox or proof covering arbitrary native/kernel access. The implementation was also read: import-time statements define/export code, while CLI file reads remain in main.

## 5.12-E5 — DESIGN_NOT_RUN

**Prompt:** Design a source-distribution rebuild check that installs no code from the checkout.

Source-distribution acceptance plan: build one retained sdist using declared pinned backend in a prepared isolated builder; record its exact digest, archive members and build evidence. Unpack into a new controlled root after checking paths/symlink policy; make the original checkout unavailable. From that unpacked sdist only, build a wheel in a second clean prepared builder with approved backend artifacts/no uncontrolled index downloads. Install the resulting regular wheel into a third fresh runtime, run copied external tests and explicit fixtures under isolated Python, verify origin/purelib, metadata, pip check and both CLI paths, including malformed/missing input failures. Assert no editable install, PYTHONPATH/sys.path adjustment, cwd import, source checkout path or hidden fixture dependency. Compare contract results to independent expectations, retain sdist/wheel/build/runtime commands and failures. Equality of wheel bytes is a separate reproducible-build claim, not required by this behavioral plan. No sdist build or rebuild was executed here.

## 5.12-E6 — SUPPLEMENTAL_COPY

**Prompt:** Add typed result records or a documented TypedDict while preserving runtime validation.

Document AnalyzeResult as a TypedDict with required currency Literal[USD], count int, total str, method Literal[sum_then_round] and rounding Literal[ROUND_HALF_EVEN]. Total is fixed two-place text under the runtime contract; annotations cannot encode all grammar/range/financial guarantees. In the disposable copy, change only the core return annotation and add its type import; keep original calculation and validation code identical. Execute original regression suite and check runtime type hints/required fields, original known result and malformed amount rejection. Demonstrate AnalyzeResult(currency=EUR) constructs an ordinary incomplete dict without runtime enforcement; do not use this constructor as validation. No static type checker or packaged py.typed distribution contract was run/created.

## 5.12-E7 — DESIGN

**Prompt:** Define a version-change policy for a deliberate change to rounding stage or supported currencies.

Project policy proposal: treat a changed rounding stage or changed meaning/units/schema/error contract as a breaking semantic change, even if values match on some fixtures. For the current pre-1.0 teaching package, designate 0.2.0 for a deliberate breaking contract and require migration notes plus side-by-side old/new golden cases; after a declared stable 1.x contract use the next major version for incompatible behavior. Prefer a separately named/versioned method or explicit configuration over silently reinterpreting analyze. Adding supported single-currency labels may be additive only if old inputs/results/errors remain valid and currency handling is fully specified; previously mixed/unsupported inputs require explicit new policy, without summing incompatible units or implying FX. Label the chosen financial contract in output, preserve prior artifact/policy records and review dependency/runtime/metadata changes. This is a proposed project policy, not a registry rule or release action.

## 5.12-E8 — DESIGN_NOT_RUN

**Prompt:** Explain which checks must be added before publishing to a public registry.

Before a public release, review distribution-name availability/ownership, project metadata/readme/license and attribution, intended API/version policy, source/dependency provenance and integrity, secrets/private-data scan, sdist contents/rebuild and wheel contents, declared Python/platform/dependency support and actual test matrix, external regular-install/API/CLI/error/origin checks, docs/examples/accessibility, resource limits and financial numerical contracts. Reconcile open findings, obtain the required independent review/acceptance and define release/rollback/support ownership and authenticated publication controls. Check the target registry current requirements at release time; no registry availability/compliance is asserted now. No upload, public release, credential provisioning or production action occurred. F28/F32 and wider acceptance are unresolved.
