# Book 1 QA — Chapter 15 Reference Runtime

**Status:** Scoped reference runs passed after corrections; independent statistical, mathematical, data, editorial and other-platform review remains pending.  
**Manuscript snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 15 files were unchanged between that snapshot and repository head `644160125a4cbfa228e615322cd27a2f1ae29b75`. The post-fix run includes the Section 15.3 and 15.4 changes published with this record.  
**Environment:** CPython 3.12.14, Linux 6.18.55 x86_64 with glibc 2.39. Run date: 2026-10-27 UTC.

## Results

All 15 section reference suites passed after correction: **180 unittest methods**, 12 per section, with no failures or skips reported. Each suite was extracted from its manuscript and run in a separate process on synthetic examples. [Per-section results](results.json) and [post-fix output](reference-output.log) are retained.

## Findings and corrections

- **Section 15.3 — constant-series variance:** The original test required exact equality with zero for `[0.05, 0.05, 0.05]`, while the computed floating-point variance was approximately `7.222237291452134e-35`. Exact mathematical variance is zero; the test now uses an illustrative absolute tolerance of `1e-30` in squared observation units. The prose explains the distinction. [Original failure](section-03-before.log).
- **Section 15.4 — adjusted excess kurtosis:** The original test expected `-1.2` for `[-2, -1, 1, 2]`. For the stated estimator, `m2=2.5`, `m4=8.5`, unadjusted excess `g2=8.5/2.5²−3=−1.64`, and adjustment `(3/2)(5g2+6)=−3.3`. The expected value was corrected. [Original failure](section-04-before.log).
- **Section 15.4 — constant-data handling:** An additional check of the original function with `[0.05, 0.05, 0.05]` returned mean `0.05000000000000001`, `m2=4.81482486096809e-35` and spurious standardized moments instead of rejecting constant data. The function now detects identical float observations before centering, and the existing invalid-input test includes this regression case. Nonconstant near-degenerate inputs and numerical extremes still need review.

All 15 suites were rerun after these changes. The corrections address the observed cases; the small variance tolerance is not a universal acceptance threshold and the estimator is not certified.

## Reproduction

Retrieve the pinned Book 1 Markdown files under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the working directory and replace Sections 15.3 and 15.4 with the corrected files in the commit containing this record. Inspect [reference-run.py](reference-run.py) and execute it in an isolated environment:

```bash
python reference-run.py
```

The script extracts each section's fenced Python block containing `unittest` and `__main__`, writes separate scripts and logs under `/tmp/book1_ch15_01_15`, and uses the invoking Python interpreter with a 30-second timeout per section. The reference blocks use standard-library imports and synthetic inputs. Section 15.14 defines a CSV loader, but its reference tests do not exercise file ingestion; no claim is made that the CSV lab was run.

## Remaining work

Independently review estimators, statistical assumptions, confidence intervals, regression, tail measures, nonconstant near-degenerate inputs, overflow/underflow, source data and missingness. Execute labs and verify worked exercises separately; review references, attribution and editorial consistency, supported platforms and artifacts. This is scoped runtime evidence, not a canonical or production certification.
