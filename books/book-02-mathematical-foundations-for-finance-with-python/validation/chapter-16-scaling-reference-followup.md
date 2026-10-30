# Chapter 16 — Independent scaling and stable-step references

**Date:** 2026-10-30  
**Inspected revision:** `f3c5eefcb83bc5664d59e0c76e3ac9dbede327ba`  
**Disposition:** Selected COV-75 scaling evidence added; implementation unchanged.

[New checker](../chapter-16/code/check_scaling_references.py) independently derives H_raw=diag(10^6,1) and inverse coordinate derivative J=diag(1/1000,1). Exact Fraction multiplication gives J^T*H_raw*J=I. The report's raw/scaled condition-number fields must match the independently derived ratios 10^6 and 1.

Four raw/scaled points check objective equality and coordinate round trips. Twelve central second-difference cases (two coordinates, three dyadic steps, raw/scaled objectives) measure the actual implementations' curvatures rather than only comparing report literals. Raw relative curvature tolerance is 2e-12; scaled curvatures are exactly one in the selected cases.

The real Section 16.5 scalar solver tests each diagonal mode a=1 and a=10^6. Step 1/a reaches the optimum in one accepted update. Step 2/a oscillates through (1,-1,1,-1) until its budget. Step 3/a grows to x=4 in two updates. These six mode runs support the selected stability illustration, not a claim that Section 16.7 implements a multivariate optimizer.

All 23 Chapter 16 files compiled and all 13 scripts passed on Python 3.12.14/Linux, assertions enabled and 15-second timeouts. The subsequent [V-39 full refresh](runtime-refresh-2026-10-30-r3.md) includes these checks and the preceding optimizer-status/multistart additions, with exact hashes and raw outputs.

The condition numbers and step bounds apply in the stated coordinate system and objective normalization; parameters/steps with different units are not interchangeable. General scaling, arbitrary conditioning, quasi-Newton theory, derivative extremes and independent review remain open under COV-75. Twenty-eight categories remain partially addressed.

Next executable item: COV-75 finite-difference representability/denominator guards in Sections 16.2–16.4, starting with minimal exact-polynomial references before any implementation change.
