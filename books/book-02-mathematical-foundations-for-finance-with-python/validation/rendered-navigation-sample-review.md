# Book 02 — Rendered Navigation Markup Sample

**Date:** 2026-10-28  
**Revision:** `0bea5e36c769854e4e0ffdfc95ff361f69fe715e`  
**Status:** Sampled GitHub rendered markup passed; browser/visual and full-book review pending.

## Method

Fetched GitHub blob pages pinned to the revision above using Python urllib, with up to six concurrent GET requests and a 20-second timeout. Parsed the JSON-encoded richText article supplied by GitHub, then extracted rendered headings and anchor labels/href destinations using HTMLParser. This inspects GitHub's rendered Markdown output, rather than inferring links from source text.

No interactive browser was used. This is not screenshot verification, visual layout inspection, JavaScript interaction or actual click-through testing.

## Pages and results

All six pages returned HTTP 200 with rendered richText articles:

- Book README.
- Master TOC.
- Chapter 4 README.
- Sections 4.6, 4.7 and 4.8.

Fourteen automated checks passed:

| Check group | Passed |
|---|---:|
| TOC and Chapter 4 index: titles and destination paths for Sections 4.7–4.8 | 4/4 |
| Section 4.7–4.8 rendered H1 titles | 2/2 |
| Section 4.6–4.8 links to Chapter 4 index and Master TOC | 6/6 |
| Section 4.7–4.8 Previous section destinations | 2/2 |

Also inspected three extracted rendered links: the book index links to Chapter 4; the Chapter 4 index links back to the book index and Master TOC. The linked destinations were among the six fetched pages.

The rendered headings agree with the established titles: Stable Evaluation Near Zero and Growth Assumptions and Model Limits. GitHub resolved the sampled relative links to repository blob paths at the pinned revision.

## Limits and follow-up

This sample supports the Chapter 4 title/navigation reconciliation. It does not establish complete navigation coverage for 215 sections or all rendered headings. Section-ending Next statements were not counted as clickable links merely because they name the following section. No manuscript or Python source was changed by this check.

Keep V-07/G2 open until the agreed rendered-navigation scope and final-revision link inventory are completed. Next, expand the section-to-check inventory into substantive claims/example/exercise coverage, while retaining browser/visual navigation as a separate pending item.

Independent review, supported-platform checks and canonical approval remain pending.
