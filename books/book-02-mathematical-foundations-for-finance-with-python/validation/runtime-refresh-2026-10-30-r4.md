# Book 02 — Full pinned runtime refresh V-40

**Date:** 2026-10-30  
**Pinned source revision:** `fe24a814a26fb542c7b5d6e0f34a0df8ff6eb6a7`  
**Disposition:** Scoped candidate execution passed; independent review and release acceptance pending.

This ninth refresh includes the three Section 16.2–16.4 derivative stencil corrections and their new checker after V-39. Counts were derived from the pinned Git tree.

| Actual check | Result |
|---|---:|
| Python sources compiled | 468/468 |
| check_/test_ scripts, each a separate process | 257/257 zero exits |
| Required source/fixture Git blob hashes, before execution | 469/469 |
| Same hashes, after execution | 469/469 |
| Failed scripts / timeouts | 0 / 0 |

[Complete machine record](runtime-refresh-2026-10-30-r4.json) contains the tree-derived manifest, exact blob hashes, every compiled path, command/environment and every script's stdout/stderr/exit/time. Required inputs are all Book 02 Python files plus `chapter-01/data/section-1.14-cases.json`. Reports written after execution are not represented as tested executable inputs.

Execution used Python 3.12.14 on Linux x86_64, assertions enabled, no `-O`; each script ran from its own parent directory with a 15-second timeout. Summed script wall time: 9.609 seconds. The snapshot was built by copying only bytes matching each pinned Git blob hash; all hashes were rechecked after execution.

For reproduction, check out the exact revision, verify the JSON manifest using Git's blob hash (`SHA1("blob "+byte_length+"\\0"+bytes)`), compile each listed Python file with `py_compile.compile(..., doraise=True)`, then run every listed check_/test_ file as `python <basename>` with its parent directory as cwd, a 15-second timeout and assertions enabled. Reverify the same input manifest afterwards. Counts include aggregate scripts that repeat checks; they do not measure independent substantive coverage.

The [derivative correction report](chapter-16-derivative-boundary-followup.md) retains initial failures and scoped reruns. All previous results remain historical evidence. G1 has scoped candidate runtime evidence at this source revision; G2–G8, supported platforms, independent review, final release revision and canonical approval remain open. Twenty-eight COV categories remain partially addressed; none is closed by this register.
