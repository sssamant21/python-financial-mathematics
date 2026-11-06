# Chapter 21 — Substantive coverage map

**Date:** 2026-10-28
**Inspected revision:** `b3d4cebc1d7053119dcb16e3ce66f2dfdfc7b238`
**Status:** Ten sections mapped; independent review pending.

Compared180 worked examples in21.1–21.9, fifty-eight cumulative questions, applied tasks and twelve-step labs with assertions and implementations. No new execution. [Pinned runtime evidence](pinned-revision-runtime-validation.md) is the run record. Catalog checks, model computations and independent acceptance are separate.

## Section/exercise map

| Section | Actual assertions | Exercise disposition |
|---|---|---|
| 21.1 | [Checks](../chapter-21/code/check_section_21_01.py): eight F1–F8 keys, pending execution/review/approval, missing source/result, required-field presence, fresh nested requirements copy. | All E1–20 are contracts/interpretations or numeric illustrations; this catalog does not run the PV examples E4–6 or domain checks E9–12. E16/E19–20 have pending/presence support only. missing_fields treats None as missing, not blank/invalid values; no evidence authentication. |
| 21.2 | [Checks](../chapter-21/code/check_section_21_02.py): six module names, nonempty inputs/output/errors catalog entries, missing/blank/type rejection, deep-copy independence. | E1–20 interface/dependency/math/interpretation statements not implemented as individual operations here. E10–13 numeric PV/derivative/bp cases are tested in later modules. Catalog completeness does not establish actual interface conformity, dependency acyclicity, output diagnostics or units. |
| 21.3 | [Checks](../chapter-21/code/check_section_21_03.py): zero-rate/time, log2 PV, annual-effective125-to100, equivalent factor conversion, effective log2-to1, empty and split, invalid convention even empty, rate boundary/time/NaN/bool/overflow. | E3–5/E8–12/E15–18 direct. E1–2 factor identities indirectly through PV. E6–7 negative-rate behavior/E13 equal-numeric convention difference/E14 fractional year/E19 permutation/E20 underflow not explicitly asserted. These remain selected missing numeric/interpretation cases. |
| 21.4 | [Checks](../chapter-21/code/check_section_21_04.py): zero-rate PV/derivatives, zero horizon and signed derivative, log2 value, bp change, Taylor levels98/98.02, central derivative, invalid zero/tiny/overflow step and domain/NaN/overflow. | E1–7/E10–12/E14–16/E18 have direct cases/formula evidence. E8–9 monotonicity not explicitly compared; E13 exact shocked PV/error absent. E17/E19–20 error/financial interpretation manual. No step sweep or second derivative independent numerical check. |
| 21.5 | [Checks](../chapter-21/code/check_section_21_05.py): reference solution(1,2), residual, identity, second example(2,2), singular consistent/inconsistent/zero, malformed/NaN/bool/threshold and nearly singular rejection. | E4–6/E10–11/E13–14 selected numeric/rejection support. E7 cost50/E8 raw determinant1 not directly reported/asserted; normalized determinant is a different quantity. E1–3/E9/E12/E15–20 units/condition/economic interpretation manual. Threshold screening is not a condition-number estimate. |
| 21.6 | [Checks](../chapter-21/code/check_section_21_06.py): interior0.75/0.25/objective0.005, both clipped boundaries, feasible-target zero objective, feasible/equality/long-only failures, feasible nonoptimal comparison, negative tolerance/nonfinite/bool/objective overflow. | E3–5/E7–12/E15 direct or related values; E5 signed equality residual not explicitly compared. E10 nonoptimal objective0.13 is only ordered, not asserted exact. E1–2/E6/E13–14/E16–20 feasibility/global proof/units/review manual. Fixed analytic quadratic, not general optimizer. |
| 21.7 | [Checks](../chapter-21/code/check_section_21_07.py): zero rate/time/flow, subnormal contribution, exact doubling, negative unconstrained balance, zero crossing, transition composition, invalid time/NaN/bool/overflow and pending report. | E5–9/E11–13/E15/E18 direct finite examples. E1–4/E10/E14/E16–17/E19–20 units/event policies/interpretation manual or unasserted. Report input/unit/boundary-policy fields implemented but not fully checked. No depletion policy is promised by unconstrained transition. |
| 21.8 | [Checks](../chapter-21/code/check_section_21_08.py): six plan cases, unique IDs, layer names, nonempty fields, type/missing and deep-copy behavior, pending execution/review/approval. | E1–20 explain testing/math/probability/review. Numeric examples E6–9 are plan descriptions, not executed model checks in this suite. A six-case plan is not comprehensive toolkit coverage. Probability/simulation assumptions remain manual transition material. |
| 21.9 | [Checks](../chapter-21/code/check_section_21_09.py): all five integrated reference outputs, derivative pair, replication residual, allocation feasibility/objective, ending balance, pending status, nonempty limitations and replication/allocation input fields. | E1–3/E5–6/E8–11/E13 direct; E4 bp-0.02 unasserted. E7/E12/E14–20 model/provenance/approval interpretation manual. Numeric integration is meaningful through imports21.3–21.7, not one coherent investable portfolio. |
| 21.10 | [Checks](../chapter-21/code/check_section_21_10.py): continuous/effective PV and conversion roundtrip, derivatives/Taylor levels, replication/singular rejection, allocation/nonoptimal feasible candidate, zero-rate/negative account and pending report. | Q10/Q16–18/Q23/Q25/Q29/Q33/Q37–39/Q43/Q45 direct selected evidence. Q30 residual tested21.5/21.9, not final check. Q9/Q11/Q14–15/Q24/Q26/Q28/Q31–32/Q36/Q44/Q46 omitted exact numeric cases or covered elsewhere. Q1–8/Q12–13/Q19–22/Q27/Q34–35/Q40–42/Q47–58 definitions, derivations, evidence/design/review tasks manual. Fifty-eight questions are not twelve comprehensive executable tests. |

