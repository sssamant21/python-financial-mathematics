# Chapter 8 — Normalized sensitivity range follow-up

**Date:** 2026-10-29 (America/New_York)
**Scope:** Section 8.8 range portion of COV-51.
**Status:** Zero-normalizer and selected nonfinite report cases addressed; scoped runtime passed; independent review pending.

Standalone discounted_price now validates its exponent and resulting price. Ordinary exponential underflow remains permitted, but rate_sensitivity requires a positive representable base price before normalization. Previously an underflowed base price could reach division by zero. Duration, convexity and analytic convexity are validated before returning a report.

Nonfinite exponents/results and a zero base price raise ValueError through the local contract; exponential overflow retains OverflowError. No general subnormal-accuracy or underflow-recovery guarantee is added.

Independent exact-arithmetic stencil ratios for a single continuously discounted payment are duration=sinh(T*h)/h and convexity=4*(sinh(T*h/2)/h)^2. These are compared at cash flows 1,1000,1e200 with T=5,h=0.001, separately from analytic limits 5 and 25. Zero maturity produces zero sensitivities. Tests cover zero-price normalization, price-product/exponent overflow and exponential overflow.

Baseline tree: `f799283ff078aeb40070705ab72275bcb20dfce8`. All 21 Chapter 8 Python sources were fetched at that revision; the local snapshot replaced only Section 8.8 and its checker. Python 3.12.14/Linux: 21/21 files compiled and 11/11 check scripts exited zero with assertions enabled, own-directory working directories and a 15-second per-script timeout.

| File | Commit | Blob |
|---|---|---|
| [section_8_08.py](../chapter-08/code/section_8_08.py) | `6c4931354d028a98df1e6ba1b537924b77cc780e` | `6a638e864fc32313e526da2a3f9e2e818ed1ba6a` |
| [check_section_8_08.py](../chapter-08/code/check_section_8_08.py) | `1cd1ce61e8053703ed68cc44946e1348d810cd5b` | `5df7583b3d18878c76214c529f98413fb3c1ff1b` |
| [8.08-numerical-derivatives-and-step-selection.md](../chapter-08/8.08-numerical-derivatives-and-step-selection.md) | `6ff24b89af901fcd666a7f8e6c00137d862ed041` | `d7481d509f72eb8e10894cb0e725328694c867c9` |

COV-51 remains partially open for earlier helper copies, implicit domains/branches, cancellation/subnormal accuracy and independent review. This extends the existing category; the register still tracks eighteen selected partially addressed categories. This scoped change follows the full-book runtime record.

[Helper guards](chapter-08-helper-guards-followup.md) · [Chapter 8 map](coverage-chapter-08.md) · [Gap register](gap-remediation-register.md) · [Tracker](PROGRESS.md).
