# Chapter 3 Sections3.7–3.9 — 27 exercise answers

Reviewed 2026-10-29 at `00b7cd53ca165d1e7d684ce54d1ea09ea3f13701`. Supplemental answers/probes do not replace canonical source. Runtime checks and conceptual reviews are distinct.

## 3.7-E1

Annotated signed_difference(ending: Decimal, starting: Decimal)->Decimal returns ending−starting. Supplemental guards reject wrong/nonfinite inputs; positive5,zero0,negative−5 fixtures pass. This is a same-currency signed difference, not a cash-flow-adjusted return.

## 3.7-E2

Decimal NaN has the right representation but is not finite. The exact source future_value raises ValueError; annotations alone do not apply this guard.

## 3.7-E3

bool is an int subclass, so reject it explicitly in this book's count policy. Exact source future_value with True raises TypeError rather than treating it as one period.

## 3.7-E4

first_qualifying is annotated int|None and delegates to the exact fully validated source search. Period0 is a present result; use result is not None rather than if result. Fixtures check0 and absence.

## 3.7-E5

Amount=Decimal and PeriodicRate=Decimal are ordinary aliases, not distinct nominal types. Reversing them is not prevented by those aliases; use explicit names/contracts and validation or a deliberately distinct domain type.

## 3.7-E6

Wrong principal text raises TypeError and negative period count raises ValueError in the exact source function. No silent string parsing or negative-horizon reinterpretation is supplied.

## 3.7-E7

typed_balance has a required keyword-only timing: Literal["end","beginning"]. Runtime membership checking is still needed; Literal itself does not enforce values. The beginning fixture returns1155, and omitted timing raises TypeError.

## 3.7-E8

An ordinary Decimal annotation cannot encode currency, valuation time or effective/nominal rate-period meaning; it also does not enforce finiteness, domain, rounding policy or economic plausibility. These require contracts and checks.

## 3.7-E9

cast(Decimal,"100") informs a static checker but returns the original str object at runtime. Decimal("100") is a separate explicit parse/construction. The identity/type probe verifies no conversion.

## 3.8-E1

The supplemental signed_difference docstring states signed same-currency output, validated finite Decimal inputs, active-context arithmetic, no explicit cents and, when called investment gain, no intermediate cash flows, fees, taxes or currency conversion. The monetary difference alone is not a rate of return.

## 3.8-E2

typed_balance documents end: B*(1+r)+C and beginning: (B+C)*(1+r), matching period units, supported finite nonnegative balance/contribution, r>-1, shared currency and failures. The two timing fixtures give1150 and1155 from1000,5%,100.

## 3.8-E3

An in-memory copy of the exact documented function adds a zero-principal equality doctest. All six examples pass, including the new one. Canonical docstring/code remains unchanged; the verbose transcript is retained.

## 3.8-E4

Infinite principal raises ValueError from the exact source, agreeing with its Raises section for nonfinite Decimal inputs. The observed class is recorded separately from prose review.

## 3.8-E5

A5% number lacks its compounding/quotation period: effective annual, monthly or nominal annual quotations produce different factors. State effective versus nominal and match the period units; a percentage alone does not define the financial input.

## 3.8-E6

A cents policy must specify quantum, rounding mode, currency/scale, stage and whether target comparisons or later arithmetic use posted versus raw values. It changes the returned-value and numerical contract and requires new boundary tests, not merely a display format.

## 3.8-E7

Doctests check included examples; unsupported prose can remain invisible if no example exercises it. The prior lab-review drift demonstration retains this case. Contract review must trace each claim through signature, validation and arithmetic rather than infer all promises from green examples.

## 3.8-E8

The temporary definition changes horizon cap1000 to10, reconciles range/message/docstring text, checks acceptance at10 and rejection at11, and reruns unchanged valid docstring examples. A full policy revision would also update every related constant, contract table, upper-bound fixtures, integrations, source hashes and compatibility notes; the canonical lab stays at1000.

## 3.8-E9

An annotation communicates representation expectations to readers/static tools; a docstring communicates effective periodic meaning, units, valuation times, domains, numerical policy and exceptions. Neither by itself executes runtime validation or certifies financial applicability.

## 3.9-E1

At period0 P=2000, effective4% per period, n=3: 2000*(26/25)^3=2249.728 exactly. The exact ambient-context source future_value agrees with the Fraction oracle. Annual meaning requires those periods to be annual.

## 3.9-E2

Discount the independently known2249.728 by(1.04)^3; exact source present_value returns2000 at period0. This check does not rely only on output from a potentially wrong FV helper.

## 3.9-E3

For positive future amount100 and n1, rate−20% gives PV125, above the PV at−10% (100/.9). Both are supported by r>-1. More negative rates need not be economically suitable merely because the mathematical domain allows them.

## 3.9-E4

Exact source present_value rejects fractional period1.5 with TypeError and string amount"100" with TypeError. These are separate fixture calls; text parsing is outside this typed API.

## 3.9-E5

Proposed signed extension: finite signed Decimal cash flows, declared inflow/outflow direction at the chosen valuation timeline, r>-1 with matching units, same currency and stated ambient/fixed policy; preserve sign through linear discount/accumulation. Add negative/zero/reversal tests and document type/domain failures before implementation. Canonical functions remain finite nonnegative amounts.

## 3.9-E6

An effective annual rate cannot be copied directly as a monthly effective rate. Equivalent monthly r satisfies(1+r)^12=1+annual_effective; simply using12% monthly compounds12 times and differs from12% effective for one annual period. Fractional-power conversion needs a separately documented numerical policy.

## 3.9-E7

The deliberate wrong pair uses a10% two-period factor while the intended known case is5%. Its inverse recovers100 exactly, so a round trip passes; forward value121 fails the independent110.25 oracle. Shared inverse errors can therefore conceal a wrong financial convention.

## 3.9-E8

With local precision2 and Inexact trapped, the exact source valuation raises Inexact for the selected.05 calculation. After localcontext exits, the caller's precision, rounding, flags and traps match the before snapshot. This fixture illustrates context dependence, not all Decimal signal/range behavior.

## 3.9-E9

Formatting raw1.005 to two decimals produces text and leaves raw unchanged. Explicit HALF_UP cents produces1.01; doubling raw yields2.010 whereas doubling posted1.01 yields2.02. Quantization stage can therefore change later economics; no universal cents policy is inferred.

