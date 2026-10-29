# Chapter 21 — Integrated diagnostics follow-up

**Date:** 2026-10-29
**Scope:** Section 21.9 portion of COV-89.
**Status:** Selected diagnostic, serialization and failure-propagation gaps addressed; independent review pending.

The integrated report previously returned analytical sensitivities alone despite its finite-difference diagnostic contract. It now calls the Section 21.4 centered first derivative at step 1e-5 and retains method, step, estimate, signed difference from the analytical first derivative, absolute difference and units. The analytical second derivative is retained; no numerical second-derivative claim is made.

The CLI now emits sorted, indented JSON with allow_nan=False. Four additional unittest methods check the independent exponential-quotient benchmark -100*sinh(2h)/h, selected required report keys and JSON round-trip/repeatability, and propagation of injected valuation and sensitivity exceptions. These are selected schema/contract checks, not a comprehensive configurable toolkit schema.

Baseline tree: `eef74281ff4d46c09b2db57fefe44d11653b4ebe`; local snapshot replaced only the integrated module and its checker. Python 3.12.14/Linux: 19/19 Chapter 21 sources compiled; 10/10 check scripts exited zero with assertions enabled, own-directory working directory and a 15-second per-script timeout. Section 21.9 passed 18 unittest methods. Two CLI executions produced identical valid JSON.

| File | Commit | Blob |
|---|---|---|
| [section_21_09.py](../chapter-21/code/section_21_09.py) | `8f5a1cbbb7461880667bd9ca6e221af36dfcffcd` | `ca2ff456691be2946163995558ecca4518b37f95` |
| [check_section_21_09.py](../chapter-21/code/check_section_21_09.py) | `d3b25c83b5ae765076827ee28ba6b63b01a33847` | `183ba902d9b2e844c2c95a444014ca57787588c3` |
| [21.09-chapter-project-financial-mathematics-foundations-toolkit.md](../chapter-21/21.09-chapter-project-financial-mathematics-foundations-toolkit.md) | `ec8d186179c418e371095754f3b53ae5b0bf56bd` | `e8ae8ef914f6636f674b71b695ec6e615afac916` |

COV-89 remains partially open for broader interfaces, error paths and independent review. The synthetic examples remain separate teaching problems. The generated report's execution/review/approval fields remain template states; actual scoped execution evidence is this record, not an automatic approval flag.

[Chapter 21 map](coverage-chapter-21.md) · [Queue](substantive-coverage-index.md) · [Tracker](PROGRESS.md).
