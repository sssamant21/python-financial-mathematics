# Book 02 — Section 17.9 audit-report contract follow-up

**Date:** 2026-10-30  
**Baseline:** `8b64d636d8524927c8adaa977d6f6b8304a6fe87`  
**Pinned executable source:** `e5bf5f753a12e8b83f98933682c97f0a55ea9805`  
**Disposition:** Selected COV-77 reporting gap addressed; independent review pending.

The manuscript asks for reproducible assumptions and deterministic decision output, but the prior financial report omitted target/current inputs, capital and configured costs; certificates omitted tolerance and proposed candidate inputs. The [initial failing check](chapter-17-report-contract-followup.json) records KeyError on missing inputs. This is a reporting-contract gap, not a demonstrated incorrect numerical allocation.

Changes are additive report fields; optimizer, feasibility, residual, financial arithmetic and acceptance rules are unchanged. Certificates retain weights/lambda/multipliers/caps, tolerance, its single-absolute-threshold policy and residual units. The financial report retains inputs, weight-sum tolerance, expected returns, annual period and inherited monetary units. The assessment identifies schema version1, ordered assets and synthetic fixed annual coefficients. No market-data dates, upstream verification or general covariance ingestion are invented.

The [runnable checker](../chapter-17/code/check_report_contract.py) exercises four financial input sets including no-trade, zero-cost and dyadic small-notional cases. Twenty-four metric fields are checked against independent Fraction calculations from explicit coefficients and weight changes. Six candidate/tolerance cases check retained inputs and actual pass-rule consistency at tolerances0,1e-12,0.125. Sorted strict JSON round-trips identically; two fresh interpreter executions return byte-identical stdout and matching parsed content. These observations are limited to the recorded environment and cases.

All23 Chapter17 Python files compiled and13 check/test scripts exited zero on Python3.12.14/Linux, assertions enabled, separate processes, timeout15 seconds, cwd the chapter-code directory. All23 source blob hashes match the pinned tree and remained unchanged after execution. [Machine record](chapter-17-report-contract-followup.json) retains baseline failure, exact manifest, environment, commands and stdout/stderr/exits. Corrected source blob `124621ffc6b58de7d984d4d5f7c097e3014fb99a`.

The manuscript now reconciles fixed synthetic data and numeric controls with upstream lab responsibilities, explains mixed residual units, and distinguishes selected numerical determinism from platform support. Its escaped lab-command backticks were also repaired. Existing financial-range and tiny-empty-interval checks pass unchanged.

This scoped source/checker change follows [V-46](runtime-refresh-2026-10-30-r10.md), whose full execution remains480 compiled/269 scripts/481 required hashes at its earlier pin. Current pinned inventory is481 Python files/270 check-test scripts; these inventory counts are not a new full runtime pass. Refresh full execution as related executable changes accumulate.

COV-77 remains partially open for broader financial assumptions, parser/data/model governance and independent review. Twenty-eight selected COV categories remain partially addressed; none closed by the register. Tolerance scaling, supported-platform validation, final reviewed release and canonical approval remain open.

Next substantive item: COV-78 Section17.10 LP assessment integration. Its current report starts from literal vertices/dual pair rather than the Section17.5 computation; integrate actual helper output and test independently derived vertex/objective/certificate expectations plus false certificates, without claiming a general LP solver.
