# Chapter3 project and checklist mapping

Thirteen source contract rows,52 checklist review units and8 acceptance steps are separate review units, not tests or a completion percentage. Paragraph checklists are explicitly split into derived items.

## Project contract

| Area | Requirement | Disposition |
|---|---|---|
| Numeric representation | Decimal amounts and rates; controlled inputs constructed from strings | REVIEWED_SCOPED |
| Amount domain | Finite and nonnegative; no sign reversal | REVIEWED_SCOPED |
| Effective rate domain | Finite and greater than -1 | REVIEWED_SCOPED |
| Horizon | Integer 0..1000, excluding bool | REVIEWED_SCOPED |
| Frequency | Integer 1..366, excluding bool | REVIEWED_SCOPED |
| Timing | Principal at period 0; future amount at end of matching periods | REVIEWED_SCOPED |
| Rate convention | Effective periodic unless explicitly named nominal annual | REVIEWED_SCOPED |
| Cash flows | Single amount; no intervening contributions or withdrawals | REVIEWED_SCOPED |
| Currency | Input and output share currency; no conversion | REVIEWED_SCOPED |
| Numerical policy | Fresh fixed 40-digit half-even context per public calculation | REVIEWED_SCOPED |
| Validation | All relevant inputs checked, including at zero horizon | REVIEWED_SCOPED |
| Effects | No printing, external reads, input mutation, or caller-context changes in calculations | REVIEWED_SCOPED |
| Verification | Independent known values, boundaries, failures, composition, and isolation | REVIEWED_SCOPED |

## Definition, call, parameter and financial-contract checklists

| ID | Item | Review evidence / limitation |
|---|---|---|
| 3.2.41-01 | Meaningful name | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.41-02 | Valid syntax/indentation | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.41-03 | Coherent operation | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.41-04 | Understood assumptions | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.2.41-05 | Consistent representations | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.2.41-06 | Calculation/presentation separation | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.41-07 | Clear intended behavior | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.41-08 | Definition precedes use | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.41-09 | Invocation matches financial model | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.42-01 | Intended function | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.42-02 | Required represented inputs | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.2.42-03 | Rate/period assumptions | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.2.42-04 | Store returned values | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.42-05 | Print versus return | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.2.42-06 | Presentation formatting boundary | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.2.42-07 | Verify/reconcile results | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.43-01 | Does each parameter represent a clear financial concept? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.43-02 | Are names understandable without reverse-engineering the implementation? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.43-03 | Are rate conventions clear? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.3.43-04 | Are period units clear? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.3.43-05 | Are timing assumptions documented or explicit? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.3.43-06 | Is positional order natural? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.43-07 | Could similar numeric parameters easily be reversed? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.43-08 | Would selective keyword arguments improve readability? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.43-09 | Does the function require too many unrelated inputs? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.43-10 | Are expected representations understood? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.43-11 | Is validation performed at the appropriate boundary? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.43-12 | Could mutable arguments be modified unintentionally? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.43-13 | Does the interface expose rather than hide the financial model? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.44-01 | Am I calling the intended function? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.44-02 | Does each positional argument correspond to the intended parameter? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.44-03 | Are keyword names correct? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.44-04 | Is any parameter being bound more than once? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.44-05 | Are all required arguments supplied? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.44-06 | Are unexpected additional arguments present? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.44-07 | Are financial values represented appropriately? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.3.44-08 | Do rate and period units agree? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.3.44-09 | Does the timing convention match the intended model? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.3.44-10 | Are argument values within the supported financial domain? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.44-11 | Could a mutable argument be changed by the function? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.3.44-12 | Does the call communicate enough meaning for another reviewer to understand it? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.8.6-01 | Purpose: What quantity is computed? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.8.6-02 | Inputs: What does each parameter mean? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.8.6-03 | Units: Currency, amount scale, rate units, and period units? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.8.6-04 | Timing: When are principal, contributions, and valuation observed? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.8.6-05 | Rate convention: Effective periodic, nominal annual, or another convention? | Explicit single-amount same-currency/matching-period contract; currency/time metadata and real financial appropriateness are not enforced by Decimal types. |
| 3.8.6-06 | Domain: Which representations and values are supported? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.8.6-07 | Output: What does the returned quantity represent and when? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.8.6-08 | Numerical policy: Precision context, quantization boundaries, and display rules? | Keyword-only calls and TypeError/ValueError fixtures in chapter-wide/section exercise evidence; exact source suites pass. |
| 3.8.6-09 | Failure: Which inputs are rejected and how? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |
| 3.8.6-10 | State: Are inputs mutated or external state consulted? | Immutable project inputs/local fixed context; caller ownership and mutation demonstrations retained in section-exercise review. |
| 3.8.6-11 | Limits: Which real-world features are excluded? | Mapped against documented project domains/signatures/context and earlier prompt-aligned examples; not a new runtime test. |

## Acceptance steps

- 1. Confirm all three filenames and imports match. — PASS_SCOPED.
- 2. Run the full test module and inspect failures, not only the final line. — PASS_SCOPED.
- 3. Compare all four demo lines with the expected display. — PASS_SCOPED.
- 4. Check the docstrings and module assumptions against the implementation. — REVIEWED_SCOPED.
- 5. Verify that changing caller precision and traps does not change the project policy. — PASS_SCOPED.
- 6. In a temporary copy, replace present-value division with multiplication and confirm the known-value test fails. — PASS_SCOPED.
- 7. Restore the correct implementation and rerun the affected checks. — PASS_SCOPED.
- 8. Record Python version, source revision, and the policy used. — REVIEWED_SCOPED.

## Remaining extension queue

- 1. Add a documented signed-cash-flow function without weakening the current nonnegative amount contract. — PENDING.
- 2. Add a test for a finite positive growth factor that underflows under the fixed policy. — PENDING.
- 3. Define, then implement, explicit currency quantization at a chosen boundary. — PENDING.
- 4. Document an equivalent effective-annual-to-periodic conversion before adding fractional powers. — PENDING.
- 5. Add a scenario report that records rate convention and period count. — PENDING.
- 6. Plan how Chapter 5 could turn the module into a package without changing the public contracts. — PENDING.
