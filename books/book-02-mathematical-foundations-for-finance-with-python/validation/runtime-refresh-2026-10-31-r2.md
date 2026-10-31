# Book 02 — Full-book runtime refresh V-53

**Date:** 2026-10-31  
**Pinned source revision:** `4d90b8d6a3fdd397c7d071582829d5384fa410ab`  
**Environment:** Python 3.12.14 / Linux x86_64, assertions enabled, no optimization.

The twenty-second refresh compiled **495/495 Python files** and ran **284/284 check_/test_ scripts successfully**, with zero failed exits or timeouts. **496/496 required source/fixture Git blob hashes matched before and after execution**. Counts derive from the pinned recursive tree, including the Section 1.14 JSON fixture. Summed script wall time: 9.334028 seconds.

Compared with V-52, this snapshot adds affine and polynomial interpolation checkers and updates Sections 18.6/18.10. [Affine evidence](chapter-18-linear-range-followup.md) and [polynomial evidence](chapter-18-polynomial-range-followup.md) retain initial defects and reruns. [Raw full run](runtime-refresh-2026-10-31-r2.json) contains the manifest, environment, per-script commands, working directories, outputs and timing.

Reproduce by checking out the pinned revision, verifying the raw manifest's Git blob hashes, compiling each listed .py with py_compile.compile(doraise=True), and running each basename beginning check_ or test_ in a fresh Python process from its parent directory with assertions enabled and a 15-second timeout. Re-verify all manifest hashes afterwards. No script was skipped. Script counts overlap and do not measure independent mathematical coverage.

G1 is refreshed for this candidate Linux snapshot only. Thirty selected COV categories remain partially addressed; none closed by the register. Independent mathematical/editorial review, supported platforms, release acceptance and canonical approval remain pending.
