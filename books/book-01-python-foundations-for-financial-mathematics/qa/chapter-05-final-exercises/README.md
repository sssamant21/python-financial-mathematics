# Chapter 5 — final six Section 5.12 exercises

Based on main `cbff55694b2914bbff91588e74a68ae9d3af4564`. [Six answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Results/mutation snapshots](results.json) · [Next-batch checkpoint](NEXT-BATCH.md)

CPython 3.12.14/Linux: **12 command expectations and 20 predicates passed** on the first run. Eight original unittest methods run once against the unchanged wheel and once against the supplemental copy:16 invocations of8 existing methods, not16 unique tests. Deliberate import-time application-read mutation fails as expected and restored original reruns successfully; actual failure traceback is retained. No unexpected failure or manuscript change. No new historical method/workflow total is claimed.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-final-exercises/review.py
```

The previously retained original wheel is hash-checked against its earlier result record; its four package listings match current manuscript bytes exactly. Install that wheel offline in one fresh runtime, verify purelib origin outside checkout and run original source tests. Quiet import is checked under a fresh isolated interpreter with [application file access guards and audit observer](import_probe.py), then challenged with a deliberate read mutation and restoration. Import-loader source/bytecode reads are allowed and logged; arbitrary native/kernel I/O is outside this observer's claim.

For E1/E6 only, modify the disposable installed copy with [reports.inflow_count](reports.py), explicit facade export and [TypedDict result documentation](result_types.py)/return annotation. The original core calculation/validation body stays the same; run original eight methods plus [13 API/type predicates](extension_probe.py), guarded import and module CLI schema. This copy has no rebuilt wheel/release and baseline metadata is not new-version evidence. The original wheel bytes are untouched and runtime is removed. No sys.path/PYTHONPATH edits, editable installation or source-checkout import was used.

E5 source-distribution rebuild, E7 version policy and E8 public-release criteria are design reviews only. No static checker, sdist rebuild, new wheel, registry request/upload, platform matrix, production or independent acceptance. E2/E3 remain linked to earlier project evidence. F28/F32 remain open; F33/F34 histories retained.

All96 Chapter5 local exercise prompts now have scoped records, alongside the separate20 chapter-wide answers and12 core workflow records. This completes the listed Chapter5 review scope, not comprehensive validation or certification. Next: Chapter6 formal lab/answer review, starting with the20 Section6.17 chapter-wide problems and companion alignment.
