# Section 7.1 — Eight scoped local answers

Original manuscript has prompts without a local companion answer block. These QA answers supply the review record; no absent-answer defect is inferred from that format. E1–E6 call the unchanged source or reproduce explicitly unguarded mechanics. E7 is a metadata design review, not integration execution. E8 is a separate renderer implementation, not a change to the source financial API.

## 7.1-E1

**Prompt:** Reorder the return Series three different ways. Confirm the validated portfolio return stays at 4.50%.

**Scope:** SOURCE + RATIONAL ORACLE

Reindex returns to ALPHA/BETA/CASH, BETA/CASH/ALPHA and BETA/ALPHA/CASH. Each original API call produces the same weight-ordered report and total9/200=0.045. Labels retain economic pairing; only the return row order changes.

## 7.1-E2

**Prompt:** Calculate the unaligned positional result of 2.50% by hand and identify each wrong asset pairing.

**Scope:** SOURCE MECHANICS + HAND DERIVATION

The wrong positional pairs are ALPHA weight0.6 with CASH return0, BETA weight0.3 with ALPHA return0.1, and CASH weight0.1 with BETA return−0.05. Terms0,0.03,−0.005 sum1/40=0.025. Correct identity alignment gives0.045, a2percentage-point difference. Matching array shapes cannot detect these mislabeled pairings.

## 7.1-E3

**Prompt:** Remove BETA from the returns. Explain why rejection is preferable to reporting ALPHA's contribution alone.

**Scope:** SOURCE + MISSINGNESS INTERPRETATION

Removing BETA raises ValueError before aggregation. An unguarded aligned product exposes BETA asNaN but defaultsum skips it and reports0.06; the missing negative−0.015 contribution makes that partial total exceed the correct0.045. CASH contributes0. Reporting only ALPHA is not a complete portfolio return, and neither zero filling nor renormalization is authorized.

## 7.1-E4

**Prompt:** Add an unexpected instrument. Explain why silently discarding it could conceal a data-source mismatch.

**Scope:** SOURCE + UNIVERSE POLICY

Append OTHER return0.02. Exact-set validation rejects it. Explicitly discarding OTHER recreates0.045 mechanically, but hides a possible wrong file,unexpected security,stale universe or mismatched weight population. Investigate the source and independently expected universe; a broad-reference filtering workflow would need an explicit different contract.

## 7.1-E5

**Prompt:** Replace BETA's return with NaN. Compare the unguarded default sum with the validated function.

**Scope:** SOURCE + UNGUARDED CONTRAST

Set BETA returnNaN without removing its label. Default sum of unguarded w*r reports0.06; sum(skipna=False) isNaN and the public function rejects the supplied nonfinite return. Unknown return is not observed0 and must not be converted into a complete performance result.

## 7.1-E6

**Prompt:** Supply duplicate labels and explain why a label-bearing object is not automatically a valid keyed dataset.

**Scope:** SOURCE + KEY CONTRACT

Duplicate labels on either input raise ValueError. pandas permits Series with repeated labels, so existence of an Index is not uniqueness validation. For this one-contribution-per-asset model enforce flat,unique,trimmed nonempty string identities and identical asset sets. A valid lot/transaction grain would need distinct keys and another explicit aggregation policy.

## 7.1-E7

**Prompt:** Describe the metadata needed to ensure all supplied returns cover the same interval and currency convention.

**Scope:** CONCEPTUAL METADATA DESIGN — NOT EXECUTED INTEGRATION

Retain stable security identifiers and identifier namespace/source version; common interval start/end instants,time zones,endpoint closure and observation/session calendar; price-only versus total-return methodology,corporate-action/adjustment/distribution basis; price currency and reporting currency,units/multipliers and FX basis; opening-weight valuation time/exposure universe and flow/rebalancing assumptions; event/publication/ingestion times,quote age/revision and source/batch evidence. Validate equality or an explicitly authorized transformation across inputs before calculation. Labels and finite numeric cells alone cannot enforce these fields; this API accepts no metadata object and does not authenticate their truth.

## 7.1-E8

**Prompt:** Extend the report renderer to show contribution percentage points. Preserve numeric return fractions in storage.

**Scope:** SUPPLEMENTAL RENDERER + UNCHANGED SOURCE

renderer.py consumes an already validated original report,total and formats only output strings. Weight/asset/portfolio returns use percentage formatting; contribution*100 displays6.00pp,−1.50pp,0.00pp,with sum4.50pp. Stored contribution fractions remain0.06,−0.015,0 and portfolio return0.045. rendered.txt and numeric-report.json retain both views; equality/dtype/copy checks establish that rendering does not mutate numeric storage. This is a small teaching renderer,not an arbitrary-input/reporting API.

Three original commands (demonstration,8-method discovery,compileall) and one supplemental renderer caller pass. First-run results retained with expected rejection traces; no unexpected failure or manuscript change. No Windows/macOS,notebook,source-authentication,arbitrary ingestion or independent acceptance is inferred.
