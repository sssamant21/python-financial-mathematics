# Chapter5 — Section5.9 layout/output/discovery exercises

Based on main `fc05f57df6529b73f40086b282ebd6174a551044`. [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Results/source and supplemental snapshots](results.json)

CPython3.12.14 Linux: **11 command expectations and13 predicates passed**. Baseline source suite runs8 methods; extended explicit discovery runs those same8 plus2 new QA nested-test methods. Thus16 invocations of8 existing methods and2 supplemental methods are recorded separately; historical unique-method/workflow totals unchanged. Initial runtime run passed; counts subsequently derived from actual verbose case names and rerun unchanged. No unexpected failures or manuscript corrections. Expected type/schema/FileExistsError/JSON/import failures retained with actual error classes/tracebacks and checked for no success stdout.

Reproduce using standard library:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-layout-exercises/review.py
```

Original package/core/entry/test/fixture listings reconstructed unchanged for baseline and hashed. New no-active fixture, output-option entry copy, regular test-package markers and nested regression class are supplemental, retained as source strings in results. Core validation and original tests/fixture remain byte-identical. No manuscript file or installed package modified.

Expected empty-active stdout is exactly `Active IDs: \n` (space before LF). New --output path writes known Active IDs SEC-A/SEC-C line through exclusive UTF8/LF create, suppresses success stdout and cannot overwrite earlier report or input. Invalid input rejected before output exists. Paths are caller-relative unless absolute, parent must exist. Exclusive creation is not crash-atomic; file existence alone is not success evidence. No append/force-overwrite mode implemented.

Nested tests use regular packages and explicit `-s tests -t .` for tested3.12 runtime, with real count10 and qualified nested names checked. No implicit cross-version namespace-discovery assumption. Separate outside-cwd-I failure confirms absolute data path does not make local package installed/discoverable. No sys.path edits or installed-financial_layout claim.

All eight prompts have scoped answers. Flat→src installation, report retention and domain-subpackage compatibility refactor are proposals, not executed packaging/release/refactor decisions. Original source checks and supplementary predicates establish specific selection/schema/ownership behavior, not quantity valuation. No static checker, Windows/macOS, notebook/kernel, registry, remote data, production or independent acceptance. F28/F32 open; F33 history retained.

74 of96 local prompts now reviewed;22 remain. All12 core workflows and20 chapter-wide answers remain separate. Next: Section5.10 configuration exercises, then5.11 and remaining six5.12 prompts (E2/E3 already reviewed).
