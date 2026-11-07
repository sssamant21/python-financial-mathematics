# Section 8.3 centered-difference copy follow-up

Baseline: `3bd554d420d7e3d60ca32b3e4b1a48d6f611858a`. Corrected executable tree: `a6441d707337946a76e059c6cf53a5b05291afa0`. [Exact blobs and observations](chapter-08-centered-copy-followup.json).

Eight wrapper observations pass. Six baseline mismatches are retained: four exercise actual callback/control/output behavior, while two require the newly established delegation contract. These are observations, not six distinct numerical defects.

Section 8.3 now delegates to Section 8.1's previously validated centered-difference implementation. Its default step remains 1e-4. Checks exercise invalid controls, nonfinite callback output, signed steps, retained default, helper identity and sentinel delegation with the original arguments. This verifies the actual Section 8.3 call path; it does not count inherited numerical checks as a new mathematical oracle.

Run `python check_centered_copy.py` from `chapter-08/code`. To replay, place both original Section 8.1 and 8.3 modules from the baseline revision in a separate directory, then pass that directory as the sole argument to the corrected checker. Retained baseline/replay observations match byte for byte. The missing-directory replay setup issue described in the [financial report](chapter-08-initial-pv-range-followup.md) led to explicit requested-module checks in both CLIs.

Both existing section regression scripts pass. [Full runtime V-103](runtime-refresh-2026-11-07-r09.md) includes this new checker. Other earlier helper copies and implicit-domain obligations remain open under COV-51; no independent approval or external gate is closed.
