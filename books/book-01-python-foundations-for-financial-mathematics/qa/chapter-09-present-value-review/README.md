# Section 9.5 — Present value lab, answers and scalar-range follow-up

Baseline `fde888bea0f09fdf01ddbe24807b824191652522`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Five answers](ANSWERS.md).

One new workflow and five local answers reviewed. Eight command checks and eighteen additional predicates passed after F46 correction. The Section9.5 demonstration and compilation are two commands with eight existing embedded methods; six separate command records rerun original unittest and compilation for Sections9.1,9.3,9.4. The final run invokes32 existing methods, not32 new historical methods. Full raw outputs, exact source hashes and rational expectations are retained. Prepared Linux CPython3.12.14, standard library only; no earlier lab imports, external data or network. Fresh installation and other platforms were not executed.

**F46:** The finite nonzero Real value Fraction(1,2**2000) converts to float0.0. Earlier scalar helpers then treated its principal/payment as an ordinary zero and bypassed the promised nonzero-amount loss rejection. The initial runner records four failed rejection predicates: Sections9.1,9.3,9.4,9.5. The corrected helpers reject a nonzero scalar lost at conversion before subsequent arithmetic. Each existing first test method now includes the case; no test method was added. Re-run this runner at the same relative evidence path in a worktree of the baseline to reproduce initial failures. Earlier section evidence remains historical; this record supplies the corrected source hashes and rerun results.

Independent rational reciprocals verify all worked common-date amounts, practice answers, signed obligations, negative rates and staged discounting. Full-precision versus rounded reversal is checked separately. The shared scalar fix also protects rate/time conversion, but no arbitrary-range accuracy is claimed; positive subnormal values can remain approximate. Contractual settlement, partial periods, day counts, rate selection, yield curves and real investment decisions remain outside this lab. Tables require no image export. F28/F32, platform/notebook and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-09-present-value-review/review.py
```

Next: Section9.6 formal lab and local answers.
