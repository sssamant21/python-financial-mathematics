# Book 02 — Section-to-Check Coverage Inventory

**Date:** 2026-10-27  
**Repository tree inventoried:** `644160125a4cbfa228e615322cd27a2f1ae29b75`  
**Status:** Filename and manuscript-reference inventory; substantive coverage review pending.

## Findings

- **215/215** numbered sections have a same-numbered check script by the naming convention examined. All 215 manuscripts contain the corresponding check filename.
- **211/215** have a same-numbered Python implementation. Four exercise sections use earlier modules: 2.10 uses 2.9; 3.10 uses 3.7–3.9; 20.10 uses 20.9; 21.10 uses 21.3–21.7 and 21.9. A missing same-numbered implementation is not automatically a defect.
- Every matching check contains at least one textual assertion-related token. This is a superficial static observation, not proof that assertions execute, cover all exercises, are independent, or are effective.
- The manuscript scan detected 21 fenced blocks labeled python or py in 21 sections. Unlabeled blocks, inline snippets, shell commands, external dependencies, and snippets encoded in other ways require separate analysis. None of these manuscript snippets was executed as part of this inventory.
- This inventory does not measure line, branch, mathematical, exercise or requirement coverage. Reference-check scripts can test only a subset of a section; mapping a script to a section is not section certification.
- The prior runtime pass tested a historical snapshot plus seven fixes, not necessarily this tree. See [runtime follow-up](runtime-failure-followup.md).

## Open work

1. Review each section's learning objectives, formulas, examples, exercises and lab steps against actual assertions and independent expected results.
2. Audit fixtures, dependencies, execution paths, skipped or unreachable checks, and documented commands.
3. Extract and validate runnable manuscript examples with appropriate context, without blindly executing arbitrary code.
4. Record meaningful coverage gaps and prioritize the integrated project, numerical edge cases and the six prior fixes.
5. Run the agreed suite on the final exact revision and supported environments.

## Section mapping

Links identify the associated files; they do not claim substantive test coverage.

