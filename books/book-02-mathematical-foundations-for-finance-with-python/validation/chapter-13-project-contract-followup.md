# Chapter 13 — Project input and report contract follow-up

**Date:** 2026-10-29  
**Implementation blob tested:** `48647a15f502b812fe2cd33343f048c842c0ef8f`  
**Disposition:** COV-66 partially addressed; independent review pending.

The [new checker](../chapter-13/code/check_project_contract.py) exercises the Section 13.9 project entry point directly. Sixteen cases cover NaN, positive/negative infinity and boolean inputs in sensitivities, target, scales and limits. Further cases cover nonpositive scales, negative limits, duplicate factor/instrument labels, malformed matrix shapes and incomplete/nonstring unit metadata.

The reference report is checked for required fields, all three standardized residuals (-1/3,-1/3,1/3), exact retained unit metadata, solver identifier and false certification flag. The valid invocation preserves its input objects. Two repeated calls produce identical sorted, strict JSON when serialized by the checker; this does not claim that the project CLI itself uses sorted keys or a versioned schema. Schema checks require these fields, without forbidding future additions.

All 24 Chapter 13 Python files compiled and all 14 check scripts exited zero on Python 3.12.14/Linux, assertions enabled and a 15-second per-script timeout. The local implementation blob matched GitHub; implementation unchanged. This scoped run includes the preceding QR and ridge checkers and follows the [third full-book refresh](runtime-refresh-2026-10-29-r3.md).

## Remaining scope

Nonempty unit strings remain descriptive metadata; callers must ensure compatible sensitivities, targets, scales and limits. The report still does not retain the complete validated input configuration, a versioned schema or source provenance. These selected negative and report checks do not establish general range stability, independent business acceptance or full input-path coverage.

COV-66 remains partially open. Independent mathematical/editorial review and release approval remain pending.
