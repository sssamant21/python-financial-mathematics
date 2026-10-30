# Chapter5 — twenty chapter-wide answers reviewed

Review reasoning is not an independent reviewer acceptance. SOURCE probes execute published functions; ORACLE uses rational arithmetic; INSTALLED executes published verifier and companion; DESIGN is conceptual.

## 5.13-P1 — Module responsibilities

**Prompt:** A script reads a file, validates records, aggregates amounts, and prints a report during import. Propose a module split and state what should happen on import.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** Core pure validation/aggregation, explicit file/argument CLI, guarded entry point. Import defines API without application file reads or printing. Quiet-import tests detect visible startup output, not all filesystem side effects.

Evidence: Companion1; installed quiet-import test supports only its observed boundary.. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P2 — Import names and distribution names

**Prompt:** Map book1-financial-inflows, financial_inflows, and financial-inflows to their roles. Explain why pip metadata and an import statement use different names.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**SOURCE:** Distribution book1-financial-inflows supplies import package financial_inflows and console command financial-inflows via financial_inflows.cli:main. Metadata identity and import spelling are different namespaces.

Evidence: metadata probes; installed metadata/base tests and CLI parity. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P3 — Quiet import acceptance

**Prompt:** Add an installed-package test that imports financial_inflows and financial_inflows.cli in a fresh subprocess and expects no output.

**Acceptance:** Supply executable checks and interpret their scope.

**INSTALLED:** Fresh isolated installed interpreter imports package and cli with empty stdout/stderr and return0. This does not instrument all file reads.

Evidence: ExtensionTests.test_quiet_import. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P4 — Interpreter selection

**Prompt:** A developer activates one environment but runs pip from another interpreter. Give a correction and evidence that identifies the interpreter actually used.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** Use absolute intended interpreter with -m pip; record sys.executable/version and package origin, compare with expected venv path. Activation changes shell lookup only. Current verifier uses explicit interpreters; no wrong-user-shell repair was executed.

Evidence: installed external origin and explicit-interpreter driver. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P5 — Environment recreation

**Prompt:** Explain why copying .venv is a weaker handoff than recreating a runtime from retained inputs. List what to retain instead.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** Recreate venv from supported Python/platform, source revision, approved artifacts/hashes, build/runtime requirements, configs/fixtures and tests. Environment path relocation and interpreter binary differences preclude claiming a copied venv is equivalent.

Evidence: new runtime creation in exact verifier; no relocation test claimed. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P6 — Build versus runtime dependencies

**Prompt:** Classify pip, setuptools, Decimal, and book1-financial-inflows in the project workflow. Explain why setuptools is absent from project.dependencies.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**SOURCE:** pip is frontend; setuptools84.0.0 is build backend; Decimal is standard library; built book1-financial-inflows is application. Runtime third-party dependencies=[]; build backend is not application dependency.

Evidence: pyproject probes; builder provenance and fresh runtime installation. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P7 — Version pins and artifact identity

**Prompt:** A pinned requirement is unchanged but its downloaded bytes differ. What additional evidence is needed, and what can a digest establish?

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** Retain approved artifact and digest from a separately trusted record with platform/build context. Pin names a release, digest identifies bytes, neither authenticates economic claims. Never approve unexpected bytes by regenerating expected hash.

Evidence: backend artifact matched version-specific PyPI metadata; not authorship certification. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P8 — Flat versus src layout

**Prompt:** Explain how a test can pass from a flat checkout even though a wheel omits the package. Propose a stronger acceptance route.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**INSTALLED:** Flat checkout imports can conceal omitted wheel content. Regular wheel, clean runtime, copied external tests, -I, no PYTHONPATH/PYTHONHOME and checked site-packages origin strengthen acceptance; src layout alone is insufficient.

Evidence: base/extended installed verifier logs. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P9 — Explicit input paths

**Prompt:** Add an installed CLI test that reads absolute input and configuration paths in a temporary directory while running from that directory. State what this proves.

**Acceptance:** Supply executable checks and interpret their scope.

**INSTALLED:** Companion uses absolute input/config in external temp cwd and isolated installed module; known total30.01. Proves this explicit-file path route, not bundled resources/remote permissions.

Evidence: ExtensionTests.test_absolute_external_cli_paths. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P10 — Configuration precedence

**Prompt:** Using Section 5.10 rules, file currency is EUR, environment currency is USD, and CLI currency is EUR. Give the effective currency/source. Repeat when the environment currency is empty.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**SOURCE:** Valid fileEUR/envUSD/cliEUR resolves EUR sourcecli. Empty env is present invalid and raises ValueError before winner selection; absent env is distinct. Strict all-layer validation is intentional.

Evidence: exact Section5.10 resolve probes. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P11 — Invalid CLI input

**Prompt:** Add an installed CLI test using an empty inflow list and the valid policy. Require nonzero exit, empty stdout, and an error identifying the violated contract.

