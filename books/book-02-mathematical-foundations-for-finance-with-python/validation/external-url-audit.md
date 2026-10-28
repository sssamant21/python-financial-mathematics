# Book 02 — External URL Audit

**Date:** 2026-10-28  
**Inventory revision:** `b0a48ed6b4dcbc36a3be906ff7a14e636370ec32`  
**State:** Historical reachability scan completed; identified references subsequently repaired. [Source-resolution evidence](source-reference-resolution.md). Rendered navigation pending.

## Method and results

Extracted 102 distinct HTTP(S) destinations from conventional inline Markdown links in the 270-file snapshot. Used Python urllib GET requests with a 12-second timeout, redirects enabled and up to 12 workers. Response bodies were sampled up to 2,000,000 bytes; HTML fragments, where supplied, were compared with explicit id/name attributes in that sample. These are HTTP observations, not browser rendering or source-quality certification.

99 destinations returned HTTP 200 and three returned HTTP 404. No supplied HTML fragment was reported absent from the inspected samples. A 200 response can still contain a soft error, access wall or unsuitable content; JavaScript-generated content was not rendered.

## Findings

| Reference | Initial outcome | Disposition |
|---|---|---|
| MathWorld /DescartesSignRuleofSigns.html | 404 | Verified /DescartesSignRule.html returned 200 and corresponds to Descartes' Sign Rule; corrected Section 18.5 |
| Federal Reserve /supervisionreg/srletters/sr1107.htm | 404 | Appears in 12 manuscripts across Chapters 20–21; replacement and citation currency require review |
| NIST CSRC /projects/software-quality-group | 404 | Appears in Section 20.8; replacement requires source-scope review |

The Federal Reserve's historical SR 11-7 PDF at /boarddocs/srletters/2011/sr1107a1.pdf and a NIST /itl/ssd/software-quality-group candidate returned HTTP 403 when requested directly. A 403 is an access result, not proof of a broken document. Neither candidate was silently substituted.

Official Federal Reserve search results identify SR 26-2 (April 17, 2026) as replacing SR 11-7. That creates a citation-currency question beyond URL repair. Before changing the twelve references, inspect the current guidance and distinguish historical educational attribution from current regulatory claims. Relevant official entry: https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm .

## Scope and follow-up

The snapshot predates the subsequent title reconciliation and audit-document additions. This audit does not claim to cover newly added links or all Markdown/HTML syntax. No Python algorithm changed; the existing runtime report retains its original pinned source scope.

1. Federal Reserve references were updated to SR 26-2 with scope notes; see the subsequent source-resolution report.
2. Section 20.8 now identifies the NIST combinatorial-testing project as background, with its scope clarified.
3. Recheck corrected/new destinations and perform rendered-navigation review.
4. Repeat the agreed link inventory at the eventual release revision.

The curriculum/navigation gate remains open. Independent source review and canonical approval are not granted.
