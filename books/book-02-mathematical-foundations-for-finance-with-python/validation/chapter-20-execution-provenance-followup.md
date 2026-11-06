# Section 20.7 actual execution provenance

[Baseline source](https://github.com/sssamant21/python-financial-mathematics/blob/afda7a09f82b9067a77e89a29cd1a3c6af77b003/books/book-02-mathematical-foundations-for-finance-with-python/chapter-20/code/section_20_07.py) · [Corrected source](https://github.com/sssamant21/python-financial-mathematics/blob/641c6ad0304d242fd3a780b12908726b4778d724/books/book-02-mathematical-foundations-for-finance-with-python/chapter-20/code/section_20_07.py) · [Synthetic baseline](chapter-20-execution-provenance-baseline.md) · [Raw observations and exact blobs](chapter-20-execution-provenance-followup.json).

The initial 14-case run found 13 missing behaviors and its first implementation passed all 14. The expanded 21-case run found 20 mismatches on the baseline; all 21 passed with the new recorder. These are observations against a new execution contract, not 20 defects in the deliberately synthetic template. The default still writes a pending manifest.

The checker uses a temporary local Git repository. It independently queries the fixture commit and interpreter, hashes the tracked source bytes, and runs the worker separately to compare actual exit codes and byte streams with fixed expectations. It exercises a clean success (zero-rate PV = 100), an invalid rate with an untracked file, a tracked edit with a different valid amount (PV = −17.5), oversized input and untracked source refusal. The recorder retains the before and after source observations, explicit argv, worker outcome, and pending review and approval flags.

Replay from `chapter-20/code` at the corrected revision: `python check_execution_provenance.py`. To replay the expanded baseline, pass the absolute path to the baseline revision's `section_20_07.py` as the checker's sole argument. The temporary fixture commit IDs can differ between runs and are checked against their own Git observations. See the [full Linux candidate run](runtime-refresh-2026-11-06-r11.md).

This is selected COV-86 evidence. It does not establish authenticity, uninterrupted source state, crash-safe publication, independent review, supported-platform validation, release acceptance, or canonical approval.
