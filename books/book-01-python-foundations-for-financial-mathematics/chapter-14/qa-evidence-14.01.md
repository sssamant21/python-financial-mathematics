# Chapter 14 — Runtime QA Evidence: Section 14.01

**Section:** [14.01 — Why Probability Matters in Finance](14.01-why-probability-matters-in-finance.md)  
**Source blob SHA:** `6075fa72dd7337cbab16e186fecd016810ebdf7b`  
**Date:** 2026-10-25  
**Execution environment:** Python 3.13.5 (local isolated execution environment)  
**Scope:** Initial reference-code execution only. **Not certified.**

## Execution summary

- One Python reference code block retrieved and inspected from the published Markdown.
- Reference code manually transcribed into a local `section_14_01.py` file for execution; byte-for-byte source equivalence to the GitHub fenced block has **not** been established.
- Python syntax compilation: **PASS** (`python -m py_compile`).
- Reference `unittest` suite: **12 run, 12 passed, 0 failures, 0 errors**.
- Process exit code: **0**.
- Full source extraction and byte-for-byte reproduction, editorial review, and independent model-owner approval: **PENDING**.

## Commands executed

```bash
python -m py_compile /mnt/data/ch14_qa/section_14_01.py
python /mnt/data/ch14_qa/section_14_01.py
python --version
```

## Recorded output

```text
Ran 12 tests in 0.006s

OK
Expected payoff: 5.0
Variance: 312.5
Probability of loss: 0.25
Expected loss below zero: 5.0
Simulated mean: 4.95
Python 3.13.5
```

## QA decision

**Initial runtime smoke test: PASS (transcribed reference implementation).**

**Full source-fidelity runtime gate: PENDING.** The reference code must be extracted verbatim from the published Markdown, re-executed, and its hash, stdout/stderr, and exit code retained in a durable build or CI artifact. Mathematical/editorial and application-owner review also remain pending.

**Next:** Establish byte-for-byte source-fidelity evidence for 14.01 and then execute Section 14.02.
