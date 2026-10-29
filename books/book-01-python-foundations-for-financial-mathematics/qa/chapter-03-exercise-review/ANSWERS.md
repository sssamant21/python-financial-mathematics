# Chapter 3 — 20 chapter-wide exercise review records

Reviewed 2026-10-29 against `098e8583d49ea0525b6cbc7f000fd7f9bbe9dadd`. These are scope-limited technical reviews, not student grades or independent financial/model certification.

## Exercise 1 — Parameters and Arguments

Parameter names are principal, periodic_rate, periods; arguments are Decimal 1000, Decimal .05 and int 2. FV=1102.50 is at end of period2 in the input currency. Annual meaning requires annual effective rate and annual periods; currency is metadata, not encoded by Decimal.

## Exercise 2 — Printing Versus Returning

Print-only returns None; a numeric calculation should return its result and reporting should print at the boundary. Both returned value and stdout were checked.

## Exercise 3 — Keyword-Only Interface

future_value(Decimal("1000"), periodic_rate=Decimal("0.05"), periods=2) is valid. Signature star makes the latter arguments keyword-only; positional invocation raises TypeError before calculation.

## Exercise 4 — Missing Result

An incomplete positive-gain branch returns None at equality and loss. ending_amount-starting_amount gives zero and signed negative gain for the no-intermediate-cash-flow convention; fixtures verify both.

## Exercise 5 — Default and Explicit None

Omission uses default1; explicit0 stays0; explicitNone staysNone. The default substitutes only when omitted and does not enforce count types/domains.

## Exercise 6 — Mutable Default

A mutable default is allocated at definition and reused. Exact companion append_flow creates a fresh list for omitted/None, but an explicitly supplied list is still mutated and returned in the same identity. Both ownership behaviors were checked; signed flows are permitted by this helper, unlike project amount domains.

## Exercise 7 — Scope Failure

Assignment marks rate local; reading rate before binding raises UnboundLocalError despite a global rate. adjusted_rate(rate,spread) returns an explicit-input sum, assuming compatible rate conventions; the demonstration is not a complete financial guard.

## Exercise 8 — Type-Hint Limits

Annotations do not enforce runtime representations, finiteness, domains or unit compatibility. int does not exclude Boolean, negative or excessive periods; Decimal does not encode currency or quote convention. A deliberately unguarded annotated function accepts strings, NaN and bool to demonstrate the limitation; project guards are tested separately.

## Exercise 9 — Financial Docstring

Contract: discount one finite nonnegative Decimal period-n amount to period0, same currency/no sign reversal, finite effective matching-period rate>-1, whole n0..1000 excluding bool; validate even at zero horizon. No interim cash flows/taxes/fees/inflation or currency conversion. Fixed precision40, HALF_EVEN, Emin/Emax +/-999999, capitals1,clamp0, clear initial flags, traps InvalidOperation/DivisionByZero/Overflow, no explicit cents. TypeError for representation, ValueError for domains; Decimal exceptions and ArithmeticError guards may propagate. Rounding/cancellation/underflow and accuracy limits remain. Companion answer9 and module docstring together supply this contract; runtime docstring presence alone does not prove it.

## Exercise 10 — Local State and Mutation

Rebinding a local Decimal name leaves caller binding unchanged; append mutates a shared list object. Both behaviors are executed. Local scope does not imply independent ownership.

## Exercise 11 — Accumulation

Period0 principal2000, 4% effective per annual period, end of year3: 2000*(26/25)^3=2249.728 exactly, display2249.73. Exact Fraction oracle independently checks library output; no cents quantization is implied.

## Exercise 12 — Discounting

144 due at period2 discounted to0 at effective20% per period: 144/(6/5)^2=100. Multiplying yields207.36, valuing a period0 amount forward instead. Both outputs were checked as different timeline questions.

## Exercise 13 — Nominal Conversion

Nominal8% convertible quarterly: j/m=.08/4=.02 effective quarterly; (1.02)^4-1=.08243216 effective annually. Fraction oracles verify both relationships; this is not effective-annual-to-periodic conversion or regulatory APR.

## Exercise 14 — Composition

104.04 due after two quarters at nominal8% convertible quarterly: staged j/m=.02, discount factor1/1.02^2, amount*factor; wrapper converts then divides. Both agree with100 and with each other within absolute1e-30, justified only for this fixture and the fixed40-digit policy.

## Exercise 15 — Supported Negative Rate

1000 at -10% for one period yields900; discounting900 by.9 recovers1000. The positive discount factor1/.9 exceeds1. A supported negative effective rate can reduce forward amounts; project r>-1 remains required.

## Exercise 16 — Validation Matrix

Expected exceptions: string amount TypeError; NaN rate at zero horizon ValueError; bool horizon TypeError; horizon1001 ValueError. All four execute against exact project code; zero horizon does not bypass validation.

## Exercise 17 — Context Preservation

Caller precision6,ROUND_DOWN, enabled Inexact trap and set Inexact flag are snapshotted before the call. The fixed-policy result equals a reference call, and all caller settings/flags/traps remain unchanged afterward. This fixture does not exhaust every Decimal signal or numerical range.

## Exercise 18 — Detect a Defect

Known value PV(125,.25,1)=100. The temporary AST copy replaces only present_value division with multiplication; result156.25 fails the independent expected equality. Canonical temporary source and repository source remain unchanged and the correct module still returns100. Mutation evidence records both code hashes and outputs; matching round trips alone could miss mutually inverse defects.

## Exercise 19 — Reproduction Record

Reproduce exact input strings, amount/currency scale, nominal/effective quote, matching period units/count, timeline, data identity/version, code revision, full arithmetic context, runtime/dependency versions, quantization/display policy, expected value/tolerance and actual result. See reproduction.json for this batch. Matching output establishes neither correct financial assumptions nor source-data suitability.

## Exercise 20 — Final Integration Case

Nominal12% monthly means monthly .01; annual effective (1.01)^12-1=.126825030131969720661201; period12 FV1000*(1.01)^12=1126.825030131969720661201, display1126.83; recovered PV1000 within absolute1e-30. No intermediate flows/fees/tax/currency conversion. Exact Fraction oracles, zero horizon and frequency0 rejection are checked; exact source demonstration output is retained.

