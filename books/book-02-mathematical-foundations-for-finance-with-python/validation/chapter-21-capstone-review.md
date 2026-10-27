# Book 02 — Chapter 21 Capstone Coverage Review

**Date:** 2026-10-27  
**Scope:** Focused review of the synthetic integrated scenario and selected boundaries in Sections 21.3–21.10; not a complete chapter or independent mathematical review.

The local run used the earlier Book 02 snapshot, with six Chapter 21 files modified as described below. Other Chapter 21 Python files were compared with the tree at `644160125a4cbfa228e615322cd27a2f1ae29b75` and matched. The six fixes were published through `53b99a7b2e6b2b03ae61d74ae3119aed76e955e6`. This is not a test of the entire current repository.

## Findings and changes

| Finding | Evidence | Change and result |
|---|---|---|
| Continuous account contribution lost at an extreme small rate | `transition(0, 5e-324, 100, .5)` returned 0 although the continuous limit is approximately 50. The product rate × time rounded to zero. | Use the zero-exponent limit for that case and an expm1/exponent form otherwise; added a regression case expecting 50. |
| Central-difference denominator overflow | With a finite step of `1e308`, `2*step` becomes infinity and can silently return zero. | Reject a non-finite denominator with OverflowError and add a regression case. This does not establish a general error bound or solve all finite-difference precision issues. |
| Integrated report omitted some scenario inputs | Replication and allocation results lacked their matrix, target and allocation inputs despite the report requirement. | Include these synthetic inputs and add checks for their presence. The report still has educational scope and pending approval. |

## Validation performed

On Python 3.12.14/Linux, the eight scripts `check_section_21_03.py` through `check_section_21_10.py` each exited zero after the changes, reporting 104 unittest cases in total. These counts include only the named scripts and are not proof of complete exercise, branch, numerical or business coverage. No full book-wide rerun or cross-platform run was performed for this change.

The scenario benchmarks for cash flow, derivatives, replication, allocation and account are exercised by the project checks. This focused review does not establish that every manuscript example, domain boundary or financial assumption is validated.

## Remaining work

- Independently review the numerical changes, including near-zero, large-magnitude and cancellation behavior; assess other intermediate overflow/underflow cases.
- Review central-difference actual perturbations and step selection, replication conditioning, and optimization objective scaling.
- Check all Chapter 21 exercises and documented lab steps against independently derived references, including the report's units and assumptions.
- Continue coverage review across the remaining chapters; rerun the full suite against the final exact revision and supported environments.
