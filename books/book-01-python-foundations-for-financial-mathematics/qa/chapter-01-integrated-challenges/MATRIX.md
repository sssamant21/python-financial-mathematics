# Integrated challenge test matrix

See [results.json](results.json) for actual results and complete CLI transcripts. Predicates are not counts of exercises or reference methods.

| # | Category | Operation | Inputs | Expected | Status | Reason |
|---|---|---|---|---|---|---|
| 1 | normal | PV | ['110.25', '5', '2'] | Decimal('100') | PASS | 100 grows to 110.25 in two 5% periods |
| 2 | zero | PV | ['0', '5', '2'] | Decimal('0') | PASS | Zero receipt allowed |
| 3 | zero | PV | ['100', '5', '0'] | Decimal('100') | PASS | No discount periods |
| 4 | zero | PV | ['100', '0', '10'] | Decimal('100') | PASS | No discount rate |
| 5 | meaningful negative | PV | ['100', '-50', '1'] | Decimal('200') | PASS | Negative effective rate can imply PV > FV |
| 6 | large | PV | ['1000000000000000000', '0', '100'] | Decimal('1E+18') | PASS | Maximum input amount remains supported |
| 7 | fractional | PV | ['1.25', '25', '1'] | Decimal('1') | PASS | Fractional amount is allowed |
| 8 | normal | discount | ['100', '80'] | Decimal('20') | PASS | Discount means a price reduction, not PV discounting |
| 9 | zero | discount | ['0', '0'] | Decimal('0') | PASS | Zero prices are permitted |
| 10 | business boundary | discount | ['100', '100'] | Decimal('0') | PASS | Equal prices imply zero reduction |
| 11 | business boundary | discount | ['100', '100.01'] | '0 <= final <= original' | PASS | Markup excluded by this contract |
| 12 | business boundary | discount | ['100', '-0.01'] | '0 <= final <= original' | PASS | Negative final price excluded |
| 13 | fractional | discount | ['10.005', '9'] | Decimal('1.005') | PASS | Keep raw difference before final-only cents |
| 14 | normal | bps | ['25'] | (Decimal('0.0025'), Decimal('0.25')) | PASS | Rate and percentage-point units distinguished |
| 15 | meaningful negative | bps | ['-25'] | (Decimal('-0.0025'), Decimal('-0.25')) | PASS | Signed rate movement permitted |
| 16 | fractional | bps | ['0.5'] | (Decimal('0.00005'), Decimal('0.005')) | PASS | Fractional basis points supported |
| 17 | zero | bps | ['0'] | (Decimal('0'), Decimal('0')) | PASS | Zero movement permitted |
| 18 | invalid text | bps | ['abc'] | 'decimal numeric text' | PASS | Invalid Decimal conversion is handled |
| 19 | invalid text | bps | [''] | 'decimal numeric text' | PASS | Invalid Decimal conversion is handled |
| 20 | nonfinite | bps | ['NaN'] | 'must be finite' | PASS | Reject before comparisons/arithmetic |
| 21 | nonfinite | bps | ['sNaN'] | 'must be finite' | PASS | Reject before comparisons/arithmetic |
| 22 | nonfinite | bps | ['Infinity'] | 'must be finite' | PASS | Reject before comparisons/arithmetic |
| 23 | nonfinite | bps | ['-Infinity'] | 'must be finite' | PASS | Reject before comparisons/arithmetic |
| 24 | precision boundary | bps | ['.0000000000001'] | 'precision/magnitude' | PASS | More than 12 decimal places rejected |
| 25 | precision boundary | bps | ['1e19'] | 'precision/magnitude' | PASS | Above amount magnitude cap rejected |
| 26 | resource boundary | bps | ['11111111111111111111111111111111111111111111111111111111111111111'] | '64 characters' | PASS | Bound external text size |
| 27 | mathematical/business boundary | PV | ['100', '-100', '1'] | '(-100, 1000]' | PASS | Explicit selected PV domain |
| 28 | mathematical/business boundary | PV | ['100', '-100.01', '1'] | '(-100, 1000]' | PASS | Explicit selected PV domain |
| 29 | mathematical/business boundary | PV | ['100', '1000.01', '1'] | '(-100, 1000]' | PASS | Explicit selected PV domain |
| 30 | mathematical/business boundary | PV | ['-1', '5', '1'] | 'nonnegative' | PASS | Explicit selected PV domain |
| 31 | mathematical/business boundary | PV | ['100', '5', '-1'] | '0..100' | PASS | Explicit selected PV domain |
| 32 | mathematical/business boundary | PV | ['100', '5', '101'] | '0..100' | PASS | Explicit selected PV domain |
| 33 | mathematical/business boundary | PV | ['100', '5', '1.5'] | 'whole integer' | PASS | Explicit selected PV domain |
| 34 | mathematical/business boundary | PV | ['100', '5', '99999'] | '0..100' | PASS | Explicit selected PV domain |
| 35 | mathematical/business boundary | PV | ['100', '-99', '100'] | 'output bound' | PASS | Explicit selected PV domain |
| 36 | rate upper boundary | PV | ['1100', '1000', '1'] | Decimal('100') | PASS | Inclusive maximum supported effective percent |
| 37 | normal | simple | ['1000', '5', '2'] | (Decimal('100'), 'Interest: USD 100.00') | PASS | Separate raw interest from posted display |
| 38 | meaningful negative | simple | ['1000', '-5', '2'] | (Decimal('-100'), 'Interest: USD -100.00') | PASS | Signed interest allowed; no savings balance guarantee |
| 39 | fractional | simple | ['100', '5', '.5'] | (Decimal('2.5'), 'Interest: USD 2.50') | PASS | Fractional time allowed for simple interest |
| 40 | rounding boundary | simple | ['100', '1.005', '1'] | (Decimal('1.005'), 'Interest: USD 1.01') | PASS | Raw value retained through final rounding |
| 41 | business boundary | simple | ['0', '5', '1'] | 'Require principal' | PASS | Selected simple-interest contract enforced |
| 42 | business boundary | simple | ['100', '5', '-1'] | 'Require principal' | PASS | Selected simple-interest contract enforced |
| 43 | business boundary | simple | ['100', '1000.01', '1'] | 'Require principal' | PASS | Selected simple-interest contract enforced |
| 44 | business boundary | simple | ['100', '5', '100.01'] | 'Require principal' | PASS | Selected simple-interest contract enforced |
| 45 | rounding boundary | round | ['1.004'] | Decimal('1.00') | PASS | Declared ROUND_HALF_UP; cents only at output |
| 46 | rounding boundary | round | ['1.005'] | Decimal('1.01') | PASS | Declared ROUND_HALF_UP; cents only at output |
| 47 | rounding boundary | round | ['1.006'] | Decimal('1.01') | PASS | Declared ROUND_HALF_UP; cents only at output |
| 48 | rounding boundary | round | ['-1.005'] | Decimal('-1.01') | PASS | Declared ROUND_HALF_UP; cents only at output |
| 49 | independent oracle | PV | ['100', '7', '10'] | relative error <= 1e-35 against exact Fraction | PASS | Independent rational oracle, not the Decimal implementation |
| 50 | context isolation | PV | ['100', '7', '10', 'caller precision 6'] | 50.83492921347178641554053032334491849132 | PASS | Local 40-digit policy |
| 51 | CLI integration | original SI | ['1', '1000', '5', '2'] | Interest:       $100.00 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 52 | CLI integration | original FV | ['2', '1000', '5', '2', '1'] | Future Value:  $1,102.50 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 53 | CLI integration | original change | ['3', '100', '110'] | Percentage Change: 10.00% | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 54 | CLI integration | original trade | ['4', '100', '110', '2'] | Status: PROFIT | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 55 | CLI integration | original fee | ['5', '100', '1'] | Fee:                $1.00 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 56 | CLI integration | original reconciliation | ['6', '100', '100.01', '.01'] | Status: WITHIN TOLERANCE | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 57 | CLI integration | PV | ['7', '110.25', '5', '2'] | Present Value: USD 100.00 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 58 | CLI integration | PV negative rate | ['7', '100', '-50', '1'] | Present Value: USD 200.00 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 59 | CLI integration | PV invalid periods | ['7', '100', '5', '1.5'] | Invalid input: Periods must be whole integer text | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 60 | CLI integration | PV invalid factor | ['7', '100', '-100', '1'] | Invalid input: Effective rate percent | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 61 | CLI integration | discount rounding | ['8', '10.005', '9'] | Discount Amount: USD 1.01 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 62 | CLI integration | discount invalid markup | ['8', '100', '101'] | Invalid input: Price reduction | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 63 | CLI integration | bps | ['9', '25'] | Decimal rate: 0.0025 / Percentage points: 0.25 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 64 | CLI integration | bps negative | ['9', '-25'] | Decimal rate: -0.0025 | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 65 | CLI integration | bps nonfinite | ['9', 'NaN'] | Invalid input: Financial input must be finite | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 66 | CLI integration | bps invalid text | ['9', 'abc'] | Invalid input: Enter decimal numeric text | PASS | Fresh subprocess; original handled input errors retain exit code zero |
| 67 | CLI integration | invalid menu | ['10'] | Invalid calculator selection. | PASS | Fresh subprocess; original handled input errors retain exit code zero |
