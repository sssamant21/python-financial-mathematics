# Book 02 — Coverage-gap remediation register

**Updated:** 2026-10-29
**Scope:** Selected follow-ups after the 215-section substantive mapping pass.
**Disposition:** Nine COV categories partially addressed; none closed by this register.

This register separates concrete changes from remaining obligations. It is not a completion percentage for the ninety categories: categories differ in scope, overlap and contain manual proof/review requirements. Earlier chapter fixes remain in their own records.

| Category | Concrete result | Remaining scope | Evidence |
|---|---|---|---|
| COV-61 | Section 12.5 rank_A no longer depends on target magnitude; column-equilibration policy disclosed; selected scale/zero/near-dependent cases added. | Larger pivot/scaling cases and independent numerical-rank review. | [Rank](chapter-12-rank-target-scaling-followup.md) |
| COV-69 | Section 14.9 computes/reports covariance eigenpairs; closed-form roots, projectors and direct residual/reconstruction checks added. | Independent review and broader numerical/interface scope. Fixed compression bound and input/unit metadata now asserted. | [Eigenpairs](chapter-14-covariance-eigenpair-followup.md) · [Compression bound](chapter-14-compression-bound-followup.md) |
| COV-70 | Section 15.9 second-order contractions checked by a Decimal path expansion across nine shocks; signed/absolute portfolio errors implemented and asserted. | Final-assessment/shared-dependency coverage and independent derivation/unit review. | [Taylor](chapter-15-taylor-oracle-followup.md) |
| COV-71 | Section 15.2 finite-difference representability and denominator guards aligned with related helpers; boundary tests added. | Perturbation asymmetry, step accuracy/convergence and selected Hessian numerical benchmarks. | [Scalar difference](chapter-15-scalar-difference-followup.md) |
| COV-74 | Section 16.9 now evaluates metrics, normalized loss/gradient and acceptance per candidate; independent residual metrics and selected failed candidates/holdout/budget cases checked. | Broader invalid-data, optimizer/threshold and independent-review scope. | [Candidate acceptance](chapter-16-candidate-acceptance-followup.md) |
| COV-82 | Section 19.6 stage/controller/rejection policy checked with Fraction stability references and callback traces; nine faulty variants detected. | Broader adaptive ODE behavior, numerical range, failure modes and independent review. | [Adaptive policy](chapter-19-adaptive-policy-followup.md) |
| COV-83 | Section 19.9 retains validated inputs/schedule and model/policy metadata; selected negative-jump/adjacent-time/log and JSON cases added. | Broader event numerics, cross-section policies and independent review. | [Provenance](chapter-19-input-provenance-followup.md) |
| COV-87 | Section 20.5 now raises explicit numerical-range errors for unrepresentable error magnitudes; exact tolerance comparison remains independent; extreme/subnormal cases added. | Section 20.6 now also validates numeric inputs/results and empty-portfolio rates. Other duplicated contracts/ranges, underflow interpretation and independent review remain. | [Error range](chapter-20-error-range-followup.md) · [PV contract](chapter-20-metamorphic-contract-followup.md) |
| COV-89 | Section 21.9 adds first-derivative finite-difference diagnostics, deterministic JSON, selected schema and injected failure propagation checks. | Broader interfaces, error paths and independent review. | [Integrated diagnostics](chapter-21-integrated-diagnostics-followup.md) |

The initial seven follow-ups through Section 21.9 are included in the [full runtime refresh](runtime-refresh-2026-10-29.md) at `37aac57a72303a6d4178790f8d172495e2bc0ada`: 444/444 compiled files; 233/233 script exits zero. The subsequent Chapter 14 compression-bound change has a 21-file/11-script scoped pass; Chapter 16 candidate acceptance has a 20-file/10-script scoped pass. Chapter 20 error-range reporting has a 19-file/10-script scoped pass. These follow the earlier full run. This execution evidence does not close the remaining column.

## Next executable and manual work

1. Section 14.9's selected compression-bound assertions are complete; continue the remaining numerical-contract/oracle obligations and independent review.
2. Continue numerical-contract and oracle items from the [prioritized queue](substantive-coverage-index.md), preserving exact expected behavior and scope.
3. Review unasserted exercise/proof, unit, model-assumption and editorial obligations with named independent reviewers.
4. Complete navigation/environment/release gates in the [review checklist](remaining-review-checklist.md).

When closing an item, record the exact sub-obligation, reviewer/evidence and revision; never promote the whole category solely because one selected example passed.