| Section | Manuscript | Same-numbered implementation | Check |
|---|---|---|---|
| 1.1 | [manuscript](../chapter-01/1.01-why-mathematical-foundations-matter-in-finance.md) | [lab](../chapter-01/code/section_1_01.py) | [check](../chapter-01/code/check_section_1_01.py) |
| 1.2 | [manuscript](../chapter-01/1.02-mathematical-objects-and-number-systems.md) | [lab](../chapter-01/code/section_1_02.py) | [check](../chapter-01/code/check_section_1_02.py) |
| 1.3 | [manuscript](../chapter-01/1.03-variables-constants-and-parameters.md) | [lab](../chapter-01/code/section_1_03.py) | [check](../chapter-01/code/check_section_1_03.py) |
| 1.4 | [manuscript](../chapter-01/1.04-sets-intervals-and-financial-domains.md) | [lab](../chapter-01/code/section_1_04.py) | [check](../chapter-01/code/check_section_1_04.py) |
| 1.5 | [manuscript](../chapter-01/1.05-mathematical-notation-and-indexed-quantities.md) | [lab](../chapter-01/code/section_1_05.py) | [check](../chapter-01/code/check_section_1_05.py) |
| 1.6 | [manuscript](../chapter-01/1.06-expressions-equations-and-identities.md) | [lab](../chapter-01/code/section_1_06.py) | [check](../chapter-01/code/check_section_1_06.py) |
| 1.7 | [manuscript](../chapter-01/1.07-inequalities-and-financial-constraints.md) | [lab](../chapter-01/code/section_1_07.py) | [check](../chapter-01/code/check_section_1_07.py) |
| 1.8 | [manuscript](../chapter-01/1.08-logic-assumptions-and-implications.md) | [lab](../chapter-01/code/section_1_08.py) | [check](../chapter-01/code/check_section_1_08.py) |
| 1.9 | [manuscript](../chapter-01/1.09-definitions-propositions-and-counterexamples.md) | [lab](../chapter-01/code/section_1_09.py) | [check](../chapter-01/code/check_section_1_09.py) |
| 1.10 | [manuscript](../chapter-01/1.10-units-dimensions-and-financial-conventions.md) | [lab](../chapter-01/code/section_1_10.py) | [check](../chapter-01/code/check_section_1_10.py) |
| 1.11 | [manuscript](../chapter-01/1.11-translating-financial-questions-into-mathematics.md) | [lab](../chapter-01/code/section_1_11.py) | [check](../chapter-01/code/check_section_1_11.py) |
| 1.12 | [manuscript](../chapter-01/1.12-translating-mathematical-expressions-into-python.md) | [lab](../chapter-01/code/section_1_12.py) | [check](../chapter-01/code/check_section_1_12.py) |
| 1.13 | [manuscript](../chapter-01/1.13-checking-mathematical-and-computational-results.md) | [lab](../chapter-01/code/section_1_13.py) | [check](../chapter-01/code/check_section_1_13.py) |
| 1.14 | [manuscript](../chapter-01/1.14-chapter-project-financial-formula-validation-toolkit.md) | [lab](../chapter-01/code/section_1_14.py) | [check](../chapter-01/code/check_section_1_14.py) |
| 1.15 | [manuscript](../chapter-01/1.15-exercises-and-applied-problems.md) | [lab](../chapter-01/code/section_1_15.py) | [check](../chapter-01/code/check_section_1_15.py) |
| 2.1 | [manuscript](../chapter-02/2.01-algebraic-expressions-and-equivalent-forms.md) | [lab](../chapter-02/code/section_2_01.py) | [check](../chapter-02/code/check_section_2_01.py) |
| 2.2 | [manuscript](../chapter-02/2.02-linear-equations-and-rearrangement.md) | [lab](../chapter-02/code/section_2_02.py) | [check](../chapter-02/code/check_section_2_02.py) |
| 2.3 | [manuscript](../chapter-02/2.03-fractions-and-rational-equations.md) | [lab](../chapter-02/code/section_2_03.py) | [check](../chapter-02/code/check_section_2_03.py) |
| 2.4 | [manuscript](../chapter-02/2.04-powers-roots-and-fractional-exponents.md) | [lab](../chapter-02/code/section_2_04.py) | [check](../chapter-02/code/check_section_2_04.py) |
| 2.5 | [manuscript](../chapter-02/2.05-quadratic-equations.md) | [lab](../chapter-02/code/section_2_05.py) | [check](../chapter-02/code/check_section_2_05.py) |
| 2.6 | [manuscript](../chapter-02/2.06-inequalities-and-absolute-values.md) | [lab](../chapter-02/code/section_2_06.py) | [check](../chapter-02/code/check_section_2_06.py) |
| 2.7 | [manuscript](../chapter-02/2.07-simultaneous-equations.md) | [lab](../chapter-02/code/section_2_07.py) | [check](../chapter-02/code/check_section_2_07.py) |
| 2.8 | [manuscript](../chapter-02/2.08-scaling-and-algebraic-validation.md) | [lab](../chapter-02/code/section_2_08.py) | [check](../chapter-02/code/check_section_2_08.py) |
| 2.9 | [manuscript](../chapter-02/2.09-chapter-project-break-even-and-formula-rearrangement-analyzer.md) | [lab](../chapter-02/code/section_2_09.py) | [check](../chapter-02/code/check_section_2_09.py) |
| 2.10 | [manuscript](../chapter-02/2.10-exercises-and-applied-problems.md) | Reuses earlier code | [check](../chapter-02/code/check_section_2_10.py) |
| 3.1 | [manuscript](../chapter-03/3.01-inputs-outputs-domain-and-range.md) | [lab](../chapter-03/code/section_3_01.py) | [check](../chapter-03/code/check_section_3_01.py) |
| 3.2 | [manuscript](../chapter-03/3.02-graphs-and-financial-interpretation.md) | [lab](../chapter-03/code/section_3_02.py) | [check](../chapter-03/code/check_section_3_02.py) |
| 3.3 | [manuscript](../chapter-03/3.03-composition-of-functions.md) | [lab](../chapter-03/code/section_3_03.py) | [check](../chapter-03/code/check_section_3_03.py) |
| 3.4 | [manuscript](../chapter-03/3.04-inverse-functions.md) | [lab](../chapter-03/code/section_3_04.py) | [check](../chapter-03/code/check_section_3_04.py) |
| 3.5 | [manuscript](../chapter-03/3.05-piecewise-functions-and-thresholds.md) | [lab](../chapter-03/code/section_3_05.py) | [check](../chapter-03/code/check_section_3_05.py) |
| 3.6 | [manuscript](../chapter-03/3.06-monotonicity-and-bounds.md) | [lab](../chapter-03/code/section_3_06.py) | [check](../chapter-03/code/check_section_3_06.py) |
| 3.7 | [manuscript](../chapter-03/3.07-convexity-and-concavity-intuition.md) | [lab](../chapter-03/code/section_3_07.py) | [check](../chapter-03/code/check_section_3_07.py) |
| 3.8 | [manuscript](../chapter-03/3.08-function-specifications-and-validation.md) | [lab](../chapter-03/code/section_3_08.py) | [check](../chapter-03/code/check_section_3_08.py) |
| 3.9 | [manuscript](../chapter-03/3.09-chapter-project-financial-function-explorer.md) | [lab](../chapter-03/code/section_3_09.py) | [check](../chapter-03/code/check_section_3_09.py) |
| 3.10 | [manuscript](../chapter-03/3.10-exercises-and-applied-problems.md) | Reuses earlier code | [check](../chapter-03/code/check_section_3_10.py) |
| 4.1 | [manuscript](../chapter-04/4.01-exponential-growth-and-decay.md) | [lab](../chapter-04/code/section_4_01.py) | [check](../chapter-04/code/check_section_4_01.py) |
| 4.2 | [manuscript](../chapter-04/4.02-natural-exponential-and-logarithm.md) | [lab](../chapter-04/code/section_4_02.py) | [check](../chapter-04/code/check_section_4_02.py) |
| 4.3 | [manuscript](../chapter-04/4.03-logarithm-rules-and-their-domains.md) | [lab](../chapter-04/code/section_4_03.py) | [check](../chapter-04/code/check_section_4_03.py) |
| 4.4 | [manuscript](../chapter-04/4.04-discrete-and-continuous-compounding.md) | [lab](../chapter-04/code/section_4_04.py) | [check](../chapter-04/code/check_section_4_04.py) |
| 4.5 | [manuscript](../chapter-04/4.05-solving-for-time-and-growth-rate.md) | [lab](../chapter-04/code/section_4_05.py) | [check](../chapter-04/code/check_section_4_05.py) |
| 4.6 | [manuscript](../chapter-04/4.06-products-and-additive-log-changes.md) | [lab](../chapter-04/code/section_4_06.py) | [check](../chapter-04/code/check_section_4_06.py) |
| 4.7 | [manuscript](../chapter-04/4.07-stable-numerical-evaluation.md) | [lab](../chapter-04/code/section_4_07.py) | [check](../chapter-04/code/check_section_4_07.py) |
| 4.8 | [manuscript](../chapter-04/4.08-numerical-conditioning-and-model-limits.md) | [lab](../chapter-04/code/section_4_08.py) | [check](../chapter-04/code/check_section_4_08.py) |
| 4.9 | [manuscript](../chapter-04/4.09-growth-and-rate-conversion-explorer.md) | [lab](../chapter-04/code/section_4_09.py) | [check](../chapter-04/code/check_section_4_09.py) |
| 4.10 | [manuscript](../chapter-04/4.10-exercises-and-applied-problems.md) | [lab](../chapter-04/code/section_4_10.py) | [check](../chapter-04/code/check_section_4_10.py) |
| 5.1 | [manuscript](../chapter-05/5.01-sequences-and-time-indexing.md) | [lab](../chapter-05/code/section_5_01.py) | [check](../chapter-05/code/check_section_5_01.py) |
| 5.2 | [manuscript](../chapter-05/5.02-arithmetic-and-geometric-sequences.md) | [lab](../chapter-05/code/section_5_02.py) | [check](../chapter-05/code/check_section_5_02.py) |
| 5.3 | [manuscript](../chapter-05/5.03-first-order-balance-recurrences.md) | [lab](../chapter-05/code/section_5_03.py) | [check](../chapter-05/code/check_section_5_03.py) |
| 5.4 | [manuscript](../chapter-05/5.04-closed-forms-from-repeated-substitution.md) | [lab](../chapter-05/code/section_5_04.py) | [check](../chapter-05/code/check_section_5_04.py) |
| 5.5 | [manuscript](../chapter-05/5.05-fixed-points-and-equilibria.md) | [lab](../chapter-05/code/section_5_05.py) | [check](../chapter-05/code/check_section_5_05.py) |
| 5.6 | [manuscript](../chapter-05/5.06-convergence-and-stability.md) | [lab](../chapter-05/code/section_5_06.py) | [check](../chapter-05/code/check_section_5_06.py) |
| 5.7 | [manuscript](../chapter-05/5.07-variable-rates-and-payment-schedules.md) | [lab](../chapter-05/code/section_5_07.py) | [check](../chapter-05/code/check_section_5_07.py) |
| 5.8 | [manuscript](../chapter-05/5.08-withdrawal-and-depletion-boundaries.md) | [lab](../chapter-05/code/section_5_08.py) | [check](../chapter-05/code/check_section_5_08.py) |
| 5.9 | [manuscript](../chapter-05/5.09-contribution-and-withdrawal-recurrence-engine.md) | [lab](../chapter-05/code/section_5_09.py) | [check](../chapter-05/code/check_section_5_09.py) |
| 5.10 | [manuscript](../chapter-05/5.10-exercises-and-applied-problems.md) | [lab](../chapter-05/code/section_5_10.py) | [check](../chapter-05/code/check_section_5_10.py) |
| 6.1 | [manuscript](../chapter-06/6.01-summation-and-product-notation.md) | [lab](../chapter-06/code/section_6_01.py) | [check](../chapter-06/code/check_section_6_01.py) |
| 6.2 | [manuscript](../chapter-06/6.02-finite-geometric-sums.md) | [lab](../chapter-06/code/section_6_02.py) | [check](../chapter-06/code/check_section_6_02.py) |
| 6.3 | [manuscript](../chapter-06/6.03-infinite-geometric-series.md) | [lab](../chapter-06/code/section_6_03.py) | [check](../chapter-06/code/check_section_6_03.py) |
| 6.4 | [manuscript](../chapter-06/6.04-ordinary-annuities-and-annuities-due.md) | [lab](../chapter-06/code/section_6_04.py) | [check](../chapter-06/code/check_section_6_04.py) |
| 6.5 | [manuscript](../chapter-06/6.05-growing-payment-streams.md) | [lab](../chapter-06/code/section_6_05.py) | [check](../chapter-06/code/check_section_6_05.py) |
| 6.6 | [manuscript](../chapter-06/6.06-perpetuities-and-tail-conditions.md) | [lab](../chapter-06/code/section_6_06.py) | [check](../chapter-06/code/check_section_6_06.py) |
| 6.7 | [manuscript](../chapter-06/6.07-truncation-and-approximation-error.md) | [lab](../chapter-06/code/section_6_07.py) | [check](../chapter-06/code/check_section_6_07.py) |
| 6.8 | [manuscript](../chapter-06/6.08-zero-rates-and-independent-verification.md) | [lab](../chapter-06/code/section_6_08.py) | [check](../chapter-06/code/check_section_6_08.py) |
| 6.9 | [manuscript](../chapter-06/6.09-cash-flow-series-derivation-and-verification-engine.md) | [lab](../chapter-06/code/section_6_09.py) | [check](../chapter-06/code/check_section_6_09.py) |
| 6.10 | [manuscript](../chapter-06/6.10-exercises-and-applied-problems.md) | [lab](../chapter-06/code/section_6_10.py) | [check](../chapter-06/code/check_section_6_10.py) |
| 7.1 | [manuscript](../chapter-07/7.01-limits-and-approaching-a-point.md) | [lab](../chapter-07/code/section_7_01.py) | [check](../chapter-07/code/check_section_7_01.py) |
| 7.2 | [manuscript](../chapter-07/7.02-one-sided-limits.md) | [lab](../chapter-07/code/section_7_02.py) | [check](../chapter-07/code/check_section_7_02.py) |
| 7.3 | [manuscript](../chapter-07/7.03-continuity-and-types-of-discontinuity.md) | [lab](../chapter-07/code/section_7_03.py) | [check](../chapter-07/code/check_section_7_03.py) |
| 7.4 | [manuscript](../chapter-07/7.04-limits-at-infinity-and-asymptotes.md) | [lab](../chapter-07/code/section_7_04.py) | [check](../chapter-07/code/check_section_7_04.py) |
| 7.5 | [manuscript](../chapter-07/7.05-exponential-limits-and-continuous-compounding.md) | [lab](../chapter-07/code/section_7_05.py) | [check](../chapter-07/code/check_section_7_05.py) |
| 7.6 | [manuscript](../chapter-07/7.06-important-small-change-limits.md) | [lab](../chapter-07/code/section_7_06.py) | [check](../chapter-07/code/check_section_7_06.py) |
| 7.7 | [manuscript](../chapter-07/7.07-intermediate-values-and-root-existence.md) | [lab](../chapter-07/code/section_7_07.py) | [check](../chapter-07/code/check_section_7_07.py) |
| 7.8 | [manuscript](../chapter-07/7.08-numerical-investigation-versus-proof.md) | [lab](../chapter-07/code/section_7_08.py) | [check](../chapter-07/code/check_section_7_08.py) |
| 7.9 | [manuscript](../chapter-07/7.09-chapter-project-boundary-and-continuity-investigation-lab.md) | [lab](../chapter-07/code/section_7_09.py) | [check](../chapter-07/code/check_section_7_09.py) |
| 7.10 | [manuscript](../chapter-07/7.10-exercises-and-applied-problems.md) | [lab](../chapter-07/code/section_7_10.py) | [check](../chapter-07/code/check_section_7_10.py) |
| 8.1 | [manuscript](../chapter-08/8.01-the-derivative-as-a-limit.md) | [lab](../chapter-08/code/section_8_01.py) | [check](../chapter-08/code/check_section_8_01.py) |
| 8.2 | [manuscript](../chapter-08/8.02-power-sum-and-constant-rules.md) | [lab](../chapter-08/code/section_8_02.py) | [check](../chapter-08/code/check_section_8_02.py) |
| 8.3 | [manuscript](../chapter-08/8.03-product-and-quotient-rules.md) | [lab](../chapter-08/code/section_8_03.py) | [check](../chapter-08/code/check_section_8_03.py) |
| 8.4 | [manuscript](../chapter-08/8.04-the-chain-rule.md) | [lab](../chapter-08/code/section_8_04.py) | [check](../chapter-08/code/check_section_8_04.py) |
| 8.5 | [manuscript](../chapter-08/8.05-exponential-and-logarithmic-derivatives.md) | [lab](../chapter-08/code/section_8_05.py) | [check](../chapter-08/code/check_section_8_05.py) |
| 8.6 | [manuscript](../chapter-08/8.06-higher-derivatives-and-curvature.md) | [lab](../chapter-08/code/section_8_06.py) | [check](../chapter-08/code/check_section_8_06.py) |
| 8.7 | [manuscript](../chapter-08/8.07-implicit-differentiation.md) | [lab](../chapter-08/code/section_8_07.py) | [check](../chapter-08/code/check_section_8_07.py) |
| 8.8 | [manuscript](../chapter-08/8.08-numerical-derivatives-and-step-selection.md) | [lab](../chapter-08/code/section_8_08.py) | [check](../chapter-08/code/check_section_8_08.py) |
| 8.9 | [manuscript](../chapter-08/8.09-analytic-and-numerical-derivative-comparator.md) | [lab](../chapter-08/code/section_8_09.py) | [check](../chapter-08/code/check_section_8_09.py) |
| 8.10 | [manuscript](../chapter-08/8.10-exercises-and-applied-problems.md) | [lab](../chapter-08/code/section_8_10.py) | [check](../chapter-08/code/check_section_8_10.py) |
| 9.1 | [manuscript](../chapter-09/9.01-absolute-and-relative-sensitivity.md) | [lab](../chapter-09/code/section_9_01.py) | [check](../chapter-09/code/check_section_9_01.py) |
| 9.2 | [manuscript](../chapter-09/9.02-elasticity.md) | [lab](../chapter-09/code/section_9_02.py) | [check](../chapter-09/code/check_section_9_02.py) |
| 9.3 | [manuscript](../chapter-09/9.03-first-order-taylor-approximation.md) | [lab](../chapter-09/code/section_9_03.py) | [check](../chapter-09/code/check_section_9_03.py) |
| 9.4 | [manuscript](../chapter-09/9.04-second-order-taylor-approximation.md) | [lab](../chapter-09/code/section_9_04.py) | [check](../chapter-09/code/check_section_9_04.py) |
| 9.5 | [manuscript](../chapter-09/9.05-remainder-and-error-bounds.md) | [lab](../chapter-09/code/section_9_05.py) | [check](../chapter-09/code/check_section_9_05.py) |
| 9.6 | [manuscript](../chapter-09/9.06-discounted-value-sensitivity.md) | [lab](../chapter-09/code/section_9_06.py) | [check](../chapter-09/code/check_section_9_06.py) |
| 9.7 | [manuscript](../chapter-09/9.07-kinks-and-one-sided-sensitivities.md) | [lab](../chapter-09/code/section_9_07.py) | [check](../chapter-09/code/check_section_9_07.py) |
| 9.8 | [manuscript](../chapter-09/9.08-sensitivity-reports-and-scenario-revaluation.md) | [lab](../chapter-09/code/section_9_08.py) | [check](../chapter-09/code/check_section_9_08.py) |
| 9.9 | [manuscript](../chapter-09/9.09-valuation-sensitivity-and-approximation-report-project.md) | [lab](../chapter-09/code/section_9_09.py) | [check](../chapter-09/code/check_section_9_09.py) |
| 9.10 | [manuscript](../chapter-09/9.10-exercises-and-applied-problems.md) | [lab](../chapter-09/code/section_9_10.py) | [check](../chapter-09/code/check_section_9_10.py) |
| 10.1 | [manuscript](../chapter-10/10.01-accumulation-and-riemann-sums.md) | [lab](../chapter-10/code/section_10_01.py) | [check](../chapter-10/code/check_section_10_01.py) |
| 10.2 | [manuscript](../chapter-10/10.02-definite-and-indefinite-integrals.md) | [lab](../chapter-10/code/section_10_02.py) | [check](../chapter-10/code/check_section_10_02.py) |
| 10.3 | [manuscript](../chapter-10/10.03-fundamental-theorem-of-calculus.md) | [lab](../chapter-10/code/section_10_03.py) | [check](../chapter-10/code/check_section_10_03.py) |
| 10.4 | [manuscript](../chapter-10/10.04-substitution-and-integration-by-parts.md) | [lab](../chapter-10/code/section_10_04.py) | [check](../chapter-10/code/check_section_10_04.py) |
| 10.5 | [manuscript](../chapter-10/10.05-discounting-continuous-payment-streams.md) | [lab](../chapter-10/code/section_10_05.py) | [check](../chapter-10/code/check_section_10_05.py) |
| 10.6 | [manuscript](../chapter-10/10.06-improper-integrals-and-infinite-horizons.md) | [lab](../chapter-10/code/section_10_06.py) | [check](../chapter-10/code/check_section_10_06.py) |
| 10.7 | [manuscript](../chapter-10/10.07-numerical-quadrature.md) | [lab](../chapter-10/code/section_10_07.py) | [check](../chapter-10/code/check_section_10_07.py) |
| 10.8 | [manuscript](../chapter-10/10.08-discrete-versus-continuous-payments.md) | [lab](../chapter-10/code/section_10_08.py) | [check](../chapter-10/code/check_section_10_08.py) |
| 10.9 | [manuscript](../chapter-10/10.09-continuous-cash-flow-valuation-engine.md) | [lab](../chapter-10/code/section_10_09.py) | [check](../chapter-10/code/check_section_10_09.py) |
| 10.10 | [manuscript](../chapter-10/10.10-exercises-and-applied-problems.md) | [lab](../chapter-10/code/section_10_10.py) | [check](../chapter-10/code/check_section_10_10.py) |
| 11.1 | [manuscript](../chapter-11/11.01-vectors-components-and-labels.md) | [lab](../chapter-11/code/section_11_01.py) | [check](../chapter-11/code/check_section_11_01.py) |
| 11.2 | [manuscript](../chapter-11/11.02-vector-addition-and-scalar-multiplication.md) | [lab](../chapter-11/code/section_11_02.py) | [check](../chapter-11/code/check_section_11_02.py) |
| 11.3 | [manuscript](../chapter-11/11.03-inner-products-and-valuation.md) | [lab](../chapter-11/code/section_11_03.py) | [check](../chapter-11/code/check_section_11_03.py) |
| 11.4 | [manuscript](../chapter-11/11.04-norms-and-distances.md) | [lab](../chapter-11/code/section_11_04.py) | [check](../chapter-11/code/check_section_11_04.py) |
| 11.5 | [manuscript](../chapter-11/11.05-orthogonality-and-angles.md) | [lab](../chapter-11/code/section_11_05.py) | [check](../chapter-11/code/check_section_11_05.py) |
| 11.6 | [manuscript](../chapter-11/11.06-projection-onto-a-direction.md) | [lab](../chapter-11/code/section_11_06.py) | [check](../chapter-11/code/check_section_11_06.py) |
| 11.7 | [manuscript](../chapter-11/11.07-portfolio-weights-and-exposure-constraints.md) | [lab](../chapter-11/code/section_11_07.py) | [check](../chapter-11/code/check_section_11_07.py) |
| 11.8 | [manuscript](../chapter-11/11.08-shape-broadcasting-and-alignment-checks.md) | [lab](../chapter-11/code/section_11_08.py) | [check](../chapter-11/code/check_section_11_08.py) |
| 11.9 | [manuscript](../chapter-11/11.09-chapter-project-vectorized-portfolio-exposure-calculator.md) | [lab](../chapter-11/code/section_11_09.py) | [check](../chapter-11/code/check_section_11_09.py) |
| 11.10 | [manuscript](../chapter-11/11.10-exercises-and-applied-problems.md) | [lab](../chapter-11/code/section_11_10.py) | [check](../chapter-11/code/check_section_11_10.py) |
| 12.1 | [manuscript](../chapter-12/12.01-matrices-and-dimensions.md) | [lab](../chapter-12/code/section_12_01.py) | [check](../chapter-12/code/check_section_12_01.py) |
| 12.2 | [manuscript](../chapter-12/12.02-matrix-multiplication-and-transformations.md) | [lab](../chapter-12/code/section_12_02.py) | [check](../chapter-12/code/check_section_12_02.py) |
| 12.3 | [manuscript](../chapter-12/12.03-transpose-identity-and-diagonal-matrices.md) | [lab](../chapter-12/code/section_12_03.py) | [check](../chapter-12/code/check_section_12_03.py) |
| 12.4 | [manuscript](../chapter-12/12.04-linear-systems-and-elimination.md) | [lab](../chapter-12/code/section_12_04.py) | [check](../chapter-12/code/check_section_12_04.py) |
| 12.5 | [manuscript](../chapter-12/12.05-rank-and-existence-of-solutions.md) | [lab](../chapter-12/code/section_12_05.py) | [check](../chapter-12/code/check_section_12_05.py) |
| 12.6 | [manuscript](../chapter-12/12.06-inverse-and-determinant.md) | [lab](../chapter-12/code/section_12_06.py) | [check](../chapter-12/code/check_section_12_06.py) |
| 12.7 | [manuscript](../chapter-12/12.07-condition-numbers-and-perturbations.md) | [lab](../chapter-12/code/section_12_07.py) | [check](../chapter-12/code/check_section_12_07.py) |
| 12.8 | [manuscript](../chapter-12/12.08-residuals-and-financial-interpretation.md) | [lab](../chapter-12/code/section_12_08.py) | [check](../chapter-12/code/check_section_12_08.py) |
| 12.9 | [manuscript](../chapter-12/12.09-chapter-project-exposure-matching-linear-solver.md) | [lab](../chapter-12/code/section_12_09.py) | [check](../chapter-12/code/check_section_12_09.py) |
| 12.10 | [manuscript](../chapter-12/12.10-exercises-and-applied-problems.md) | [lab](../chapter-12/code/section_12_10.py) | [check](../chapter-12/code/check_section_12_10.py) |
| 13.1 | [manuscript](../chapter-13/13.01-span-and-linear-combinations.md) | [lab](../chapter-13/code/section_13_01.py) | [check](../chapter-13/code/check_section_13_01.py) |
| 13.2 | [manuscript](../chapter-13/13.02-independence-bases-and-dimension.md) | [lab](../chapter-13/code/section_13_02.py) | [check](../chapter-13/code/check_section_13_02.py) |
| 13.3 | [manuscript](../chapter-13/13.03-column-space-and-null-space.md) | [lab](../chapter-13/code/section_13_03.py) | [check](../chapter-13/code/check_section_13_03.py) |
| 13.4 | [manuscript](../chapter-13/13.04-orthogonal-projection-onto-a-subspace.md) | [lab](../chapter-13/code/section_13_04.py) | [check](../chapter-13/code/check_section_13_04.py) |
| 13.5 | [manuscript](../chapter-13/13.05-least-squares-objectives.md) | [lab](../chapter-13/code/section_13_05.py) | [check](../chapter-13/code/check_section_13_05.py) |
| 13.6 | [manuscript](../chapter-13/13.06-qr-factorization-and-stable-solvers.md) | [lab](../chapter-13/code/section_13_06.py) | [check](../chapter-13/code/check_section_13_06.py) |
| 13.7 | [manuscript](../chapter-13/13.07-weighted-least-squares-and-units.md) | [lab](../chapter-13/code/section_13_07.py) | [check](../chapter-13/code/check_section_13_07.py) |
| 13.8 | [manuscript](../chapter-13/13.08-rank-deficiency-and-regularization.md) | [lab](../chapter-13/code/section_13_08.py) | [check](../chapter-13/code/check_section_13_08.py) |
| 13.9 | [manuscript](../chapter-13/13.09-chapter-project-least-squares-replication-analyzer.md) | [lab](../chapter-13/code/section_13_09.py) | [check](../chapter-13/code/check_section_13_09.py) |
| 13.10 | [manuscript](../chapter-13/13.10-exercises-and-applied-problems.md) | [lab](../chapter-13/code/section_13_10.py) | [check](../chapter-13/code/check_section_13_10.py) |
| 14.1 | [manuscript](../chapter-14/14.01-eigenvalues-and-eigenvectors.md) | [lab](../chapter-14/code/section_14_01.py) | [check](../chapter-14/code/check_section_14_01.py) |
| 14.2 | [manuscript](../chapter-14/14.02-symmetric-matrices-and-spectral-decomposition.md) | [lab](../chapter-14/code/section_14_02.py) | [check](../chapter-14/code/check_section_14_02.py) |
| 14.3 | [manuscript](../chapter-14/14.03-quadratic-forms.md) | [lab](../chapter-14/code/section_14_03.py) | [check](../chapter-14/code/check_section_14_03.py) |
| 14.4 | [manuscript](../chapter-14/14.04-positive-definite-and-semidefinite-matrices.md) | [lab](../chapter-14/code/section_14_04.py) | [check](../chapter-14/code/check_section_14_04.py) |
| 14.5 | [manuscript](../chapter-14/14.05-cholesky-factorization.md) | [lab](../chapter-14/code/section_14_05.py) | [check](../chapter-14/code/check_section_14_05.py) |
| 14.6 | [manuscript](../chapter-14/14.06-singular-value-decomposition.md) | [lab](../chapter-14/code/section_14_06.py) | [check](../chapter-14/code/check_section_14_06.py) |
| 14.7 | [manuscript](../chapter-14/14.07-low-rank-approximation.md) | [lab](../chapter-14/code/section_14_07.py) | [check](../chapter-14/code/check_section_14_07.py) |
| 14.8 | [manuscript](../chapter-14/14.08-decomposition-validation-and-interpretation.md) | [lab](../chapter-14/code/section_14_08.py) | [check](../chapter-14/code/check_section_14_08.py) |
| 14.9 | [manuscript](../chapter-14/14.09-chapter-project-quadratic-exposure-and-decomposition-lab.md) | [lab](../chapter-14/code/section_14_09.py) | [check](../chapter-14/code/check_section_14_09.py) |
| 14.10 | [manuscript](../chapter-14/14.10-exercises-and-applied-problems.md) | [lab](../chapter-14/code/section_14_10.py) | [check](../chapter-14/code/check_section_14_10.py) |
| 15.1 | [manuscript](../chapter-15/15.01-functions-of-several-variables.md) | [lab](../chapter-15/code/section_15_01.py) | [check](../chapter-15/code/check_section_15_01.py) |
| 15.2 | [manuscript](../chapter-15/15.02-partial-derivatives.md) | [lab](../chapter-15/code/section_15_02.py) | [check](../chapter-15/code/check_section_15_02.py) |
| 15.3 | [manuscript](../chapter-15/15.03-total-differentials-and-the-chain-rule.md) | [lab](../chapter-15/code/section_15_03.py) | [check](../chapter-15/code/check_section_15_03.py) |
| 15.4 | [manuscript](../chapter-15/15.04-gradients-and-directional-derivatives.md) | [lab](../chapter-15/code/section_15_04.py) | [check](../chapter-15/code/check_section_15_04.py) |
| 15.5 | [manuscript](../chapter-15/15.05-jacobians-of-vector-functions.md) | [lab](../chapter-15/code/section_15_05.py) | [check](../chapter-15/code/check_section_15_05.py) |
| 15.6 | [manuscript](../chapter-15/15.06-hessians-and-mixed-partials.md) | [lab](../chapter-15/code/section_15_06.py) | [check](../chapter-15/code/check_section_15_06.py) |
| 15.7 | [manuscript](../chapter-15/15.07-multivariable-taylor-approximation.md) | [lab](../chapter-15/code/section_15_07.py) | [check](../chapter-15/code/check_section_15_07.py) |
| 15.8 | [manuscript](../chapter-15/15.08-level-sets-and-sensitivity-interpretation.md) | [lab](../chapter-15/code/section_15_08.py) | [check](../chapter-15/code/check_section_15_08.py) |
| 15.9 | [manuscript](../chapter-15/15.09-chapter-project-multi-input-valuation-sensitivity-engine.md) | [lab](../chapter-15/code/section_15_09.py) | [check](../chapter-15/code/check_section_15_09.py) |
| 15.10 | [manuscript](../chapter-15/15.10-exercises-and-applied-problems.md) | [lab](../chapter-15/code/section_15_10.py) | [check](../chapter-15/code/check_section_15_10.py) |
| 16.1 | [manuscript](../chapter-16/16.01-objectives-and-decision-variables.md) | [lab](../chapter-16/code/section_16_01.py) | [check](../chapter-16/code/check_section_16_01.py) |
| 16.2 | [manuscript](../chapter-16/16.02-stationary-points-and-first-order-conditions.md) | [lab](../chapter-16/code/section_16_02.py) | [check](../chapter-16/code/check_section_16_02.py) |
| 16.3 | [manuscript](../chapter-16/16.03-second-order-classification.md) | [lab](../chapter-16/code/section_16_03.py) | [check](../chapter-16/code/check_section_16_03.py) |
| 16.4 | [manuscript](../chapter-16/16.04-convex-sets-and-convex-objectives.md) | [lab](../chapter-16/code/section_16_04.py) | [check](../chapter-16/code/check_section_16_04.py) |
| 16.5 | [manuscript](../chapter-16/16.05-gradient-descent.md) | [lab](../chapter-16/code/section_16_05.py) | [check](../chapter-16/code/check_section_16_05.py) |
| 16.6 | [manuscript](../chapter-16/16.06-newton-and-quasi-newton-methods.md) | [lab](../chapter-16/code/section_16_06.py) | [check](../chapter-16/code/check_section_16_06.py) |
| 16.7 | [manuscript](../chapter-16/16.07-scaling-initial-guesses-and-local-methods.md) | [lab](../chapter-16/code/section_16_07.py) | [check](../chapter-16/code/check_section_16_07.py) |
| 16.8 | [manuscript](../chapter-16/16.08-calibration-residuals-and-validation.md) | [lab](../chapter-16/code/section_16_08.py) | [check](../chapter-16/code/check_section_16_08.py) |
| 16.9 | [manuscript](../chapter-16/16.09-chapter-project-deterministic-calibration-optimizer.md) | [lab](../chapter-16/code/section_16_09.py) | [check](../chapter-16/code/check_section_16_09.py) |
| 16.10 | [manuscript](../chapter-16/16.10-exercises-and-applied-problems.md) | [lab](../chapter-16/code/section_16_10.py) | [check](../chapter-16/code/check_section_16_10.py) |
| 17.1 | [manuscript](../chapter-17/17.01-feasible-sets-and-constraint-types.md) | [lab](../chapter-17/code/section_17_01.py) | [check](../chapter-17/code/check_section_17_01.py) |
| 17.2 | [manuscript](../chapter-17/17.02-equality-constraints-and-lagrange-multipliers.md) | [lab](../chapter-17/code/section_17_02.py) | [check](../chapter-17/code/check_section_17_02.py) |
| 17.3 | [manuscript](../chapter-17/17.03-inequality-constraints-and-kkt-conditions.md) | [lab](../chapter-17/code/section_17_03.py) | [check](../chapter-17/code/check_section_17_03.py) |
| 17.4 | [manuscript](../chapter-17/17.04-active-constraints-and-complementarity.md) | [lab](../chapter-17/code/section_17_04.py) | [check](../chapter-17/code/check_section_17_04.py) |
| 17.5 | [manuscript](../chapter-17/17.05-linear-programming.md) | [lab](../chapter-17/code/section_17_05.py) | [check](../chapter-17/code/check_section_17_05.py) |
| 17.6 | [manuscript](../chapter-17/17.06-quadratic-programming.md) | [lab](../chapter-17/code/section_17_06.py) | [check](../chapter-17/code/check_section_17_06.py) |
| 17.7 | [manuscript](../chapter-17/17.07-financial-allocation-assumptions.md) | [lab](../chapter-17/code/section_17_07.py) | [check](../chapter-17/code/check_section_17_07.py) |
| 17.8 | [manuscript](../chapter-17/17.08-feasibility-and-independent-optimality-checks.md) | [lab](../chapter-17/code/section_17_08.py) | [check](../chapter-17/code/check_section_17_08.py) |
| 17.9 | [manuscript](../chapter-17/17.09-chapter-project-constrained-allocation-decision-engine.md) | [lab](../chapter-17/code/section_17_09.py) | [check](../chapter-17/code/check_section_17_09.py) |
| 17.10 | [manuscript](../chapter-17/17.10-exercises-and-applied-problems.md) | [lab](../chapter-17/code/section_17_10.py) | [check](../chapter-17/code/check_section_17_10.py) |
| 18.1 | [manuscript](../chapter-18/18.01-error-taxonomy.md) | [lab](../chapter-18/code/section_18_01.py) | [check](../chapter-18/code/check_section_18_01.py) |
| 18.2 | [manuscript](../chapter-18/18.02-floating-point-arithmetic-and-cancellation.md) | [lab](../chapter-18/code/section_18_02.py) | [check](../chapter-18/code/check_section_18_02.py) |
| 18.3 | [manuscript](../chapter-18/18.03-bracketing-and-bisection.md) | [lab](../chapter-18/code/section_18_03.py) | [check](../chapter-18/code/check_section_18_03.py) |
| 18.4 | [manuscript](../chapter-18/18.04-newton-and-safeguarded-root-finding.md) | [lab](../chapter-18/code/section_18_04.py) | [check](../chapter-18/code/check_section_18_04.py) |
| 18.5 | [manuscript](../chapter-18/18.05-multiple-roots-and-cash-flow-equations.md) | [lab](../chapter-18/code/section_18_05.py) | [check](../chapter-18/code/check_section_18_05.py) |
| 18.6 | [manuscript](../chapter-18/18.06-interpolation-and-extrapolation.md) | [lab](../chapter-18/code/section_18_06.py) | [check](../chapter-18/code/check_section_18_06.py) |
| 18.7 | [manuscript](../chapter-18/18.07-numerical-differentiation-and-integration.md) | [lab](../chapter-18/code/section_18_07.py) | [check](../chapter-18/code/check_section_18_07.py) |
| 18.8 | [manuscript](../chapter-18/18.08-stopping-rules-and-diagnostics.md) | [lab](../chapter-18/code/section_18_08.py) | [check](../chapter-18/code/check_section_18_08.py) |
| 18.9 | [manuscript](../chapter-18/18.09-chapter-project-financial-numerical-solver-and-diagnostics.md) | [lab](../chapter-18/code/section_18_09.py) | [check](../chapter-18/code/check_section_18_09.py) |
| 18.10 | [manuscript](../chapter-18/18.10-exercises-and-applied-problems.md) | [lab](../chapter-18/code/section_18_10.py) | [check](../chapter-18/code/check_section_18_10.py) |
| 19.1 | [manuscript](../chapter-19/19.01-differential-models-and-initial-conditions.md) | [lab](../chapter-19/code/section_19_01.py) | [check](../chapter-19/code/check_section_19_01.py) |
| 19.2 | [manuscript](../chapter-19/19.02-separable-equations.md) | [lab](../chapter-19/code/section_19_02.py) | [check](../chapter-19/code/check_section_19_02.py) |
| 19.3 | [manuscript](../chapter-19/19.03-linear-first-order-equations.md) | [lab](../chapter-19/code/section_19_03.py) | [check](../chapter-19/code/check_section_19_03.py) |
| 19.4 | [manuscript](../chapter-19/19.04-equilibria-and-local-stability.md) | [lab](../chapter-19/code/section_19_04.py) | [check](../chapter-19/code/check_section_19_04.py) |
| 19.5 | [manuscript](../chapter-19/19.05-euler-time-stepping.md) | [lab](../chapter-19/code/section_19_05.py) | [check](../chapter-19/code/check_section_19_05.py) |
| 19.6 | [manuscript](../chapter-19/19.06-runge-kutta-and-adaptive-solvers.md) | [lab](../chapter-19/code/section_19_06.py) | [check](../chapter-19/code/check_section_19_06.py) |
| 19.7 | [manuscript](../chapter-19/19.07-depletion-events-and-boundary-rules.md) | [lab](../chapter-19/code/section_19_07.py) | [check](../chapter-19/code/check_section_19_07.py) |
| 19.8 | [manuscript](../chapter-19/19.08-validation-and-discrete-time-comparison.md) | [lab](../chapter-19/code/section_19_08.py) | [check](../chapter-19/code/check_section_19_08.py) |
| 19.9 | [manuscript](../chapter-19/19.09-chapter-project-continuous-account-growth-and-depletion-simulator.md) | [lab](../chapter-19/code/section_19_09.py) | [check](../chapter-19/code/check_section_19_09.py) |
| 19.10 | [manuscript](../chapter-19/19.10-exercises-and-applied-problems.md) | [lab](../chapter-19/code/section_19_10.py) | [check](../chapter-19/code/check_section_19_10.py) |
| 20.1 | [manuscript](../chapter-20/20.01-model-validation-and-software-verification.md) | [lab](../chapter-20/code/section_20_01.py) | [check](../chapter-20/code/check_section_20_01.py) |
| 20.2 | [manuscript](../chapter-20/20.02-known-value-and-analytic-benchmarks.md) | [lab](../chapter-20/code/section_20_02.py) | [check](../chapter-20/code/check_section_20_02.py) |
| 20.3 | [manuscript](../chapter-20/20.03-financial-and-mathematical-invariants.md) | [lab](../chapter-20/code/section_20_03.py) | [check](../chapter-20/code/check_section_20_03.py) |
| 20.4 | [manuscript](../chapter-20/20.04-boundary-and-invalid-inputs.md) | [lab](../chapter-20/code/section_20_04.py) | [check](../chapter-20/code/check_section_20_04.py) |
| 20.5 | [manuscript](../chapter-20/20.05-floating-point-tolerances.md) | [lab](../chapter-20/code/section_20_05.py) | [check](../chapter-20/code/check_section_20_05.py) |
| 20.6 | [manuscript](../chapter-20/20.06-property-and-metamorphic-checks.md) | [lab](../chapter-20/code/section_20_06.py) | [check](../chapter-20/code/check_section_20_06.py) |
| 20.7 | [manuscript](../chapter-20/20.07-reproducibility-and-evidence.md) | [lab](../chapter-20/code/section_20_07.py) | [check](../chapter-20/code/check_section_20_07.py) |
| 20.8 | [manuscript](../chapter-20/20.08-review-findings-and-release-gates.md) | [lab](../chapter-20/code/section_20_08.py) | [check](../chapter-20/code/check_section_20_08.py) |
| 20.9 | [manuscript](../chapter-20/20.09-chapter-project-mathematical-model-validation-dossier.md) | [lab](../chapter-20/code/section_20_09.py) | [check](../chapter-20/code/check_section_20_09.py) |
| 20.10 | [manuscript](../chapter-20/20.10-exercises-and-applied-problems.md) | Reuses earlier code | [check](../chapter-20/code/check_section_20_10.py) |
| 21.1 | [manuscript](../chapter-21/21.01-capstone-requirements-and-assumptions.md) | [lab](../chapter-21/code/section_21_01.py) | [check](../chapter-21/code/check_section_21_01.py) |
| 21.2 | [manuscript](../chapter-21/21.02-architecture-and-module-interfaces.md) | [lab](../chapter-21/code/section_21_02.py) | [check](../chapter-21/code/check_section_21_02.py) |
| 21.3 | [manuscript](../chapter-21/21.03-cash-flow-and-rate-module.md) | [lab](../chapter-21/code/section_21_03.py) | [check](../chapter-21/code/check_section_21_03.py) |
| 21.4 | [manuscript](../chapter-21/21.04-sensitivity-and-approximation-module.md) | [lab](../chapter-21/code/section_21_04.py) | [check](../chapter-21/code/check_section_21_04.py) |
| 21.5 | [manuscript](../chapter-21/21.05-linear-algebra-and-replication-module.md) | [lab](../chapter-21/code/section_21_05.py) | [check](../chapter-21/code/check_section_21_05.py) |
| 21.6 | [manuscript](../chapter-21/21.06-optimization-and-feasibility-module.md) | [lab](../chapter-21/code/section_21_06.py) | [check](../chapter-21/code/check_section_21_06.py) |
| 21.7 | [manuscript](../chapter-21/21.07-continuous-time-module-and-scenario-report.md) | [lab](../chapter-21/code/section_21_07.py) | [check](../chapter-21/code/check_section_21_07.py) |
| 21.8 | [manuscript](../chapter-21/21.08-testing-documentation-and-transition-to-book-03.md) | [lab](../chapter-21/code/section_21_08.py) | [check](../chapter-21/code/check_section_21_08.py) |
| 21.9 | [manuscript](../chapter-21/21.09-chapter-project-financial-mathematics-foundations-toolkit.md) | [lab](../chapter-21/code/section_21_09.py) | [check](../chapter-21/code/check_section_21_09.py) |
| 21.10 | [manuscript](../chapter-21/21.10-exercises-and-applied-problems.md) | Reuses earlier code | [check](../chapter-21/code/check_section_21_10.py) |
