# Chapter5 — Section5.7 venv identity/shadowing exercises

Based on main `63b4d515c48c10dae70de9278579a2d7badcbeb6`. [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Results/raw errors](results.json) · [Editor/notebook checklist — NOT RUN](EDITOR-NOTEBOOK-CHECKLIST.md)

CPython3.12.14 Linux: **13 command expectations and23 predicates passed**. No original unittest methods are present in these workflows and historical unique-method/workflow totals are unchanged. Initial run satisfied all expectations; no unexpected failures or source corrections. Deliberate source-shadow origin assertion failure retained with raw traceback, separately observed shadow location and subsequent correct isolated-origin/behavior checks.

Reproduce with standard library and venv/ensurepip:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-venv-exercises/review.py
```

Compile exact Section5.7 fence unchanged without main, reusing original interpreter/copy_marker helpers, INFO_CODE, MARKER_SOURCE and BEHAVIOR_CODE. New exercise orchestration creates two no-pip venvs plus a separate normally provisioned pip venv, records every result and source/code SHA256. This is not an exact repeat of the whole original recreation workflow, already recorded separately. Marker source is explicitly copied fixture code, not a pip-installed distribution; only third environment demonstrates standard pip provisioning. All artifacts/environments belong to temporary task directories and are cleaned.

Both runtime field sets retained, executable/prefix/base/purelib/config/isolated values checked; A/B purelib differ. Working-directory SHADOW marker uses same source recipe with a different label. Ordinary lookup fails original expected-prefix assertion; -I recovers intended marker without changing environment installation or inventing path fixes. Normal source lookup controls are explicit and do not establish a universal editor configuration. VIRTUAL_ENV-only experiment invokes unchanged executable and compares all runtime fields. Benign outside-venv file read is restricted to our owned synthetic note and illustrates absence of filesystem jail, not network/IAM/security certification.

Independent representation expectations are marker labelsA/B/SHADOW and exact zero/fractional Decimal units; original rejection code runs. No amount arithmetic, prices, valuation or other financial analysis inferred. Notebook/editor/recreation categories and security limits are reviewed explanations; checklist execution is entirely NOT_RUN. No kernel/UI, shell activation, static checker, Windows/macOS, external packages/data, production or independent acceptance performed. F28/F32 open; prior F33 history retained.

58 of96 local prompts now reviewed;38 remain. All12 core workflow and20 chapter-wide answer reviews stay separate. Next: Section5.8 hash/dependency-closure exercises, then queue order; skip completed5.12-E2/E3 unless sources change.
