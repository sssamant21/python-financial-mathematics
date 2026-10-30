# Section5.6 — eight dependency exercise answers

Exact source helpers/fixture code, new orchestration and conceptual promotion/retention policies are distinguished per record.

## 5.6-E1 — SOURCE_HELPERS+SUPPLEMENT

**Prompt:** Change the report fixture requirement to an unavailable unit-demo version. Verify installation fails before claiming the environment is ready.

Original fixture_wheel generates a report requiring unavailable book1-unit-demo2.0.0 while wheelhouse has only unit1.0.0. Offline resolver fails with specific requirement diagnostic; both imports remain absent. A separate approved wheelhouse uses original report requirement1.0.0; normal install with unit1 constraint succeeds, pip check and unchanged original behavior code pass. Both failed and corrected artifacts/metadata/outputs retained; no required version was silently loosened in source.

## 5.6-E2 — SUPPLEMENT

**Prompt:** Add a constraints file limiting the unit fixture to 1.0.0. Explain why that file alone does not request its installation.

constraints.txt limits book1-unit-demo==1.0.0. Install -c constraints with no requirement fails at-least-one-requirement and installs neither fixture. Requesting report1.0.0 with -r and -c causes its declared dependency to be resolved under the constraint. Constraint is a candidate restriction, not an installation request.

## 5.6-E3 — SOURCE_RUNTIME

**Prompt:** Add a check comparing the interpreter reported by sys.executable with the path invoked by the lab.

Explicit child sys.executable equals exact invoked runtime/bin/python (lexical path, not symlink-to-base identity). Prefix matches owned venv and differs base_prefix; pip --version recorded via same executable. Activation/shell prompt is not proof of actual interpreter.

## 5.6-E4 — SUPPLEMENT+DESIGN

**Prompt:** Explain why --no-deps would defeat the initial dependency-resolution demonstration.

--no-deps suppresses the transitive-resolution lesson. In a separate fresh runtime report-only no-deps install succeeds, but pip check fails missing unit and import raises ModuleNotFoundError. Reinstall normal report requirements resolves unit and restores metadata plus original quantity behavior. Metadata and import failures remain visible; no-deps is not universally invalid when a separately complete environment is deliberately prepared.

## 5.6-E5 — SOURCE_INSTALLED

**Prompt:** Add an installed behavior test that explicitly preserves Decimal zero and a fractional quantity.

Original report/unit sources installed from locally generated wheels, external isolated imports confirmed beneath selected sys.prefix. Zero0 and fractional12.50 retain exact Decimal type, instrument_units label and scale exponents0/-2. Installed versions both1.0.0; source original valid/invalid BEHAVIOR_CHECK runs before and after repairs. No arithmetic/valuation inferred.

## 5.6-E6 — DESIGN+INVENTORY

**Prompt:** Describe what a freeze inventory omits about source data, numeric policies, and platform reproducibility.

Recorded freeze identifies installed version state, not consumed financial source/input snapshots, units/currency/sign/as-of rules, precision/rounding, interpreter binary/platform libraries, artifact approval/trust, or external services. Retain those separately. Freeze output here is inspection evidence, not a portable lock or full analysis record.

## 5.6-E7 — DESIGN

**Prompt:** Explain why importing decimal does not require a distribution named decimal.

decimal is Python standard library, supplied with this base runtime; the local fixture needs no distribution named decimal. Import spelling is not a reliable pip distribution name. Explicit Decimal behavior executes successfully in fresh venvs without installing such a distribution; unsupported Python builds still need platform setup review.

## 5.6-E8 — DESIGN

**Prompt:** Propose evidence needed before promoting an external dependency version change into a financial application.

Before external dependency promotion retain old/candidate requirements and artifacts/hashes, approved source/provenance, target Python/platform/build constraints, release/compatibility/security review and independent known-value/invalid-input/numeric/context/CLI regression evidence. Review changed outcomes against declared financial policies, then document migration and rollback/recreation. Synthetic fixture pass is not approval for any external version; no upgrade of a real dependency or production workload executed.
