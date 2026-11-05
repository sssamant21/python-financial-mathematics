# Section 9.16 — Project contract review and pending probes

## Prerequisites and evidence flow

The only executable prerequisite is a Python interpreter with the standard library. Save the sole Python listing as tvm_engine.py before running or compiling. The frozen dataclass is self-contained; no Section 9.15 import is required. No network, credentials, external data or optional CSV file is needed for the demonstration. Rates are annual decimals, times are nonnegative years, nominal frequency is a positive integer, and discrete factors must be positive. Continuous quotes use separate functions. Fractional years are a model extension rather than a credit calendar.

The two POSIX-compatible commands are script execution and compileall. The PowerShell evidence recipe additionally displays Python version, redirects the transcript and reads it back; PowerShell itself is not validated here. A transcript must not be parsed wholesale as JSON. The prepared runner captures stdout JSON separately from stderr tests and saves a separate report from a source pipeline call. It has not run.

| Source acceptance gate / existing method | Static alignment and pending source verification |
|---|---|
| 01 FV/PV inverse | Same Convention and unrounded intermediate; verify 1000 recovery within stated floating tolerance |
| 02 Effective annual | Monthly nominal quote maps to (201/200)^12−1; independent rational oracle ready |
| 03 Continuous inverse | Separate continuous API and same quote/horizon; roundtrip pending |
| 04 Rate solver | Two-year 1000→1210 fixture implies 10%; check range and nearby-balance candidates too |
| 05 Time solver | Same fixture implies two years; check direction and zero-time-underflow candidates too |
| 06 Break-even NPV | Cost included exactly once, two audit rows; source tolerance pending |
| 07 CSV/JSON | Exact header and two events; report must preserve count and serialize finite numbers; strict row-shape candidates remain |
| 08 Negative rate | Positive factor .9 gives 81 after two years; source pending |
| 09 Zero rate | Constant valuation, nonunique equal-balance inverse; unequal-balance unreachable probe also prepared |
| 10 Invalid inputs | Existing cases cover selected bad rate/frequency/time/sign/CSV; not exhaustive domain coverage |
| 11 Same-date netting | Three rows, zero modeled NPV; supplemental audit-field inspection prepared |
| 12 Initial-cost policy | Receipt-only schedule must yield 100 PV with no implicit subtraction; pending |

## Open candidate issues; no runtime failures claimed

These are source-inspection candidates with executable probes prepared in review.py. No manuscript patch is published before reproduction and corrected rerun.

| Candidate | Static evidence and proposed probe | Disposition |
|---|---|---|
| C916-01 — F46 recurrence | real converts value to float before checking for nonzero loss. Probe Fraction(1,10**400) as amount, rate and horizon. Unlike the reviewed combined module, no original-value guard is present. | OPEN, reproduction pending |
| C916-02 — F48 recurrence | solve_rate divides by frequency*time without checking finite total periods or nonzero implied rate lost to zero. Probe (1,2,1e308,12) and adjacent represented balance over 1e308 years. | OPEN, reproduction pending |
| C916-03 — F49 recurrence | log_balance_ratio subtracts separate logs; solve_time rejects negative/nonfinite results but permits zero for nonzero growth. Probe adjacent large balances in both directions, opposed quote, nearby implied rates, and actual elapsed-time underflow with finite negative log growth. | OPEN, reproduction pending |
| C916-04 — row shape | CSV parser checks required field presence but does not inspect surplus fields. Probe year,amount followed by 0,-100,unexpected; verify the strict-schema promise before choosing a fix. | OPEN, reproduction pending |
| C916-05 — textual input loss | CSV converts strings directly with float before real/years validation. Nonzero 1e-400 amounts or negative −1e-400 years may lose original sign/value before validation. Probe both fields and define/reject unsupported numeric range. | OPEN, reproduction pending |

A nonfinite Convention.log_growth is another range boundary to assess during reproduction. scaled and effective_annual have later checks, so do not infer every path accepts it or assign an unexecuted failure. Log-space scaling intentionally avoids intermediate factor overflow when the final amount is small; preserve that design when fixing unrelated inverse routines. Calendar, input-volume and ledger precision remain declared extensions. Zero-valued cash flows are valid and must remain distinguishable from nonzero inputs lost during conversion.

Owner: next QA execution batch/manuscript maintainer. F46/F48/F49 remain resolved only in their previously recorded section scopes; this checkpoint does not reopen or erase prior passing evidence. Candidate IDs are local review records, not test methods or historical findings. F28 notebook/platform, F32 shared-input integration and all independent acceptance requirements remain open.
