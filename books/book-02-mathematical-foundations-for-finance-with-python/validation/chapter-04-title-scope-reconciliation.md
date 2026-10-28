# Book 02 — Sections 4.7–4.8 Title and Scope Reconciliation

**Date:** 2026-10-28  
**Disposition:** Display-title mismatch resolved; independent content review remains pending.  
**Manuscript/index corrections published through:** `699fc6ed37e469719bebe964f06b644e6a78b1ec`.

## Policy and decision

The Master TOC v1.0 identifies itself as the authoritative section sequence. Its Structure Change Policy says: “Preserve the exact chapter and section numbers/titles during manuscript development.”

The established titles remain in force. The manuscript headings, Chapter 4 index and previous/next labels were corrected to match them. This restores the approved curriculum rather than renaming established TOC entries; a TOC version change is therefore not needed. Existing manuscript filenames and links are preserved.

| Section | Former manuscript display title | Reconciled title |
|---|---|---|
| 4.7 | Stable Numerical Evaluation | Stable Evaluation Near Zero |
| 4.8 | Numerical Conditioning and Model Limits | Growth Assumptions and Model Limits |

## Scope comparison

Section 4.7 already explains small-return cancellation, log1p/expm1, log-space accumulation and stable periodic compounding. Its additional representation/range discussion supports the established near-zero evaluation topic. A scope paragraph now identifies this focus and points readers to Section 4.8 for model assumptions and sensitivity.

Section 4.8 already examines fixed rates, timing/day-count conventions, omitted cash flows, uncertainty, identifiability and contractual rounding. Its conditioning and perturbation material explains how uncertain growth inputs affect conclusions. A scope paragraph now relates those supporting tools to the established model-assumptions topic and later sensitivity/numerical-method chapters.

No derivations, exercise answers or Python algorithms were changed. This reconciliation does not independently certify their mathematical correctness.

## Verification and remaining work

Re-fetched both manuscripts, the Chapter 4 index, Section 4.6 navigation and the Master TOC after publication. Corrected file contents matched the intended edits; the five checked documents contained neither former display title. Both manuscript headings and the Chapter 4 entries now agree with the unchanged TOC titles.

Existing file paths were retained, so inbound path links remain valid. Rendered heading-fragment links and external navigation were not tested. No new Python runtime run was required for these prose/title changes; the prior pinned runtime result retains its original source-revision scope.

The title/scope portion of V-07 is resolved. Rendered-navigation, external-link, substantive coverage and independent editorial/mathematical review remain open.
