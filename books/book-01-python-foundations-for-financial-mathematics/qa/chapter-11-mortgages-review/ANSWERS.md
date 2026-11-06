# Section 11.8 — Worked-answer and lab-step alignment

| Prompt | Review and evidence |
|---|---|
| 1. Principal | 300,000 − 60,000 = 240,000. Checked by the source purchase helper. |
| 2. Financed fees | 240,000 + 2,000 = 242,000; assumes the entire stated fee is financed. |
| 3. LTV | 240,000 / 300,000 = 80% using the specified property valuation. |
| 4. Payment count | 30 × 12 = 360, used in the independent present value sum. |
| 5. Periodic rate | The nominal annual rate is divided by 12, giving 0.005 per month. This is not a conversion from an effective annual rate. |
| 6. Payment | Divide 240,000 by the sum of the 360 discount factors. The source and demo give 1,438.92 to cents. |
| 7. First interest | 240,000 × 0.005 = 1,200. Derived from the fixture; the listing has no schedule function. |
| 8. First principal | The unrounded payment less 1,200 gives approximately 238.92. |
| 9. Tax allowance | 3,600 / 12 = 300. Isolated with zero other inputs. |
| 10. Insurance allowance | 1,200 / 12 = 100. Isolated with zero other inputs. |
| 11. Housing allowance | Add 400 to the unrounded payment for a displayed 1,838.92; HOA and mortgage insurance are not in this fixture. |
| 12. Fixed versus ARM | Conceptual: an ARM can reset under contract rules. No reset path is implemented or tested. |
| 13. Term trade-off | Positive-rate 15- and 30-year calculations confirm lower installment and higher total interest for the longer term. At zero rate, interest is zero for both terms. |
| 14. Scope | Conceptual: P&I excludes escrow and dues. The separate housing helper can add stated allowances; it is not an escrow accounting system. |

Save the listing as the named file and run its demo/suite and compilation; there are no data files or imported chapter modules. Rate and payment frequency are matched; the housing helper specifically returns a monthly allowance. LTV uses the supplied property valuation, not necessarily the purchase price. The checklist flags actual fees, escrow, ARM terms, balloons and prepayments as model applicability questions; no lender data or product was validated.
