# F35 — Problem18 requested functions omitted from companion

Severity: low instructional/prompt-contract defect; owner manuscript maintainer/QA executor. Affected baseline main `ddb839244c0831b8595dcebe709b4d88316290c4`, Section6.17 companion, Solution18/test_problem_18.

[Original companion](initial-companion.md.txt), [original runnable listing](initial-reference.py) and [initial results](initial-results.json) preserve the evidence. The initial suite passed20 methods. That did not satisfy the prompt requiring equivalent callable Python and NumPy P&L functions: AST/source review found zero top-level function definitions and only inline expressions in test_problem_18. This is a retained prose-to-code alignment failure, not an invented runtime test failure.

Correction adds python_pnl and numpy_pnl to the actual companion listing, documents the trusted finite aligned numeric-list scope, rejects unequal lengths, and makes the existing Problem18 method call/check both functions against the50/20/0 known answer. No extra unittest method was added, and no benchmark speed claim was made. The function comparison includes list conversion/to-list for NumPy; source-side input validation remains deliberately limited to the exercise scope.

Corrected explicit-discovery suite passes20 methods; read-only local-value observer reruns the same20 methods. Independent rational/Decimal and contract predicates pass45/45. Initial20 and corrected40 invocations overlap20 existing unique methods; none are added to2996 historical unique methods. [Reproduction runner](review.py) and [actual rerun results](results.json) identify source/code hashes and commands. Original snapshot remains runnable on the documented NumPy runtime. The source-fence mapping ledger preserves the old hash/evidence and identifies this new payload; historical runtime records are not rewritten.

Scope: callable answer omission corrected and listed fixtures rerun. Arbitrary-input API hardening, benchmarks, complete lab/platform and independent acceptance remain open.
