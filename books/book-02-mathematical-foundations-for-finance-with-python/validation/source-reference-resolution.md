# Book 02 — Federal Reserve and NIST Reference Resolution

**Date:** 2026-10-28  
**Status:** Identified citation/link findings resolved; independent source review remains pending.

## Federal Reserve

Inspected the official SR 26-2 letter and its guidance attachment:
https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm
https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf

The letter identifies SR 26-2, dated April 17, 2026, as replacing SR 11-7. Updated all twelve previously identified manuscript references in Chapters 20–21 to the dated SR 26-2 title and official landing page. The old URL appeared in reference lists, not historical discussion requiring preservation of the old document.

Sections 20.1 and 21.1 now distinguish banking model-risk context from the book's educational checklists. No assertion of regulatory compliance, applicability to every teaching calculation or prescribed release requirements is made. No numerical formula or Python implementation changed.

## NIST

Inspected the official project:
https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software

The retrieved page identifies Combinatorial Methods for Trust and Assurance and discusses software test methods and input-space coverage. Replaced the broken CSRC software-quality-group reference in Section 20.8 with this specifically named background source.

The guessed old NIST group path redirects to a different organizational topic and was not substituted merely because it resolved. Section 20.8 now explicitly separates testing background from the book's illustrative release-gate decisions.

## Verification

Retrieved the two replacement landing pages and the Federal Reserve attachment through web retrieval and inspected their content. This resolves source identity and relevance beyond the earlier HTTP-only scan; it does not assert that direct urllib requests always succeed or that browser navigation was tested.

All twelve updated manuscripts were re-fetched through GitHub and compared byte-for-byte with the intended edits; all matched. The corrected reference lists contain neither the old SR 11-7 URL nor the broken NIST CSRC group URL.

The earlier external URL audit remains historical evidence: 99 initial HTTP 200 responses and three 404 responses, with MathWorld repaired separately. It should not be reinterpreted as a fresh 102-URL rerun.

## Remaining work

Rendered navigation, release-revision link inventory, substantive claims-to-evidence coverage, independent mathematical/editorial/source review and supported-platform validation remain pending. The V-07 reference-repair subtask is resolved; the overall navigation gate remains open.
