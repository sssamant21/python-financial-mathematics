# Book 02 — Anchor and Reference Link Audit

**Date:** 2026-10-28  
**Source revision:** `b0a48ed6b4dcbc36a3be906ff7a14e636370ec32`  
**Status:** Static scan complete for the syntax described below; rendered navigation and external URLs not validated.

## Results

| Measure | Count |
|---|---:|
| Markdown files scanned | 270 |
| Recognized inline Markdown link/image destinations | 3,278 |
| External destinations skipped | 535 |
| Local destinations checked against repository tree | 2,743 |
| Missing local paths detected | 0 |
| Local fragment destinations detected | 0 |
| Reference definitions detected | 0 |
| Explicit full/collapsed reference uses detected | 0 |
| Undefined explicit references detected | 0 |

No anchor destination was exercised: no local fragment links were detected. Zero unmatched fragments is therefore not evidence that rendered headings or table-of-contents anchors work. No reference definitions or explicit reference uses were detected; there were no defined reference-style links to resolve.

A separate raw-line scan found 18 lines containing fragment-bearing inline link syntax; inspected examples were external documentation URLs and were excluded from local anchor validation.

## Method

Fetched all 270 Book 02 Markdown files through the GitHub connector at the source revision. Repository path existence was checked against the recursive tree for that revision.

A Python static scanner removed backtick/tilde fenced blocks and inline code, extracted conventional inline destinations and full/collapsed reference syntax, normalized reference labels, resolved relative paths and percent escapes, and compared recognized local fragments with generated ATX heading IDs or explicit HTML IDs. Defined shortcut references were recognized only when their labels existed in the same file.

No missing paths, unmatched local fragments or undefined explicit references were reported by this scanner.

## Limitations

The scanner is a purpose-built regular-expression scan, not a CommonMark/GitHub renderer. Nested brackets/parentheses, multiline destinations/definitions, complex inline markup, indented code, HTML links, setext headings, duplicate-heading edge cases and GitHub-specific rendering may require separate review. With no local fragment destinations, the heading-ID approximation was not exercised by the repository data.

External URLs, including their fragments, were not requested. No claim is made about external availability, rendered navigation or semantic correctness. The Chapter 4 title/scope mismatch remains open.

## Next work

Prepare the Section 4.7–4.8 title/scope reconciliation against the curriculum policy. Complete rendered-navigation and external-link review separately, recording scope and actual evidence before closing the curriculum/navigation gate.
