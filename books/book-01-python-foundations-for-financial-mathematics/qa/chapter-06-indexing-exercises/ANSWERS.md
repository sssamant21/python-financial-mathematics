# Section 6.4 — Eight scoped answers

Prerequisites: the Section 6.1 prepared runtime, unchanged sibling source/test listings, and the published finite nonnegative float64 table with unique tuple IDs. Caller retains chronology, original label alignment and consistent units. Review: Codex executor, 2026-10-30; not an independent acceptance decision.

## 6.4-E1

Select B then C for the final two observations and derive expected values, labels, and shape.

**EXACT SOURCE + INDEPENDENT TABLE ORACLE**. Select B,C using select_instruments, then take [-2:,:]. Manual row/column lookup gives [[76,51],[78,52]], shape (2,2), instrument labels (B,C) and observation positions (1,2). Controlled observation labels obs1,obs2 are synthetic positional identifiers, not parsed dates. Output remains independent of the original table.

## 6.4-E2

Add a test for a zero slice step and distinguish that failure from an empty slice.

**SUPPLEMENTAL SOURCE PROBES**. source[::0] raises ValueError: zero cannot define a slice stride. source[99:100] is a valid empty slice of shape (0,3); source[99] instead raises IndexError. The runner adds explicit exception predicates without modifying the original eight-method suite. All expected traces are retained.

## 6.4-E3

Combine latest-price conditions of at least 50 and below 100 with an explicit column mask.

**SUPPLEMENTAL MASK + INDEPENDENT TABLE ORACLE**. Use mask=(source[-1]>=50)&(source[-1]<100). Final stored values 103,78,52 produce False,True,True. source[:,mask] is [[80,50],[76,51],[78,52]], shape (3,2), labels B,C. Retain all observation labels. The last row is latest only under the caller chronology precondition; this nominal-price mask is not an investment rule.

## 6.4-E4

Add an independent observation-label tuple and reverse it together with rows.

**SUPPLEMENTAL LABEL ALIGNMENT + STORAGE PROBES**. Introduce the independent tuple (obs0,obs1,obs2). Pair observations[::-1] with source[::-1,:], giving obs2:[103,78,52], obs1:[105,76,51], obs0:[100,80,50]. Apply the same reversal to both axes of meaning; reversing only labels would misidentify data. The basic reverse shares storage; copy it for an independent scenario. These labels demonstrate positional alignment and do not establish calendar validity.

## 6.4-E5

Demonstrate why a full-table boolean selection cannot be interpreted as a date-by-instrument table.

**SUPPLEMENTAL CELL SELECTION + CONCEPTUAL AXIS REVIEW**. source[source>=100] yields [100,105,103] with shape (3,), not a two-axis table. Matching coordinates are (obs0,A),(obs1,A),(obs2,A). Retain coordinates separately with nonzero if identities matter. This particular fixture coincidentally selects one A cell per row; arbitrary full-table masks may select unequal numbers of instruments per observation. A reshape cannot restore general missing axis information.

## 6.4-E6

Add a test proving an invalid unselected source column still fails under this selector's policy.

**EXACT SOURCE REJECTION PROBES**. Put NaN, positive infinity, then -1 in column B on separate disposable copies and request only A. Each original select_instruments call raises ValueError before selection because validation covers the whole source. Byte comparisons prove rejection did not edit it. Do not silently filter invalid columns first: that would change the published policy.

## 6.4-E7

Compare direct indexed assignment with editing an advanced-index copy on a disposable source.

**SUPPLEMENTAL OWNED-MUTATION PROBES**. On a disposable copy, advanced=disposable[:,[0,2]] returns independent storage. advanced[0,0]=999 leaves disposable unchanged. disposable[0,[0,2]]=[999,888] directly changes its first row to [999,80,888]. The original fixture stays intact. This contrasts retrieved-copy editing with direct indexed assignment; it does not make statements about concurrent writers.

## 6.4-E8

Design an explicit no-match policy for a downstream report without changing the selector silently.

**EXACT SOURCE EMPTY RESULT + SUPPLEMENTAL REPORT POLICY**. Choose a downstream report policy that emits explicit status NO_MATCH, instrument_ids (), the retained observation tuple, shape (3,0), and valuation None. A controlled threshold above 1000 produces no requested IDs; the unchanged source returns its permitted (3,0) table. The supplemental dictionary construction demonstrates this policy without manufacturing zero prices, placeholder instruments, returns or a successful complete valuation. MATCHED means selection matched, not financial validity. A serialized/report API and user interface are not implemented; future downstream calculations must branch on status before reductions. The selector itself remains unchanged.
