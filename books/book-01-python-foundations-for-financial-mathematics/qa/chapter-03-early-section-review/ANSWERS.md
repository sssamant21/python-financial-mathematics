# Chapter 3 Sections3.4–3.6 — 25 exercise answers

Supplemental teaching answers, reviewed 2026-10-29. The [runner](review.py) distinguishes exact source calls from generated/temporary variants and small conceptual probes. Conceptual reasoning is reviewed separately from runtime counts.

## 3.4-E1

Replacing the calculation return with print displays1102.5000 for the chosen Decimal inputs and makes the assigned call result None. The review changes only a temporary function AST; canonical source is unchanged.

## 3.4-E2

net_cash_flow(inflow,outflow)=inflow-outflow returns signed same-currency flow. Fixtures10−5=5,5−5=0,5−10=−5 check all outcomes. Inputs are assumed validated compatible quantities; this teaching helper adds no hidden conversion.

## 3.4-E3

A string represents formatted text, not a numeric Decimal amount. Arithmetic consumers and type contracts change, even if displayed characters match. The test records both distinct types.

## 3.4-E4

The source first_target_period applied to [100,110,121] with target121 returns2, the final supplied index. Observations start at period0; None would mean no crossing in this finite list, not never reachable.

## 3.4-E5

Exact guarded source future_value rejects NaN principal and Infinity rate with ValueError before arithmetic. This augments source assertions; no unrestricted numerical-domain claim is made.

## 3.4-E6

A returned list may be the same mutable object held by the caller. Appending through the returned alias changes caller state; returning does not copy an object or promise purity.

## 3.4-E7

Proposed PV contract: return the period0 equivalent of one period-n amount, same currency, no sign reversal; finite nonnegative Decimal amount, finite effective matching-period rate>-1, integer n0..1000 excluding bool. Validate even at n0. No interim cash flows/fees/tax/inflation/currency conversion. For an ambient-policy version, Decimal context controls arithmetic; no explicit cents quantization. Raise TypeError for unsupported representations, ValueError for domains; Decimal signals can propagate. Production numerical-range and suitability decisions remain separate.

## 3.5-E1

The exact introductory future_value_one_period definition returns1050 for omitted periods or explicit1 and1000 for explicit0 at principal1000 and rate.05. Omission uses the default; zero does not request that default. The introductory function itself is not the guarded model.

## 3.5-E2

Keyword call future_value(periods=2, periodic_rate=Decimal("0.05"), present_value=Decimal("1000")) returns1102.50. Keyword order does not change binding; names must match the actual signature.

## 3.5-E3

A star makes an argument keyword-only, not optional. In the required-timing variant, omitting contribution_timing raises TypeError because its default is removed.

## 3.5-E4

required_timing_variant.py is a generated teaching copy: contribution_timing is required and all calls are updated with explicit timing. Defaults supplied through **options are merged before caller overrides, preserving deliberate invalid-value fixtures. All original lab assertions execute and pass in this variant; canonical code keeps its existing interface.

## 3.5-E5

At rate0, both (balance+contribution)*(1+rate) and balance*(1+rate)+contribution equal1100 from1000 plus100. Exact source advance_balance verifies both timings.

## 3.5-E6

The exact source rejects Infinity balance and rates exactly−1/below−1 with ValueError. These guards already exist; the requested extension is supplied as additional exercised fixtures, not an unnecessary rewrite.

## 3.5-E7

An explicitly passed empty list expresses caller ownership and must be mutated/returned under the source helper contract. Replacing it through items=items or [] selects a new list because empty is falsy. The counterexample leaves the original list empty and changes identity.

## 3.5-E8

Renaming a public parameter breaks callers supplying its former keyword, yielding TypeError unless an explicit compatibility policy exists. The teaching probe demonstrates an old principal keyword against a renamed amount parameter.

## 3.5-E9

One defensible educational default is zero contribution when the interface explicitly models an optional top-up; it is not a missing-data repair. Require a rate convention and contribution timing explicitly when ambiguity would change financial meaning. This batch demonstrates a required timing interface; real API choices must document intended users and compatibility.

## 3.6-E1

A parameter named principal shadows the module principal locally. Rebinding it changes the local result while module principal remains1000. This does not generalize to mutation of shared objects.

## 3.6-E2

Add supported−10% alongside3%/7%; reversing the evaluation order leaves each rate result unchanged. The−10% two-period result is810 from1000, independently hand-checkable as1000*.9*.9.

## 3.6-E3

A function may read a module name through normal lookup without global. Assignment creates a local binding unless global declares rebinding of the module name. The probe separately reads and explicitly updates a module rate.

## 3.6-E4

If a conditional assigns answer only when values is nonempty, returning answer for [] raises UnboundLocalError. Initialize a deliberate absence value or reject unsupported empty input according to an explicit contract; do not hide it behind a financial default.

## 3.6-E5

running_total creates total in each enclosing invocation; its inner add uses nonlocal to update that closure state. Two closures accumulate1→3 and10 independently; a later zero addition to the first leaves3.

## 3.6-E6

A returned closure retains access to captured enclosing bindings. The exact source make_projector captures−10% and still returns810 after the outer function has returned. Retained state is not necessarily immutable in other closure designs.

## 3.6-E7

explicit_rate(principal,rate) returns principal*(1+rate), supplying the rate rather than reading a market/global variable. At1000/.05 it returns1050. Its simple probe assumes validated compatible inputs; explicit arguments do not by themselves set numerical context.

## 3.6-E8

A local list parameter can alias the caller list; append mutates that object without global or nonlocal because it does not rebind the caller name. The observed list becomes[Decimal(1)].

## 3.6-E9

Explicit inputs leave ambient precision, rounding, traps/flags and external dependencies to be controlled separately. The same1/7 inputs at precision6 versus28 yield different values, with localcontext restoring settings. Reproducibility requires a declared complete policy; repeated output does not prove financial correctness.

