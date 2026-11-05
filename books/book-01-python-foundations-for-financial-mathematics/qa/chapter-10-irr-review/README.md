# Section 10.13 — IRR and bisection review

Baseline `7725bff38afe50857a15512d1d574f5a8e892f2b`. [Runner](review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Twelve answers](ANSWERS.md).

Both documented commands and twelve existing methods passed on both source versions. Nine of 33 additional predicates initially failed; all 33 now pass. The runner saves the exact sole Python fence as irr_root_finding.py, executes the demonstration and tests, and compiles it in isolation. Filename and save/run/compile steps verified on prepared Linux CPython 3.12.14 using the standard library only. No network, data, installation or previous module is required.

F60: absolute currency residual stopping falsely accepted 0.5 for a scaled stream with root 0.1; multiplying tiny endpoint residuals erased the same-sign check; adding two large finite endpoints overflowed. The solver uses rate half-width or a computed zero, direct sign comparisons and a safe midpoint. F61: infinite tolerance and boolean rates, flows and iteration caps were accepted; finite nonboolean numeric settings/flows and positive integer iteration limits are now enforced. F54/F56: nonzero term underflow is rejected and exact zero flows no longer require a factor. Nine regression assertions are inside an existing method; no historical unique methods were added. The same runner against baseline reproduces the initial failures.

Exact one-period and factored quadratic roots, a 100-digit Decimal square root, and independently recomputed Decimal residuals benchmark ordinary roots, endpoints and both separate brackets of a two-root case. A tangent root and two roots hidden inside a wide bracket illustrate why a rejected bracket does not imply no IRR. Monthly-to-annual conversion is supplemental rational arithmetic; interpretation and audit prompts are conceptual. The returned rate does not certify an economically meaningful or unique root. Computed zeros, cancellation, float range and resolution remain limitations. No production solver, dated XIRR, real project data, fresh installation, notebook or additional platform was tested. F28, F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-irr-review/review.py
```

Next: Section 10.14.