## Integration and contract scope

21.9 build_report imports actual component implementations and retains scenario inputs added in the [focused capstone review](chapter-21-capstone-review.md). Reference checks assert target replication [3,5] and allocation target_a0.7, but not every input, convention, unit, threshold, finite-difference step or limitation. Sensitivity integration reports analytic derivatives only; the module contract mentions finite-difference diagnostics, units and step. No central-difference result or approximation error is included in this integrated report.

The report uses fixed synthetic examples. It does not accept arbitrary scenario inputs or test invalid-data propagation through orchestration. Individual suites cover many expected exceptions, but integration has no failing module injection test. Repeated calls in separate tests are not a determinism assertion or serialized schema check. CLI uses pprint rather than a versioned JSON artifact.

21.1/21.2/21.8 intentionally create catalogs/plans, not execute their listed financial tests. Copy and field-presence assertions are useful software evidence, but cannot establish authenticity, correctness of a reviewer, source/environment identity, actual F1–F8 fulfillment or a release decision. Pending status is appropriate even though the scenario itself computes values; actual historical execution is separately recorded.

The capstone replication and allocation interfaces are positional rather than financially labeled. Their mathematical shape checks do not prevent economically misassigned rows/assets.21.5 returns a normalized determinant screen and residual but no general conditioning diagnostic.21.7 is an unconstrained final-state transition, not a trajectory/event engine. These are stated teaching limitations, not automatic missing general-purpose features.

21.3 effective/continuous equivalence has selected reference evidence, but fractional horizons, negative rates, extreme conversion approaching effective-1, underflow and permutation are incomplete.21.4 has meaningful tiny-step/2h-overflow guards and21.7 a subnormal-flow regression; neither provides general range certification for all copies or extreme target/flow cancellation.

Final twelve-step lab requests analytic versus numerical sensitivity, boundaries, evidence and independent review. Some numeric tasks are covered in earlier module checks, not repeated in21.10; source/version/commands/outputs/reviewer fields are tasks for actual validation artifacts. No grading, independent review or authorization is inferred.

## Open gap register

| ID | Gap | Required next evidence |
|---|---|---|
| COV-88 | Catalog/plan completeness is distinct from fulfilled interfaces and requirements; claims/provenance fields are only syntactically tested. | Map F1–F8 to actual module/report/manual evidence; reconcile proposed versus implemented diagnostics and keep review/approval pending. |
| COV-89 | Integration report lacks selected numerical diagnostics and full schema/provenance assertions; fixed successful examples do not test failure propagation or deterministic serialization. | Meaningful integrated input/convention/diagnostic/schema checks and documented error behavior; reconcile report format and retained evidence. |
| COV-90 | General interpretation, exact cumulative numeric cases and range/boundary variants exceed selected toolkit tests. | Independent proofs/units/scope review and selected required conversion/sensitivity/replication/account cases; preserve limited-solver and unconstrained-account distinctions. |

These extend COV-01–COV-87; ninety coverage categories are not ninety proven defects. No code/manuscript changes or runtime execution for this map. Independent mathematical/editorial review and canonical approval remain pending.

## Subsequent COV-89 remediation — 2026-10-29

The [integrated diagnostics follow-up](chapter-21-integrated-diagnostics-followup.md) adds centered first-derivative diagnostics with step/error/units, deterministic JSON output, selected report-schema checks and injected failure propagation. All 19 chapter files compiled and 10 scripts passed; Section 21.9 passed 18 unittest methods. COV-89 remains partially open for broader interfaces/error paths and independent review. Original map evidence remains historical.


## Capstone valuation and analytic sensitivity — V-76 (2026-11-05)

[Section 21.3 rate and valuation evidence](chapter-21-capstone-rate-range-followup.md) retains ten baseline mismatches and a 53-case pass. Independent effective gross-power, continuous exponential and conversion references cover fractional horizons, negative rates, the rounded-minus-one boundary, complete term scaling and the actual capstone cash-flow field. Conversion code is unchanged. Chapter scope at `239085a0580b7a97db6787e415c36f20d11f706c`: 20 files compiled and 11 scripts passed.

