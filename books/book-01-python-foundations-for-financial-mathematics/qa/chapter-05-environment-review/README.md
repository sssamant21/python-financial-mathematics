# Chapter5 — dependency/environment/repeatability lab-step review

Based on main `aae5aa1674a5184f5a6279a4b9b48fbb4dd7eabe`. Three formal lab records and24 derived step-review units now have scoped evidence. [Steps](STEPS.md) · [Register](step-register.json) · [Final results](results.json) · [Failure and rerun](FAILURE-AND-RERUN.md)

CPython3.12.14 Linux: **27 final predicates passed**, covering unchanged Section5.6/5.7/5.8 workflows, fresh quiet imports and a separate Linux explicit-interpreter venv/pip setup. These predicates and child subprocess records are not new original unit-test methods or additions to historical unique workflow totals. All96 optional local extension prompts remain separately queued.

Reproduce from repository root with standard library and venv/ensurepip:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-environment-review/review.py
```

The runner extracts original source listings unchanged under prescribed names, including Section5.8's exact helper dependency. The supplemental observer executes each listing and records subprocess arguments/returncodes/stdout/stderr without altering command behavior. It restores direct-script path/argv semantics. [5.6 raw children](5-6-children.json) · [5.7 raw children](5-7-children.json) · [5.8 raw children](5-8-children.json). Original stage output and selected evidence JSON, source/code hashes, runtime/platform and manual setup fields are in results.json. Environment-variable values are not dumped.

The initial observer import-path defect and secondary evidence-decoding error are retained, corrected in QA tooling only and rerun; no manuscript change. Expected missing-dependency and changed-wheel hash failures are separately retained together with successful approved repair/retry. Only original synthetic fixtures are installed in temporary environments; no external index or build backend is used here. Section5.7's copied marker is explicitly not a pip-installed distribution. Original no-pip lab and additional ensurepip setup are separate evidence.

Independent expectations follow declared representation semantics: exact Decimal zero/fractional units retain value and text12.50, label instrument_units, finite/nonnegative policy; no financial arithmetic or valuation. Report1.0.0 requires unit1.0.0; removal must fail metadata check, restore must pass. MarkerA/B identities require distinct prefixes/origins; recreatingA removes its marker while preserving recipe/B. Same approved wheel bytes must match approved hashes and known behavior; changing ZIP comment must change bytes/hash without claiming changed financial code. The two installs are independently checked against explicit known output, not compared only with each other.

Scope: prerequisites, paths, dependency contract, stage sequence, expected failures, repairs, ownership/cleanup and output interpretation. Source resource creation/deletion is restricted to script-owned temporary directories. No shell activation, static checker, Windows/macOS, editor/kernel, public release, compiled dependency matrix, real market inputs, IAM/security or independent financial acceptance was executed. Existing F28 and F32 remain open.

Next: Sections5.9–5.11 formal layout/configuration/research lab-step reviews, then Section5.12 project/checklists/extensions and96 local prompts. Four formal workflow records remain pending; all20 chapter-wide answers and first eight lab/workflows have scoped records, not comprehensive acceptance.
