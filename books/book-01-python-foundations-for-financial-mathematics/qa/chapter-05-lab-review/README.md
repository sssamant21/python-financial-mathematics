# Chapter5 — first five formal lab-step reviews

Based on main `ff203f1630b1760001482a77530d1ec311862e5d`. [Steps/prerequisites/contracts](STEPS.md) · [Thirty derived records](step-register.json) · [Runner](review.py) · [Results, exact-source hashes and transcripts](results.json)

CPython3.12.14 Linux passed all **23 command records** across **five lab records**; embedded original suites reran **43 existing methods** (8+9+9+9+8), no skips. Command records comprise five direct suites, seven demo/script/module launches, five silent imports, five supplemental assertion scripts and one expected erroneous package-file launch. These counts overlap by purpose and must not be added as unique test methods/workflows. Historical totals are unchanged. Initial22-record run passed; one explicit wrong-file error probe was then added and the final23-record run passed. No unexpected failures or source edits occurred.

Reproduce from any directory with Python3.12 and standard library:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-lab-review/review.py
```

The runner extracts exact original Python fences into five isolated temporary layouts. File names, selected fence indices, code SHA256, full manuscript SHA256 and all child stdout/stderr are retained. PYTHONPATH/PYTHONHOME are removed; no package install or arbitrary path patch is used for these local-parent-directory contracts. This batch covers complete labs, not introductory fragments or optional extension implementations.

Expected outputs were derived from source fixtures and contracts: holdings B0,A12.5,C3 select A,C; three bindings validate the same12.5; wire schedule preserves E0 negative, E1 zero and E2 positive on the leap day; date/ID sorting and inclusive cutoff preserve E1/E2. Explicit literals in supplemental source-consuming probes check canonical values, empty identity, ownership, full validation and Decimal lexical scope without implementing substitute financial logic. No price, total, conversion, discounting or settlement calculation is inferred.

The wrong plain-file launch for finance_lab/__main__.py intentionally returns nonzero with the specific relative-import error. Its raw traceback is retained as expected negative evidence and is separate from final unexpected-failure count0; the correct python -m finance_lab path passes. Original suites also contain expected error assertions; their method count is not inflated by subtests or subprocesses.

All six review phases per lab record prerequisites, exact assembly, execution, result derivation, failure/ownership boundaries and import/limits. These are30 derived review units, not30 manuscript steps or new test cases. Troubleshooting explanations are reviewed against dependency direction, launch context, exact input contracts and observed process behavior; no exhaustive failure-injection or resource-limit review is implied.

Still pending: Sections5.6–5.12 formal workflows (seven records), all96 optional local extension prompts, associated project/checklist/platform work and independent acceptance. No static checker, Windows/macOS, interactive import-cache session, notebook, registry, external data or remote IAM was run here. F28 notebook/platform and F32 shared-input gaps remain open.

Next: Sections5.6–5.8 dependency/environment/repeatability lab-step review, retaining deliberate failed-install/hash evidence and approved-artifact distinctions; then5.9–5.12 and local exercises. Consult existing runtime records before reusing work, and reassess changed source hashes.
