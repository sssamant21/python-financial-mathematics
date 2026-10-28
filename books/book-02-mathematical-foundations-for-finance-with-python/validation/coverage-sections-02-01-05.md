# Book 02 — Substantive Coverage: Sections 2.1–2.5

**Date:** 2026-10-28  
**Inspected revision:** `c0551fc371cf1d0fc0a39a35f12f87dff5204001`  
**State:** Five sections and thirty practice problems mapped; independent review pending.

Inspected the five manuscripts, implementations, numbered check scripts and the separate quadratic cancellation regression. Mapping now covers 30/215 numbered sections: Chapters 1 and 4 plus Sections 2.1–2.5. This is a mapping count, not a validated-content percentage. No new test execution or algorithm change occurred. Runtime evidence remains the [pinned full run](pinned-revision-runtime-validation.md) and [quadratic fix report](chapter-02-quadratic-boundary-review.md).

## Assertion sources

- [check_quadratic_cancellation.py](../chapter-02/code/check_quadratic_cancellation.py): `9d07b531a720af1a4ad4d0a33017544f86eb14a4`.
- [check_section_2_01.py](../chapter-02/code/check_section_2_01.py): `61305ddcdba45e1fb808928257e409a4ede3c456`.
- [check_section_2_02.py](../chapter-02/code/check_section_2_02.py): `3f4914e9a5c75269a81cca7849492ba46322152d`.
- [check_section_2_03.py](../chapter-02/code/check_section_2_03.py): `eb9b5fb22e21059ba824dc8827f7fe82cc7439ff`.
- [check_section_2_04.py](../chapter-02/code/check_section_2_04.py): `a1dffa1b6306364979b2eb18c9a8a92ad396defc`.
- [check_section_2_05.py](../chapter-02/code/check_section_2_05.py): `6cd90e7eb383bf3ddd52c3a5f0312281644888d2`.

## 2.1 — Algebraic Expressions and Equivalent Forms

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 expand 3P(1+r)-2P-F | Other expansion/equivalence grids | Exact collected coefficient 1+3r not directly asserted |
| P2 800,.05,4,.01 | Exact ending828 and return7/200 | Balance/decomposition agreement covered through function result; derivation manual |
| P3 changed gross-ending fee basis | Exact changed return69/2000 and difference1/2000 | Fee timing/basis interpretation manual |
| P4 cross term at .02,.03 | Product-minus-linear difference3/5000 | General distributive proof manual |
| P5 cancelled quadratic quotient | At x=4 original gives7 | x=3 exclusion and domain-preserving identity not directly implemented for this quotient |
| P6 invalid cancellation across subtraction | Matching principal100/rate.1/fee5 counterexample | Division restriction and general rewrite proof manual |

81 fee cases compare all returned forms with a separate net-interest-minus-fees accounting route; fifteen growth cases compare factored/expanded values with repeated accrual. Seven cancellation cases include mathematically allowed nonzero rates outside the financial-growth domain; zero is rejected. Twelve principal comparisons distinguish fixed-fee effects. Thirteen input rejections and a negative net return below -100% are checked: an affine fee model can create that outcome without admitting rate<=-1.

Finite identities do not prove general equivalence. Formula agreement also cannot establish which fee basis a real contract uses.

## 2.2 — Linear Equations and Rearrangement

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 expanded equation with x=8 | Both original sides equal25 asserted | No call solving that exact expanded input; reversible-operation reasoning manual |
| P2 zero coefficients and -3x+6=0 | Generic all/none grid plus matching unique2 | Constants7/8 not in small grid; positive-domain interpretation manual |
| P3 principal for target828 | Matching solution800, admissible | Full original substitution supported by solver/grid; derivation manual |
| P4 rate and recovered fee | Matching rate1/20 and fixed-fee equality4 | Formula rearrangement proof manual |
| P5 zero/negative collected coefficient | Grid covers zero-coefficient branches; explicit negative root-100 rejected financially | All positive-principal solution-set explanation manual |
| P6 simple annual interest | Exact30/(2000/4)=3/50; generic zero-coefficient all/none | No dedicated simple-interest inverse helper; nonnegative-rate solution set manual |

125 coefficient cases substitute unique roots and neighboring nonroots; 54 principal cases compare financial-domain membership with original equations; 43 admitted forward/inverse cases reconstruct rates. Tiny nonzero coefficient remains unique. Zero principal and rate=-1 algebraic candidates have zero residual but are inadmissible. Fourteen selected invalid calls are rejected.

Residual zero alone is not sufficient for financial admissibility. Finite sample points in an all/none branch do not replace its algebraic classification proof.

## 2.3 — Fractions and Rational Equations

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 common denominator at x=3 | Matching2/3 and nine non-pole integer samples | General numerator/domain derivation manual |
| P2 (x²-16)/(x-4)=8 | Cleared candidate4 equality asserted | Original undefined quotient not evaluated; exclusion argument manual |
| P3 (3x+2)/(x-2)=4 | Matching solver root10 and original substitution | Domain explanation manual |
| P4 (x+2)/(x-1)=3/(x-1) | Related pole-rejection examples and classification grid | Exact exercise equation/difference-one statement not directly asserted |
| P5 fee target with fixed6, rate.01 | Matching principal400, ratio.025; lower-target root-1200 inadmissible | Fee10 not separately asserted; q=.01 branch represented in grid |
| P6 fixed0, rate.02 targets.02/.03 | Matching all branch in grid; explicit .03 none | General punctured-domain interpretation manual |