**Acceptance:** Supply executable checks and interpret their scope.

**INSTALLED:** Empty inflows must nonzero exit, no stdout and expected1to1000 message. CLI preserves error boundary before print; production concise-error design is outside current test.

Evidence: ExtensionTests.test_invalid_cli_has_no_report; source rejection probe. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P12 — Environment labels and authorization

**Prompt:** A configuration says development but credentials permit production access. Is the workload isolated? Give concrete controls to review.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** development label grants no isolation. Review IAM/workload identity, account/project boundaries, endpoints/datasets, network restrictions and least privilege; venv only isolates dependencies. No remote access/authorization was tested.

Evidence: conceptual only. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P13 — Rounding stage

**Prompt:** Independently compute the total for USD 10.005 and 20.005 using sum-then-round and round-each-then-sum, both with half-even rounding to cents.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**SOURCE+ORACLE:** 10005/1000+20005/1000=30010/1000 USD. Rounded once gives3001 cents=30.01. Individually1000 and2000 cents (even ties) sum3000 cents=30.00. Difference0.01; rational integer-cent tie algorithm is independent of Decimal quantize.

Evidence: Fraction oracle plus eight source fixture comparisons. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P14 — Numerical context

**Prompt:** Explain why a caller precision of 2 with an Inexact trap must not change this project result. Give the bounds that justify its local context.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**SOURCE+ORACLE:** At most1000 nonnegative values≤1000000 with≤4 fractional digits give sum≤1000000000.0000, at most14 digit positions including fixed fractional scale; quantized result≤1000000000.00 needs12. Fresh precision28 context suffices for bounded addition/cent quantization; no division/powers. Caller precision2/ROUND_DOWN/Inexact trap and flags preserved.

Evidence: hostile-context and max-bound probes; installed context test. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P15 — Bytes versus meaning

**Prompt:** Add a newline to copied input bytes. Test input-digest inequality and equality of the validated result. Explain the two observations.

**Acceptance:** Supply executable checks and interpret their scope.

**SOURCE+INSTALLED:** Appended newline changes SHA256 bytes while JSON meaning and analyze output agree. Preserve both byte snapshots; hash equality is not semantic equivalence or authenticity.

Evidence: ExtensionTests.test_hash_identity_is_not_semantic_identity and source probes. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P16 — Research evidence limitations

**Prompt:** A run records input/config/source digests and returns the expected total. List four claims that remain unsupported.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** Digests/known answer do not establish authentic authorship, historical market availability, investment-hypothesis validity, or other-platform reproduction. Also not full repo/interpreter identity or crash-atomic research output.

Evidence: conceptual only; no independent research validation. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P17 — Compatibility review

**Prompt:** A proposed change renames total to amount and switches to round-each-then-sum without changing version or tests. Describe a review response.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**SOURCE+DESIGN:** Renaming total→amount breaks callers; changing rounding stage changes30.01→30.00. Require explicit compatibility/version/migration decision, updated semantic tests and possibly preserved old API/separate function. Current output keys/method checked, no change implemented.

Evidence: output schema/method and independent rounding expectations. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P18 — Diagnosis from evidence

**Prompt:** A package imports successfully but the console command is missing; separately, tests run but report zero cases. Give the next diagnostic step for each.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** Missing console: inspect project.scripts, installed entry-point metadata, explicit interpreter scripts directory; rebuild/reinstall correct wheel. Zero tests: inspect discovery filenames/startdir and actual nonzero count. No synthetic fault injection in this batch.

Evidence: installed verifier confirms actual8/12 discovery and CLI; diagnosis remains reasoning. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P19 — Release and retention plan

**Prompt:** Design a handoff for a retained wheel without uploading to a registry. Include what the recipient validates and what remains outside scope.

**Acceptance:** Give a concrete answer, explain its reasoning, and state relevant limits.

**DESIGN:** Retain wheel+trusted digest, supported platform/Python, source and dependency artifacts, fixtures/config and tests/commands. Recipient fresh-installs and checks origin, known/invalid cases, CLI parity, differences. This verifier deletes wheels; durable recipient handoff/reinstall and sdist rebuild remain future Section5.12 tasks.

Evidence: current temporary-wheel checks do not count as retained artifact handoff. Companion satisfies stated result/design and limits within recorded scope.

## 5.13-P20 — Integrated acceptance report

**Prompt:** Extend Section 5.12 with the four companion tests, rerun the installed-wheel verifier, and write an acceptance report distinguishing executed checks from proposals.

**Acceptance:** Supply executable checks and interpret their scope.

**INSTALLED:** Exact companion class inserted before existing guard, all eight original methods retained; only verifier success text8→12 changed. Final extended run actual12 tests plus both CLIs, origin, bad arguments, pip check and cleanup passed. Linux3.12 only; no independent certification.

Evidence: extended.log; results.json installed evidence. Companion satisfies stated result/design and limits within recorded scope.
