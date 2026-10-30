# Book 02 — Section 17.4 degenerate multiplier follow-up

**Date:** 2026-10-30  
**Baseline:** `1273dc47b6df75c107047da28b81f2630a8a4546`  
**Pinned executable source:** `df656dbbe59bda073bf662392c9f0348fc18cc83`  
**Disposition:** Selected COV-76 evidence added; helper unchanged; independent review pending.

At cap zero, primal feasibility fixes weights (0,1). Differentiating the exact decimal variance polynomial gives gradient (1/50,9/50). Inactive second lower bound forces its multiplier to zero; stationarity gives lambda=-9/50 and cap multiplier minus first lower multiplier=4/25. Therefore (a,0,a+4/25), a>=0, is a nonunique dual family for one unique primal portfolio. The lab's existing a=0 choice is valid. Opposite active normals sum to zero.

The [runnable checker](../chapter-17/code/check_degenerate_multipliers.py) uses Fraction equations without importing the lab gradient. Six parameters (0,1/1024,1/16,1/4,1,8) satisfy exact equations and pass actual floating diagnostics at tolerance1e-12. It verifies canonical multipliers, unchanged objective9/100, activity [0,2], primal residuals and complementary products.

Three independently constructed candidates isolate dual-sign, stationarity and complementarity failures. Each is rejected while the other residual families pass. Omitting its single failing family would accept it; all three incomplete acceptance rules are detected. A negative a=-2^-45 passes tolerance1e-12 but fails tolerance0, explicitly distinguishing numerical acceptance from mathematical feasibility. One valid exact-model family fails zero-tolerance float diagnostics after rounding. No change to the fixed tolerance policy is inferred from this characterization.

The first new checker run passed against the unchanged baseline helper; there was no numerical regression failure or source fix to conceal. [Raw evidence](chapter-17-degenerate-multiplier-followup.json) retains that initial run, exact source manifest and subsequent actual outputs. Helper blob `3f581603f381837951e52c959bf74249ded948a9`; checker blob `52fdfc95cba246fb45acdeef2e24e27c9a1253d8`. The manuscript now derives the family and distinguishes strict complementarity by multiplier choice. Its eight escaped backticks in the lab instructions were corrected so the inline path and command fence render as Markdown.

All22 Chapter17 Python files compiled and12 check/test scripts passed as part of [V-46](runtime-refresh-2026-10-30-r10.md). Full execution compiled480 files, passed269 scripts and verified481 required input hashes before/after. The exact runtime manifest was compared with the pinned Git tree. Manuscript/report/tracker writes after this pin are outside executable inputs.

Scope is the fixed decimal covariance and six moderate finite dual parameters, not arbitrary magnitudes, general covariance, complete tolerance scaling, a general solver or human independent review. COV-76 remains partially open. Twenty-eight selected categories remain partially addressed; none closed by the register. Supported environments, independent mathematical/editorial review, final reviewed release and canonical approval remain pending.

Next substantive item: COV-77 Section17.9 retained report inputs/model/tolerance metadata and deterministic strict-JSON contract. Reconcile absent provenance without claiming real-market data validation.