243 rational-map cases use a determinant/constant-map classification route, with 1,215 original-membership samples. Thirty-six fee-target cases keep positive-principal restrictions separate from real roots. Explicit hole, punctured identity and empty-domain cases preserve exclusions; ten invalid calls sample interfaces.

The restricted solver handles a linear-over-linear ratio, not arbitrary rational equations, symbolic cancellation or inequalities. An undefined original expression retains no valid residual; that is checked for excluded candidates rather than replaced with zero.

## 2.4 — Powers, Roots, and Fractional Exponents

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 powers and zero policies | Exact4/9,1,0; zero^-1/zero^0 rejected | Built-in 0**0 comparison not asserted here; policy explanation manual |
| P2 exponent rules vs addition | Product/power identities checked at a=2 | Incorrect sum rewrite counterexample not explicitly asserted |
| P3 principal sqrt vs equation roots | sqrt49=7 and sqrt((-7)^2)=7 | Negative equation root-7 not explicitly enumerated |
| P4 rational exponents/negative roots | Matching27,.25,-3; negative even root rejected | General real-branch proof manual |
| P5 500-to605 over two periods | Matching .1 rate and rejection of naive .105 reconstruction | Interpretation of equivalent rate manual |
| P6 1000-to729 and zero periods | Matching -.1 rate; zero-period inference rejection | Equal/unequal zero-horizon solution-set classification manual |

Sixty exact-power cases use repeated multiplication; 32 planted nonnegative roots, twelve negative odd roots, seven sqrt references and forty endpoint reconstructions sample the approximate interface. Twenty-six selected invalid/range calls include index121, unsupported/nonfinite inputs, endpoint ratio over/underflow and a rate rounding to -1.

The common abs_tol=1e-12 can be permissive near zero; separate tiny sqrt references use abs_tol=0 and require positive results. These do not establish relative accuracy for every near-zero inferred rate. Index120 is exercised positively, but full supported-range accuracy and extreme-scale root reconstruction are not certified.

## 2.5 — Quadratic Equations

| Practice problem | Assertion evidence | Remaining review |
|---|---|---|
| P1 roots3,4 via factoring | Matching root tuple; planted-root grid checks Vieta/substitution for other roots | Matching polynomial's proof/substitution/Vieta prose manual |
| P2 completing square gives1,7 | Matching tuple | Completion steps and both-sign explanation manual |
| P3 repeated/no-real/irrational | Matching -3, no_real and exact spread_squared3/2 | Specific irrational root reconstruction described symbolically, not rational tuple |
| P4 break-even roots20,80 and cap60 | Original price/revenue/cost checked; cap filters to20 | Model assumptions/manual formulation review |
| P5 rate quadratic200,400,-42 | Both roots verified in original growth equation; admissibility leaves .1 | Financial-domain derivation manual |
| P6 degenerate quadratic and sqrt2 | a=0 rejected; symbolic irrational and approximate residual cases | Linear solution3 is not returned by this interface; interpretation manual |

Sixty planted rational-root cases verify classification, Vieta, original substitution and coefficient rescaling. Twenty-seven irrational descriptions compare Decimal roots at precision40 using scaled residual and root-sum checks at precision60, while preserving caller precision/rounding. Twelve no-real cases and twelve invalid calls sample other branches.

The separate cancellation regression covers eight sign combinations with |b|=10^50 at precision40. It compares each root with a precision160 direct-formula reference and requires relative root error and normalized residual <=10^-38. Both signs/coefficients are sampled; symmetric, repeated and no-real outputs are also checked. This supports the known cancellation fix, not universal Decimal accuracy or near-repeated-root conditioning.

Precision endpoints16/100, arbitrary exponent limits and extreme rational conversion are not meaningfully covered. The separated-root loop uses zip(actual,expected) without an explicit root-count assertion, so its comparison alone does not guarantee both roots are returned; ordinary cases assert tuples elsewhere.

## Additional gap register

| ID | Finding | Next evidence |
|---|---|---|
| COV-30 | Restricted rational/root interfaces do not cover all manuscript algebraic transformations | Manual scope/domain review and exact-input cross-map |
| COV-31 | Approximate roots/rates need broader scale-aware accuracy evidence | Independent references for near-zero rates and ill-conditioned roots |
| COV-32 | Decimal support limits and cancellation output cardinality not fully asserted | Precision endpoint/range cases and explicit separated-root count/order checks |

These extend COV-01–COV-29. Existing conceptual, exact-input mismatch and independent-oracle categories also apply. They are coverage findings, not demonstrated new implementation defects.

Next: Sections 2.6–2.10, including project and chapter assessment. Independent mathematical/editorial review, supported-platform validation and canonical approval remain pending.
