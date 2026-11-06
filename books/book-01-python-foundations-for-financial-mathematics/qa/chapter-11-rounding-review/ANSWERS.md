# Section 11.12 — Worked answers and lab steps

| Prompt | Review and scope |
|---|---|
| 1. Float representation | 0.1 has no finite base-two expansion. The exact snippet prints False for exact comparison and True for the tolerance comparison. |
| 2. Stable formula | The denominator is −expm1(−n log1p(r)). Direct discount sums check ordinary and 10⁻¹² rate fixtures. |
| 3. Zero rate | 1,200 / 12 = 100. |
| 4. Display rounding | Conceptual: round for presentation unless the calculation policy expressly calls for earlier rounding. |
| 5. Cent rounding | Exact Decimal snippet gives 1.01. The ledger helper also verifies −1.005 gives −1.01. |
| 6. First interest | 10,000 × 0.005 = 50.00. |
| 7. Payment identity | Payment is interest plus principal, checked across the cent oracle rows. |
| 8. Balance identity | Closing is opening less principal, checked across the rows. |
| 9. Continuity | The next row opens at the preceding closing balance. |
| 10. Principal total | Sum of principal equals the booked cent opening. The answer now distinguishes booked from raw principal. |
| 11. Final adjustment | The model settles its residual with 443.11 rather than the regular 443.21. |
| 12. Exact maturity | Final balance is exactly zero cents. The optimized-mode probe separately verifies that malformed reconciliation raises an error. |
| 13. Rate convention | Conceptual: the periodic rate must match the modeled accrual interval; no day-count adapter is supplied. |
| 14. Real lender | Conceptual: verify the contract’s rounding and posting rules separately. |

Run the two teaching snippets separately, save the complete lab to its named file, run the demo and embedded tests, and compile that file. The stable and naive formulas operate on unrounded inputs. The cent schedule first books principal, then rounds the installment and interest under the stated policy. No third-party dependency, external file or earlier module is required.
