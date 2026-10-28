# Book 02 — Substantive Coverage: Sections 4.7–4.8

**Date:** 2026-10-28  
**Inspected source revision:** `fa0aeb8ad1954bb2b4168f0de8d2bfd5412a1da8`  
**State:** Two sections mapped; partial numerical evidence, manual review pending.

This is the first substantive mapping slice: 2/215 numbered sections mapped, not 2/215 validated. Other sections retain filename mapping only until a comparable content review is recorded. Runtime evidence remains the separately pinned [full run](pinned-revision-runtime-validation.md); no new runtime pass is claimed here.

## Assertion sources

- [4.7 checks](../chapter-04/code/check_section_4_07.py), blob `1d8fabc52c831997fc34642c1fc2bad3bb8a3ec5`.
- [4.8 checks](../chapter-04/code/check_section_4_08.py), blob `4474eaad16909052ca572534bef15a2b50d3a895`.

Both scripts place assertions in run(). “Spot check” means an executable example, not a proof or an independent implementation. Some expected values reuse the implementation's formula.

## Section 4.7 claims, examples and exercises

| Exercise / related claim | Existing assertion evidence | Remaining work |
|---|---|---|
| E1: log(1+tiny) can lose the increment | log(1+1e-16)==0; log_change positive and close to 1e-16 | Explain representability and platform assumptions independently |
| E2: continuous-to-simple return via expm1 | simple_change(1e-16) and conversion round trips | General formula/domain derivation and non-unit time example |
| E3: stable nominal-to-EAR formula | effective_annual_rate(.12,12) vs 1.01**12-1 | Derivation and broader frequency/rate cases |
| E4: +100%, -50% cumulative return | Both cumulative log/simple results close to zero | Written explanation review |
| E5: log space avoids intermediate product overflow | No direct overflowing-product-versus-finite-log example | Add independent range benchmark; manually review explanation |
| E6: stable functions cannot restore lost input precision | No explicit input-information-loss assertion | Conceptual/manual review |
| E7: inverse-time conditioning near zero rate | No direct sensitivity experiment in this script | Cross-map Section 4.8 carefully; review derivation and near-zero range |
| E8: Fraction/Decimal/float distinction | No representation comparison in this script | Conceptual/source review; do not count imported tools as assertions |

Additional spot checks cover periodic accumulation, a 10,000-zero sequence, 1,000 tiny returns, domain rejections, bool/nonfinite rejection and exponential overflow. The tiny-return sequence expected value uses the same log1p/expm1 identity, so it is not an independent oracle for that identity. The stated 1e-8 worked conversion is not explicitly the same input as the tiny-rate or round-trip cases.

## Section 4.8 claims, examples and exercises

| Exercise / related claim | Existing assertion evidence | Remaining work |
|---|---|---|
| E1: conditioning vs stability | No direct conceptual assertion | Manual definition and example review |
| E2: derivative of log FV w.r.t. rate is t | Value t=30 and central difference at h=1e-5 | General derivation, domain and truncation/rounding analysis |
| E3: 10 bp over 30 years gives about 3% | Exact relative change checked against expm1(.03) | Explicit first-order .03 error comparison and negative perturbation |
| E4: periodic log sensitivity n/(1+i) | One value 10/1.05 | Derivation and independent numerical/range checks |
| E5: full differential of implied rate | Ending-value derivative checked analytically and centrally at h=1e-3 | Initial-value/time partials and full differential review |
| E6: relative rate error undefined at zero | No F=P implied-rate/relative-error case | Add zero-rate absolute-error example; manual explanation review |
| E7: very small steps can worsen estimates | Zero/indistinguishable step rejection only | Step-size sweep with error comparison; rejection alone is not accuracy evidence |
| E8: precision cannot repair model assumptions | No executable coverage for business/model suitability | Manual review of assumptions, examples and intended use |

Additional assertions check one forward FV, implied rate, implied time, time sensitivity and invalid domains. The zero-rate rejection uses initial=100 and final=150: it does not exercise equal endpoints with zero rate, where time is not uniquely identifiable. Checking the implemented time sensitivity against its analytic expression is a spot check, not an independent conditioning proof.

## Gap register and disposition

| ID | Gap | State / proposed evidence |
|---|---|---|
| COV-01 | Step-size sweep claimed but not asserted | Wording corrected; meaningful sweep experiment pending |
| COV-02 | Equal-endpoint zero-rate nonidentifiability untested | Coverage wording narrowed; explicit case pending |
| COV-03 | First-order 3% approximation not explicitly bounded | Compare exact positive/negative perturbations with linear approximation |
| COV-04 | Full implied-rate differential only partly tested | Independently check all partials and derivation |
| COV-05 | Log-space overflow benefit lacks direct range benchmark | Construct finite-log/intermediate-product-overflow reference |
| COV-06 | Conceptual exercises and arithmetic/model limits | Named manual reviewer and evidence pending |
| COV-07 | Reused-formula reference values | Add independent high-precision or alternative-formulation oracles where useful |

These are coverage gaps, not demonstrated implementation defects. No trivial tests were added merely to raise a count. Manuscript runtime-status statements now point to existing evidence; independent mathematical/editorial review and canonical approval remain unchecked.

Next mapping slice: Sections 4.1–4.6, then the Chapter 4 project and integrated assessment. Expand across the remaining book without treating filename matches or aggregate reruns as substantive coverage.
