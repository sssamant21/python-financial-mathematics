# Section 7.10 — Eight scoped local answers

Original single-sector screen remains unchanged. Supplemental authored two-sector query/isin mechanics run on the validated fixture;this does not add a multi-sector public API. E5 retains the original maximum-row/tie-break policy. E8 proposes richer status/provenance fields without implementing a report writer or changing failure semantics.

## 7.10-E1

**Prompt:** Request all eligible equity rows and verify the order ALPHA, BETA, GAMMA.

**Scope:** EXACT SOURCE

Request limit10 to include all three eligible equity rows. Output order is ALPHA600,BETA600,GAMMA300,with input5,eligible3,returned3. Rank uses descending market value then ascending unique asset;all rows are validated before selection. This reporting subset is not a complete portfolio or a performance result.

## 7.10-E2

**Prompt:** Set floor to 600 and explain which boundary values remain.

**Scope:** EXACT SOURCE BOUNDARY

With floor600 and limit10,both ALPHA and BETA at exactly600 remain eligible;GAMMA300 is excluded. The floor is inclusive. A next-representable float above600 excludes those exact boundary values in the controlled fixture;this does not define a general financial materiality tolerance.

## 7.10-E3

**Prompt:** Reverse the source records and verify that a limit-one report still returns ALPHA.

**Scope:** EXACT SOURCE TIE-BREAK

Original and reversed source order both return ALPHA for limit1. Equal600 values are resolved by ascending asset,not by whichever record happened to arrive first. Source-index labels are retained as lineage but do not determine the financial ranking.

## 7.10-E4

**Prompt:** Compare filtering before head with taking head before filtering for the bond criterion.

**Scope:** SOURCE + ORDERING CONTRAST

Filtering for bond before limiting finds DELTA800 and returns it,with5input/1eligible/1returned. Taking raw.head(1) first leaves only BETA equity,then bond filtering yields no rows. These operations select different populations;early limiting cannot implement this screen.

## 7.10-E5

**Prompt:** Add a second eligible value tied at the cutoff and specify whether to preserve the maximum-row rule or include all ties.

**Scope:** EXACT SOURCE + DECLARED TIE POLICY

Append ZETA equity300 and request limit3. Four assets qualify,but ALPHA,BETA,GAMMA are returned because GAMMA sorts before ZETA at the tied300 cutoff. Preserve the original strict maximum-row rule and unique asset tie-breaker;the result is stable after source reversal. Including every cutoff tie would return4 and needs a different explicitly named contract,not a silent change.

## 7.10-E6

**Prompt:** Write an equivalent fixed query for an authored two-sector screen and compare it with isin-based filtering.

**Scope:** SUPPLEMENTAL FIXED QUERY

For authored sectors=(equity,bond) and floor300,compare raw.loc[(raw.market_value>=floor)&raw.sector.isin(sectors)] with raw.query("market_value >= @floor and sector in @sectors",local_dict={"floor":floor,"sectors":sectors},engine="python"). Both select source-order BETA,ALPHA,GAMMA,DELTA. The runner uses fixed bracket-based column access and validated fixture data. No expression text is interpolated and the original single-sector screen signature is unchanged.

## 7.10-E7

**Prompt:** Explain why a missing unselected market value still causes validation to fail.

**Scope:** EXACT SOURCE REJECTION

Set the unselected bond DELTA market value toNaN. The original equity screen rejects before filtering,so invalid source data cannot disappear behind the reporting criterion. Missing value is not observed0;source integrity is a full-input contract even when only a subset is displayed.

## 7.10-E8

**Prompt:** Design evidence fields that would let a reviewer distinguish no matches, rejected input and output truncation.

**Scope:** EXISTING COUNTS + EVIDENCE DESIGN

Existing criteria floor/sector/limit and input/eligible/returned counts distinguish no-match(5,0,0) from truncation(5,3,2). Propose explicit status=validated_no_matches/validated_results/rejected_input,was_truncated=eligible>returned,sort keys/directions,inclusive boundary,source snapshot hash,policy/runtime versions and source-context provenance. For rejected input,retain error category and validation-stage context and do not fabricate success counts or an empty successful report. These richer fields are a design;the current source raises errors and returns only its existing evidence for valid inputs.

Original source demonstration,discovery and compileall pass with FutureWarning as error. No unexpected QA failure or manuscript defect surfaced;first-run outputs and expected rejection traces retained. No historical unique methods or earlier workflow cases added by overlapping reruns. F28/F32,F37 history and platform/input/numerical/independent acceptance limits remain intact.
