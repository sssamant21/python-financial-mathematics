# Book 02 — Final LP assessment integration follow-up

**Date:** 2026-10-30  
**Baseline:** `f64d29daa401efc1ae2e83732efc9ccd52d4da64`  
**Pinned executable source:** `60cd09c1072aec6d6f437b62961d0b4e50cad50c`  
**Disposition:** Selected COV-78 integration evidence; independent review pending.

Section17.10's LP report previously started from literal vertices and a dual pair. The fixed numerical answers were correct, but did not exercise the Section17.5 computation or retain its certificate. The [initial new checker failure](chapter-17-final-lp-integration-followup.json) records the missing certificate. This is an assessment-integration gap, not a demonstrated original arithmetic defect.

The final report now calls Section17.5's actual `solve_vertices()`, scores computed vertices with its benefit helper, and calls `certificate(...)` on the returned allocation. The manuscript's display order and existing fields are retained. The fixed positive-coordinate optimum implies both dual inequalities bind: u1+2u2=5 and u1+u2=4, hence (3,1). This is a specific analytic dual derivation, not a general dual solver. Raw primal/dual slacks, gap, complementary products and residual-based acceptance are retained.

The [runnable checker](../chapter-17/code/check_final_lp_integration.py) derives all six boundary intersections with Fraction arithmetic independently of lab constants/functions, filters four feasible vertices, and verifies corresponding scores and the optimum(2,6), value34. Six primal/dual candidates have exact slack/value/gap/complementarity expectations: one valid pair and five rejected alternatives, including a zero-gap but dual-infeasible pair. It observes two actual helper calls and detects five injected wrong outputs: allocation, benefit, vertex set, certificate acceptance and gap. Strict JSON round-trip passes.

All24 Chapter17 sources compiled and14 check/test scripts passed on Python3.12.14/Linux with assertions enabled and timeout15 seconds. The scoped manifest matches the pinned tree and all24 hashes remained unchanged after execution. [Machine evidence](chapter-17-final-lp-integration-followup.json) retains the baseline failure, exact manifest, commands/environment and actual outputs. Corrected source blob `05b5a37ffb1d461e6be7435f71eb74d5074170e4`; checker blob `bb93ec59bef18d1c7efb2e0606260b99d1df2f9a`.

[V-47 full runtime](runtime-refresh-2026-10-30-r11.md) compiled482 files, passed271 scripts and verified483 required input hashes before/after at the same executable pin. It also covers the preceding Section17.9 report source/checker. Later manuscript/report/tracker writes are outside executable inputs.

The manuscript explains the actual dependency and fixed scope; its escaped command markup is repaired. COV-78 remains partially open for broader applied tasks and mathematical proofs. Twenty-eight selected COV categories remain partially addressed; none closed by the register. No independent reviewer sign-off, supported-platform validation, release acceptance or canonical approval is implied.

Next substantive item: COV-79 Section18.9 safeguarded Newton project trace checks: independently recompute every selected endpoint sign and proposal-interior safeguard, returned-root residual and exact function/derivative call accounting. Section18.8's earlier bracket audit is already complete within its recorded scope.