[Section 21.4 sensitivity evidence](chapter-21-capstone-sensitivity-range-followup.md) retains 17 baseline mismatches and a 32-case pass. Selected independent complete PV, derivative and Taylor references and the actual capstone analytic field verify the corrected scaling; finite-difference stencil guards are unchanged. This adds selected partial COV-90 evidence, not a general range proof.

[V-76](runtime-refresh-2026-11-05-r18.md) compiled all 540 Python files, passed all 327 discovered scripts and matched all 541 required source/fixture hashes before and after at `77a943c4ee6551431485c3a53d71f789691c2392`. Final Chapter 21 scope: 21 compiled files and 12 passing scripts. Thirty-four selected COV categories are partially addressed; none closed. Independent review, supported platforms and release approval remain pending.

Next substantive item: Section 21.5 replication screening, solve and residual ranges. Derive independent normalized determinant and pivoted-solve expectations, check the declared screening threshold separately from singularity, and check residuals on the returned represented holdings. Include selected finite results hidden by overflowing intermediate products and the actual integrated report path. Preserve the limited 2x2 interface and do not repeat the Section 20.2 benchmark fixtures as new coverage. Chapter 21 actual provenance and independent review, Section 19.8's end-period exponent boundary, and other manual obligations remain open.

## Capstone replication and allocation — V-77

[Replication](chapter-21-capstone-replication-range-followup.md) records five baseline mismatches and a 14-case pass against independent pivoted elimination, exact screening and residual checks on returned holdings. [Allocation](chapter-21-capstone-allocation-range-followup.md) records seven baseline mismatches and a 20-case pass against a high-precision projection and represented-weight feasibility reference. Both check the actual integrated report fields. Section 21.5 keeps its two-by-two screen; Section 21.6 keeps its two-weight teaching objective. These are selected additions to COV-90. Thirty-four selected COV categories are partially addressed; none closed.

[V-77](runtime-refresh-2026-11-05-r19.md) compiled 542 files, passed 329 scripts and matched 543 required blobs before and after at `bc29b0d67dfd61b3d522d36d956b768101fee0ab`. Chapter 21 scope: 23 compiled files, 14 passing scripts. Independent review, supported-platform evidence and release approval remain pending.

Next substantive item: [Section 21.7 baseline probes](chapter-21-capstone-account-range-baseline.md) reproduced four false overflow results in the unconstrained transition. Retain that initial evidence and build an independent account oracle for equilibrium, scaled growth and flow, cancellation and genuine overflow. Check the actual Section 21.9 account field and document the output underflow policy. Section 19.8's end-period exponent boundary, COV-88 provenance and requirement fulfillment, and wider manual obligations remain open.

## Capstone account and requirements traceability — V-78

[Account range](chapter-21-capstone-account-range-followup.md) retains 17 initial mismatches and a 29-case pass for the complete account transition and actual integrated field. It covers equilibria, scaled growth and flow, cancellation, signed zero, and genuine overflow while keeping the unconstrained final-state contract.

[Requirements and preflight evidence](chapter-21-capstone-requirements-evidence-map.md) maps F1–F8 to implemented evidence and manual obligations. It retains the cash-flow preflight failure and the 16-test pass: both row orders now report the invalid date before discounting, and a valid one-shot iterator still works. The map distinguishes proposed diagnostics from the actual report and its pending placeholders. COV-88 is newly partially addressed; COV-90 gains selected account evidence. Thirty-five selected COV categories are partially addressed; none closed.

[V-78](runtime-refresh-2026-11-05-r20.md) compiled 543 files, passed 330 scripts and matched 544 required blobs before and after at `59f713d346fbcbf14e7125902637cd2f6e2c56e4`. Chapter 21: 24 compiled files and 15 passing scripts. Independent review, supported platforms and release approval remain pending.

Next substantive item: [Section 19.8 end-period exponent baseline](chapter-19-end-period-exponent-baseline.md) records four finite-payment cases rejected under the documented exponent limit. Evaluate a bounded extension against independently derived end-period sums and genuine range failures; keep the Chapter 19 underflow contract. Wider Chapter 21 provenance, proofs and review remain open.

## Integrated capstone execution evidence — V-94

[Chapter 21 integrated run receipt](chapter-21-integrated-provenance-followup.md) records actual Section 21.9 CLI bytes, source hashes, command and exit. All ten checks passed, including changed-source and altered-output detection and a retained real import failure. The report itself remains unchanged and retains pending status. This adds selected COV-88 evidence. Thirty-five selected categories remain partially addressed; none are closed.

[V-94](runtime-refresh-2026-11-06-r13.md) compiled 559 files, passed 346 scripts and verified 560 required blobs before and after at `44c6a0bcd5d5e8e6ab8ac84e9691c89610d3ed3e`. Independent review, supported platforms, release acceptance and canonical approval remain pending.

Next: [Section 21.4 central-difference baseline](chapter-21-central-difference-range-baseline.md) reproduces two finite complete stencil values rejected by the actual helper. Check COV-90 centered-difference arithmetic, existing perturbation guards and the actual integrated diagnostic. Wider capstone requirements and manual reviews remain open.
