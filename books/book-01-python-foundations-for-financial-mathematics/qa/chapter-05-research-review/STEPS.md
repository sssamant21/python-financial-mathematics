# Sections5.9–5.11 — formal lab-step review

Twenty-four derived records cover three workflows; these are not24 new tests, original manuscript step numbers or independent acceptance decisions.

## 5.9-STEP1 — Prerequisites and exact layout

Flat local import project, Python3.10+ syntax, no third-party runtime dependencies. Package, fixtures and tests siblings at root; tests/test_layout.py discovered by explicit -s tests without requiring tests package. Avoid financial_layout.py/json.py name collisions.

## 5.9-STEP2 — Create files

Reconstruct all four Python listings plus exact JSON fixture, README and .gitignore. Per-file hashes retained. Source/fixtures outside environment; ignore rules neither untrack files nor enforce access controls.

## 5.9-STEP3 — Run local application

Module launched from root, explicit caller-relative input fixture. B0,A12.5,C3 yields A,C in source order; zero omitted from active IDs, not interpreted as missing. Quantities parsed from text, no float or valuation.

## 5.9-STEP4 — Absolute/external paths

Absolute project fixture and copied absolute external input both return same exact stdout. Package discovery stays in flat project root; this is not installed arbitrary-directory use.

## 5.9-STEP5 — Run discovery

Exact documented discover -s tests -v finds8 methods, OK, zero exit/no skips. Suite includes schema/types/duplicate IDs, full validation and path failures. An empty suite would fail this harness.

## 5.9-STEP6 — Import and ownership

Fresh normal package/module/entry imports quiet; source and all supplied files remain byte-identical after runs. Parent layout and import context intentionally preserved, no sys.path repairs.

## 5.9-STEP7 — Interpret errors and growth

Missing input propagates rather than selecting fixture; package discoverability distinct from input location. src migration/installed-artifact checks, output policy and nested-test discovery are separately queued extensions.

## 5.9-STEP8 — Scope

Ordinary wire quantity text may include Decimal exponent syntax; finite nonnegative validation follows parsing. No market-value ordering, wheel installation, external resources, static checker, Windows/macOS or independent acceptance in this batch.

## 5.10-STEP1 — Prerequisites and files

Four sibling source/test/config files in a fresh directory. No earlier lab file dependency; explicit required UTF8 JSON config. Child FINLAB settings cleared without changing parent process environment.

## 5.10-STEP2 — Precedence contract

defaults<required file<recognized process<CLI; validate all supplied recognized values even shadowed. Presence differs from empty; same selected value may have different provenance. Unknown JSON/override keys rejected, unrelated process variables ignored.

## 5.10-STEP3 — Baseline application

File completeUSD/development/2 plus CLI EUR yields EUR(cli),development(file),decimal_places2(file). Expected JSON independently stated; equal-to-default values remain file-sourced.

## 5.10-STEP4 — Process override

Controlled child FINLAB_ENVIRONMENT=test overrides file environment; selected source environment while other settings file. No environment variables or real credentials are changed in parent.

## 5.10-STEP5 — Run discovery

Exact default discover -v finds8 methods/OK/no skips. Original suite exercises defaults, validation of shadowed invalid settings, duplicate/unknown file keys and CLI behavior.

## 5.10-STEP6 — Failure boundary

Explicit --decimal-places3 fails with invalid decimal_places in cli and empty stdout; missing --config fails argument parsing with empty stdout. Raw nonzero error output retained. No conversion to zero/success fallback.

## 5.10-STEP7 — Ownership and import

Fresh import defines configuration/API and CLI without app output. Supplied files unchanged. Frozen settings object and source provenance are returned, not authorization grants.

## 5.10-STEP8 — Scope and secrets

CurrencyEUR is a label, not FX conversion; decimal_places is not implemented accounting rounding. Development label and Python venv do not restrict production access. IAM/network/resource controls require separate review; no remote access, shell changes, static checker or OS matrix executed.

## 5.11-STEP1 — Prerequisites and claim

Four sibling files: research.py,input,settings,test. No third-party runtime dependencies, remote data, clock/randomness or environment override. Define local repeat execution separately from independent reproduction/scientific robustness.

## 5.11-STEP2 — Numeric contract and independent expectation

Input10.005+20.005 gives30.010; half-even once at cents gives30.01, rounding each first would30.00. Independent Fraction integer-cent tie logic probes baseline,0.005,0.015 and1000 rows at1000000. Source precision28 ample for bounded≤14 digit-position sum; hostile precision2/ROUND_DOWN/Inexact trap does not govern result.

## 5.11-STEP3 — Run two experiments

Exact CLI invocations use distinct nonexisting run-a/run-b paths. No success stdout; return0 and identical UTF8 JSON bytes. Exact comparison command prints Identical run artifacts; this is same controlled runtime only.

## 5.11-STEP4 — Inspect evidence and hashes

Result schema values explicitly checked; input/config/source SHA256 recomputed from consumed exact extracted files. Source digest is research.py only, not repository/interpreter/test authenticity. Retained result artifacts include Python/implementation/system and no third-party runtime dependencies.

## 5.11-STEP5 — Run discovery

Exact discover -v finds9 original methods, OK/no skips. Includes known answer/context, byte/meaning distinction, changed data/source, invalid inputs/config and repeat/no-overwrite CLI. These reruns do not add unique methods.

## 5.11-STEP6 — Failure boundary

Existing output explicit rerun fails FileExistsError and original bytes remain; invalid[] input fails before creating output. Raw failures retained. Exclusive create is not crash-atomic; incomplete write simulation/atomic publication not performed.

## 5.11-STEP7 — Preserve bundle and ownership

Retain unchanged four source/input/test files plus actual run-a/b outputs in research-bundle with this transcript and note. Compare supplied-file bytes after operations; no input overwritten. Retention is evidence for this local synthetic question only.

## 5.11-STEP8 — Limits and research review

Market data availability/revisions, identifiers/calendars/FX, selection bias, investment conclusions, code attestation, notebook fresh kernel, dependency artifacts, other platforms/interpreters and independent acceptance remain outside run. A digest and repeated deterministic output do not certify model correctness.
