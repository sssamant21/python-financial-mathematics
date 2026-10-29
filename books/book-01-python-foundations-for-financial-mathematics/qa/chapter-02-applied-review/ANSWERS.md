# Chapter 2 Exercises 33–60 — answer review and supplements

Reviewed 2026-10-29 at `8ebbdb6859b8d23a1b62fd114c13a1f19de3370c`. Runtime predicates are separate from conceptual review. Functions are in [reference.py](reference.py), executions/oracles in [review.py](review.py).

## 2.13.33 — Investment amount

investment_valid first checks Decimal representation and finiteness, then value>0. Decimal 25000 passes; zero, negatives, NaN, None and text do not. External text conversion belongs to a separate acquisition/parser stage; this helper does not silently coerce it.

## 2.13.34 — Contribution

contribution_valid accepts finite Decimal zero and positive amounts, rejects negatives/nonfinite. Truthiness would reject a legitimate zero contribution and does not establish numeric type or finiteness.

## 2.13.35 — Financial period

period_valid requires isinstance(years,int), not isinstance(years,bool), and 0<years<=100. Tests include 20, both Boolean values, zero, endpoints 1/100, 101 and Decimal(20). The simplified analyzer requires a positive horizon even though it handles target attainment at period 0.

## 2.13.36 — Finite rates

Decimal .05 is finite; NaN, Infinity and -Infinity are not. Finiteness precedes supported-domain comparison. This predicate does not itself decide rate plausibility.

## 2.13.37 — Cross-field relationship

9%>4% passes the model-specific r>g rule; equality and r<g fail. The mathematical inequality does not establish realistic persistent growth, appropriate discounting, data quality, risk or economic conditions.

## 2.13.38 — Validation order

Presence → conversion/representation → finiteness → domain → relationships → financial plausibility. rate_error demonstrates the first four for typed inputs. Dependent methods require representation; comparisons require appropriate finite values; cross-field relationships require validated prerequisites. Plausibility requires evidence and judgment beyond a Boolean guard.

## 2.13.39 — Savings goal

The supplemental analyze with P=15000,C=6000,r=.04,T=75000,h=20 uses end-of-year contributions and first reaches the target at year 8, raw 75813.8933168701440000, displayed 75813.89. Shared inputs, period 0, horizon, target placement, stored results and report are explicit; closed-form Fraction checks establish the crossing and stopping balance independently.

## 2.13.40 — Multiple scenarios

For 2/4/6/8%, first years are 9/8/8/7 and displayed balances 76454.16/75813.89/83292.53/79244.18. All four evaluate and reach; no rejections. Scenario balances reset independently; reversed-order comparison gives the same result per rate. Both evaluated+rejected=total and reached+not_reached=evaluated are enforced.

## 2.13.41 — Cash-flow quality

quality records processed=4,missing=2,rejected=1; processed signs positive=2,negative=1,zero=1. It preserves an explicit reason for the NaN observation. Missing and rejected remain distinct; both classification levels reconcile. Known zero is processed rather than skipped.

## 2.13.42 — PV scenario grid

pv_grid resets discount totals per rate and stores period rows. End-of-year annual cash flows 10000/12000/15000 at effective annual 4/6/8% give displayed totals 34045.00/32708.21/31454.81. Exact Fraction oracles check each total. Rates require finite Decimal r>-1; invalid scenarios retain reasons. Annual cash-flow periods must match effective annual rate; no nominal-rate conversion is implied.

## 2.13.43 — Contribution timing

End-of-year update applies return then adds contribution; beginning-of-year update adds contribution before return. From 10000 with 2000 annual contributions at 5% for five years, displays are 23814.08 and 24366.64. Each beginning contribution receives one more period of growth, including the last contribution. Both terminal balances are checked against exact formulas.

## 2.13.44 — Precision layers

Internal 99999.996 is below 100000.00. HALF_UP cent quantization produces a business balance of 100000.00 and thus a different policy outcome. Formatting produces text 100,000.00 and must not redefine internal target status. The reference compares raw values; the quantized result is a clearly separate demonstration.

## 2.13.45 — Ties

analyze finds the minimum non-None first year and retains every scenario index attaining it. A 100 initial balance targeting 105 with 5/6/1% rates has two earliest scenarios at year 1 (5 and 6%). Reversed input order still retains both rates. Earliest target attainment ranks a deterministic assumption outcome, not risk-adjusted suitability or investment superiority.

