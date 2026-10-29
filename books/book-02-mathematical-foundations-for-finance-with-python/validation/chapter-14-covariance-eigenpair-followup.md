# Chapter 14 — Covariance eigenpair follow-up

**Date:** 2026-10-29
**Scope:** Section 14.9 eigenpair portion of COV-69.
**Status:** Fixed-example eigenpair report and checks complete; independent review pending.

## Contract gap and correction

The capstone learning outcomes promised eigenvalue verification, and its manuscript derived the covariance eigenvalues. The implementation checked positive definiteness through principal minors and Cholesky but did not compute or return the covariance eigenpairs.

The project now calls the existing Section 14.2 spectral decomposition for its fixed covariance. The report includes the covariance matrix, ordered eigenvalues, paired eigenvectors, eigenpair residual norms, reconstruction error and orthogonality error. The manuscript acceptance table and output contract describe these fields and eigenvector sign freedom. This reuses an existing teaching decomposition; it does not introduce a general-purpose eigensolver or configurable covariance API.

## Independently expected results

The characteristic polynomial is \(\lambda^2-0.13\lambda+0.0035\), so

\[
\lambda_\pm=\frac{13\pm\sqrt{29}}{200}.
\]

The checker asserts these values, strict positivity and descending order, their trace and product. For each returned vector, it independently computes the norm and \(Cv-\lambda v\), checks orthogonality, and reconstructs C from the returned eigenpairs.

It also compares each vector's outer product with the corresponding exact spectral-projector expression,

\[
v_kv_k^\mathsf T=\frac{C-\lambda_{\mathrm{other}}I}
{\lambda_k-\lambda_{\mathrm{other}}}.
\]

This checks direction and eigenvalue pairing while allowing either vector sign. Reported near-zero diagnostic fields are asserted in addition to these direct calculations, rather than being accepted as evidence by themselves. The checker retains its explicit 1e-10 relative and absolute tolerances.

Four temporary report corruptions were detected: swapped vector pairing, incorrect eigenvalues with the same trace, nonunit vectors, and standard-basis vectors accompanied by unchanged near-zero diagnostics. No corrupted report was published.

## Runtime and publication

Baseline tree: `c2e8205575f2e35e0bf9ee81fed40cea9a113bfe`. All 21 Chapter 14 Python files were fetched at that revision; the local snapshot replaced only the capstone and its checker.

Python 3.12.14/Linux: 21/21 files compiled with py_compile; 11/11 check scripts exited zero. Scripts ran from their code directory with assertions enabled and a 15-second timeout per script. This scoped follow-up does not replace the historical full-book run.

| File | Commit | Blob |
|---|---|---|
| [section_14_09.py](../chapter-14/code/section_14_09.py) | `1142a550481707149ca080279589f521a5af4a10` | `577a4d6417e8232a18e53750dc373363871674c5` |
| [check_section_14_09.py](../chapter-14/code/check_section_14_09.py) | `b177d0e5e3d44a83996334a9f70503f4efdb548e` | `ac57ddd6d198529b120a0d20612762cbacfe95bb` |
| [14.09-chapter-project-quadratic-exposure-and-decomposition-lab.md](../chapter-14/14.09-chapter-project-quadratic-exposure-and-decomposition-lab.md) | `71a43792ea072f764dc08c52f98ff0b23bec0d64` | `00cd0f6fdc974347825ded644f5f368241f632f2` |

## Remaining scope

The fixed-example eigenpair omission is addressed. COV-69 remains partially open for compression-bound/report-metadata evidence and independent review. Near-degenerate spectral behavior, arbitrary covariance inputs, estimator assumptions and broader decomposition ranges remain outside this follow-up. No independent mathematical/editorial sign-off or canonical approval is granted.

[Chapter 14 map](coverage-chapter-14.md) · [Queue](substantive-coverage-index.md) · [Tracker](PROGRESS.md).
