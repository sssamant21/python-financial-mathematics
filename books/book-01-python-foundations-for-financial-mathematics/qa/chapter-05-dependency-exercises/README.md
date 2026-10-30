# Chapter5 — Section5.6 dependency exercises

Based on main `855ecdb9f97dafdb0253f48538342db11339baf0`. [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Raw evidence/results](results.json)

CPython3.12.14 Linux: **19 command expectations and12 predicates passed**. No unittest methods are introduced/rerun by this batch and historical unique-workflow totals are unchanged. Initial run met all expectations; no unexpected failures or manuscript changes. Expected constraint/no-requirement, unavailable-dependency resolution, no-deps metadata and missing-import failures remain raw nonzero records alongside successful approved repairs.

Reproduce with standard library and venv/ensurepip:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-dependency-exercises/review.py
```

Exact Section5.6 executable fence is compiled unchanged without invoking its main. Original fixture_wheel/pip_args/UNIT_SOURCE/REPORT_SOURCE/BEHAVIOR_CHECK are reused; new orchestration explicitly implements requested exercise variations, not an exact rerun of the full original lab workflow. Source/code/fixture-source hashes, each generated wheel's metadata/digest, explicit commands, stdout/stderr, return codes and diagnostics retained. Runtime package modifications are confined to two owned temporary venvs; source working directories do not contain importable fixture packages. No external package index/backend download or system interpreter change.

Unavailable report Requires-Dist2.0.0 fails against unit1.0.0 candidates; no fixture imports exist afterward. Approved original Requires-Dist1.0.0 with explicit constraints installs normally and passes pip check/behavior. Constraint alone requests nothing. Separate no-deps report-only install succeeds as installation but fails metadata/import; normal dependency resolution repairs both. Neither changed requirements nor approved metadata is silently relabeled. All local artifact bytes unchanged through probes, then temporary artifacts/environments cleaned.

Independent expectations concern instrument-unit representation:0 and12.50 remain exact Decimal with preserved scale and instrument_units label; no monetary arithmetic, FX or valuation. Actual executable/prefix/base_prefix and both installed origins checked against selected runtime. Installed source's original rejection checks exercise unsupported types, nonfinite and negative quantities. Inventory/stdlib/promoting an external dependency are reviewed explanations, not full source/environment/release/security certification.

50 of96 local prompts now reviewed;46 remain. All12 core workflow and20 chapter-wide answer reviews are separate evidence. No static checker, Windows/macOS, notebook/kernel, external version promotion, registry, production or independent acceptance. F28/F32 open; prior F33 failure/rerun retained. Next: Section5.7 venv identity/shadowing and environment-record exercises.