## 2.13.46 — Off-by-one

Use range(1,maximum_years+1) to include the financial horizon; range(1,maximum_years) omits its final year. The check includes the expected last period and preserves the exclusion as a deliberate counterexample.

## 2.13.47 — State reset

Initialize balance=principal inside each accepted scenario iteration. Reusing terminal state mixes independent hypothetical assumptions. The applied multi-scenario model is tested in reverse order to establish identical per-rate output for these fixtures.

## 2.13.48 — Boolean horizon

True is an int subclass instance, so isinstance(True,int) alone accepts it. Add not isinstance(years,bool) before checking positive/supported bounds; period_valid rejects it.

## 2.13.49 — NaN order

rate_error checks Decimal representation, then is_finite, then r>-1. NaN is rejected as nonfinite without performing the domain comparison; correctness does not depend on comparison traps or incidental NaN behavior.

## 2.13.50 — Display comparison defect

Formatting 99999.996 to two decimals and parsing it back changes below-target status into attained. Keep raw balance>=target for the Chapter 2 policy; quantization before comparison must be separately authorized and documented as a business rule.

## 2.13.51 — Silent exclusions

Increment missing before continue and reconcile it with processed and rejected. quality([None,Decimal(0)]) records one missing and one processed zero. Silent exclusion loses data-quality and denominator information.

## 2.13.52 — Timing defect

For end-of-year contributions use balance=balance*(1+rate)+contribution. Starting 100 at 10% plus 10 yields 120; adding before return yields 121 and represents beginning-of-period timing. Match implementation order to documented recurrence.

## 2.13.53 — Decision placement

balance>=target is a financial attainment rule. Evaluating it before update tests the initial/beginning state; after return and contribution tests the ending state. A balance of 100 targeting 105 at 10% demonstrates False before growth and True afterward. Record which period label applies.

## 2.13.54 — Defaulting

Rejecting invalid input preserves the fact that the assumption is unavailable/unsupported. Replacing it with 5% supplies a new assumption. A permitted default policy must record original value, replacement, reason and policy version; it cannot be described merely as validation.

## 2.13.55 — Clamping

Replacing 30% with a 25% cap changes the supplied scenario; rejection preserves unsupported-input status. Clamping requires an explicit policy, original/effective values and disclosure. Silent clipping undermines reproduction and audit review.

## 2.13.56 — Scenario versus forecast

The list 3/5/7/9% consists of deterministic assumptions, not assigned probabilities or forecasts. Probabilistic interpretation needs a stated data basis, distribution or probability model, weights summing appropriately, calibration/estimation method, horizon, uncertainty and validation. Expected outcomes require that additional model; no such interpretation is inferred here.

## 2.13.57 — Plausibility

20%>19% passes r>g but may embed implausibly persistent growth or risk assumptions and a highly sensitive 1% spread. Review growth sustainability, nominal/real consistency, horizon, discount-rate rationale and sensitivity; mathematical admissibility is only one prerequisite.

## 2.13.58 — Explainable rejection

A rejection that names annual return as nonfinite identifies the failed field/rule. Store scenario identity, supplied assumption and reason for debugging, audit trails, governance, reconciliation and reproducibility. A bare rejection count cannot explain why outcomes disappeared.

## 2.13.59 — Integrated analyzer

review.py executes the exact companion input fence, then calls the new supplemental implementation. 2/4/6/8% first reach in years 16/14/12/10 at displayed balances 153019.28/161701.76/161585.54/151687.12. All four accepted scenarios reach; none fails in the published fixture. NaN is rejected as nonfinite, -110% as r<=-1. Counts: total6,evaluated4,rejected2,reached4,not_reached0. Earliest is year10 at 8%, no tie. Additional fixtures cover period0, horizon failure, final-year equality and ties; report states nominal amounts, effective annual constant returns, end-of-year contributions, no inflation/tax/fees and no recommendation.

## 2.13.60 — Model review checklist

See MODEL-REVIEW-CHECKLIST.md for seven required review categories with failure consequences and concrete evidence expectations. It is a review aid, not a completed independent production approval. The companion listed the categories but did not explicitly explain each failure mode; this supplement adds those explanations.

