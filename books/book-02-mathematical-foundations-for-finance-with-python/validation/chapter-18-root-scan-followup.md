# Book 02 — Section 18.5 root-scan correction and contract follow-up

**Date:** 2026-10-30  
**Baseline:** `ae253c33989977fb1849aca60e456ac04c4d7371`  
**Pinned executable source:** `f02d9dc8de4198e2804737313a0ef9e05dcff50d`  
**Disposition:** Selected COV-80 correction/evidence; independent review pending.

For flows(-1,2+d,-(1+d)), d=2^-30, multiplying NPV by (1+r)^2 gives -r(r-d). Thus exact represented-input roots are0 andd. Five of six original non-root/root probes falsely returned zero for nonzero NPVs; e.g. at r=-d, exact NPV=-2/1152921502459363329 rounds to -1.7347234792079814e-18, while the original returned0. The original seven-point scan reported every point as an exact grid root and retained three non-root rates after merging. [Machine evidence](chapter-18-root-scan-followup.json) preserves these original outputs and the failed first checker.

The finite-period NPV now uses exact rational Horner evaluation for represented cash flows/rate and rounds the complete result once. Nonzero-to-zero underflow and final overflow raise ValueError; true cancellation to zero is allowed. This avoids separately rounded powers inventing roots, at a computation cost that grows with the polynomial/input precision. It is an educational exact-input contract, not a throughput or cash-flow measurement guarantee.

A separate original probe scanning[0,1e308] with two steps failed because width*index overflowed before division, although all requested points were finite. Each grid point now uses the complete exact endpoint interpolation before rounding; duplicate represented points are rejected. Reports retain actual grid and NPV values. The original overflow failure and an intermediate checker failure on missing new grid metadata are retained separately from the NPV regression.

Root merging is now a declared optional `dedup_tol`, default1e-9 absolute periodic-rate units. All sorted candidate roots and merged_count remain visible. A candidate is retained only when its exact represented-float distance to the last retained candidate is strictly greater than the threshold. The default intentionally merges the two close roots; tolerance0 preserves both when resolved. This greedy policy is not transitive clustering or proof of mathematical identity.

The [runnable checker](../chapter-18/code/check_root_scan_contract.py) verifies13 independent direct rational NPV references, actual close-root grid discovery/refinement, four repeated-root hit/miss grids, five isolated merge-boundary sets, five invalid tolerances, four grid references, collapsed-grid rejection, two NPV range rejections and JSON round-trip. Controlled scanner output isolates merging from financial conditioning; real close/repeated-root checks use the actual scanner/refiner.

All23 Chapter18 Python sources compiled and13 check/test scripts passed. All23 hashes match the pinned tree and remained unchanged after execution. Corrected source blob `6b7c564775aede25201ac384c5ed19491ebba585`; checker blob `2d1f687818c5b9e995e3921db34264ddfada31ac`. Raw evidence retains environment, commands, stdout/stderr/exits, baseline failures and scoped reruns.

[V-48 full execution](runtime-refresh-2026-10-30-r12.md) compiled484 files, passed273 scripts and verified485 required hashes before/after at the same pin, including the preceding project-trace checker. Later manuscript/report/tracker writes are outside executable inputs. The manuscript describes exact input arithmetic, declared merging limits and repaired command markup.

Scanning remains nonexhaustive, including nearby roots in one cell and non-grid repeated roots. Broader interpolation/step/order/range, continuity and completeness proofs remain open. COV-80 is newly partially addressed, bringing selected partial categories to29; none closed by the register. These categories are not defect counts or a completion percentage. Independent mathematical/editorial review, supported platforms, release acceptance and canonical approval remain pending.

Next substantive item: COV-80 Section18.6 selected interpolation curvature-bound and half-width/factor-four references; preserve the distinction between interpolation and extrapolation.
