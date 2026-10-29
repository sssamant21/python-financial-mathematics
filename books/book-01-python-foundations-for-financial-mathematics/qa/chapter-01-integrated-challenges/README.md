# V06 — Chapter 1 integrated challenges

Date: 2026-10-29. Reviewed source revision: `7ee99f60d5089510f860a0b6f695f971beb2eac6`.

**PASS (scoped): three challenge records, 67 checks passed, zero failed, including 17 fresh-process calculator cases.** These are supplemental implementations and finite test cases, not new manuscript reference methods or claims of exhaustive coverage. Do not add their counts to historical unique-workflow totals.

The existing companion supplied formula sketches, a calculation/rounding/presentation excerpt and an illustrative test table. This supplement supplies the executable extension, explicit input/validation stages and concrete expected/actual matrix. No original numerical implementation defect was identified in this batch.

| Challenge | Evidence | Scoped result |
|---|---|---|
| 1: extend calculator | [builder](build_extension.py), [assembled nine-option calculator](extended_calculator.py), [policies/helpers](reference.py), [assembly provenance](assembly.json) | Original six branch ASTs preserved; new PV, price reduction and basis-point operations execute through the menu |
| 2: staged refactor | `simple_interest` and `simple_interest_report` in [reference.py](reference.py) | Parse/validate, normalize, raw calculation, final rounding and presentation are explicit; raw result retained |
| 3: matrix | [readable matrix](MATRIX.md), [complete results and transcripts](results.json), [validator](validate.py) | Normal, zero, negative, large, fractional, invalid, nonfinite, rounding, mathematical and business boundaries recorded |

Run `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-01-integrated-challenges/validate.py` from the repository root. Standard library only; it rebuilds the extension and writes evidence. Run the generated calculator directly for interactive use. Tested with CPython 3.12.14 on Linux x86_64. No additional platform/runtime claim is made.

## Challenge 1 — contracts fixed before implementation

| Operation | Formula and units | Inputs/domain | Representation and rounding |
|---|---|---|---|
| Present value | PV = FV / (1+r)^n, USD; r is effective rate per period | Finite nonnegative receipt; percent strictly above -100 and at most 1000; whole periods 0..100; output at most 1e24 | Parse Decimal strings; percent divided by 100 once; local 40-digit arithmetic; cents HALF_UP only when displaying |
| Discount amount | Original price minus final price, USD | 0 <= final <= original; same currency/valuation basis; markup excluded | Raw difference retained; local 40-digit arithmetic; cents HALF_UP only when displaying |
| Basis points | Decimal rate = bp/10000; percentage points = bp/100 | Finite signed bp; fractional bp permitted | Decimal, local 40-digit arithmetic; no monetary rounding or conversion to money |

New numeric text is limited to 64 stripped characters, magnitude at most 1e18 and Decimal exponent at least -12 (including trailing fractional zeros). These are explicit teaching bounds, not universal finance restrictions. Whole-period text uses int directly, rejecting fractional text rather than truncating it. Negative effective rates are meaningful inside the selected PV domain. Positive growth factor is required even for zero periods. Discount here means a price reduction, not an implied yield or discount-rate quotation. No taxes, fees, intermediate cash flows, calendars or day-count assumptions are modeled.

The original six operations retain their existing behavior and error handling; the stricter new-operation contracts do not silently apply to them. The builder extracts the exact complete Section 1.12 program, inserts menu options 7–9 and checks all six original branch ASTs. The generated standalone file is a QA supplement, not a replacement manuscript fence. Existing handled errors print messages and exit zero; this is preserved and explicitly checked, not endorsed as a production CLI convention.

## Challenge 2 — staged refactor and benefits

The selected calculation is simple interest I=P*r*t. `simple_interest` acquires its external strings through explicit arguments, parses them as finite Decimal values, validates P>0, fractional t in [0,100], and signed percent magnitude <=1000, then normalizes the rate and calculates raw interest in a local 40-digit context. `simple_interest_report` applies the declared HALF_UP cents policy once and formats a USD label while returning raw interest separately. A caller presents the returned string with print; no input or print is hidden in the arithmetic.

Example: `simple_interest_report("100", "1.005", "1")` returns raw Decimal 1.005 and `Interest: USD 1.01`. A negative rate can produce negative interest; this helper does not promise a nonnegative ending balance. Separating the stages makes the formula readable, allows direct tests without stdin, isolates policy changes from arithmetic and makes the rounding stage visible to maintainers. Boundary checks and raw/display comparisons are in the matrix.

## Challenge 3 — oracle and limits

Each matrix row records operation, concrete inputs, expected behavior, actual result, reason and status. The normal PV case uses the known relation 100*(1.05)^2=110.25; a recurring-value case additionally compares against an exact Fraction oracle with an explicit relative bound of 1e-35. Half-cent examples use independently specified expected results. Caller-precision isolation is checked. Seventeen subprocess cases cover all nine menu operations plus selected errors and boundaries; they are included in the 67 checks, not counted again.

Forty significant digits and display policy do not prove exact cents for every supported input near a rounding boundary. Full error bounds, comprehensive branch/domain coverage, platform validation and independent review remain open. The original 1,160 manuscript Python fences are unchanged; the companion receives only an appended link. Chapter 1 remaining environment/platform/step review is next, followed by Chapter 2 formal V06 review. Broader V05/V06 acceptance is incomplete.
