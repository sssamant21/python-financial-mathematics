# Section 6.14 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling listings; explicit exact float64 bounded vector contracts and comparison tolerances. Caller establishes correct identities, units, interval interpretation and formula before numerical review. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.14-E1

Repeat the tiny-return experiment with one and ten entries, using a Decimal reference constructed from text.

**EXACT SOURCE + DECIMAL-TEXT/FRACTION ORACLES**. Repeat the source tiny-return experiment at lengths 1 and 10, each return 1e−17. Construct references from Decimal text at precision 100 and independently from (1+Fraction(1,10^17))^n−1. One entry gives 1e−17; ten give approximately 1.000000000000000045e−16. Original linked_return agrees with the reference converted to float at relative tolerance 1e−15 and zero absolute tolerance, while ordinary product(1+r)−1 gives zero in both cases. Retain full reference strings/fractions, actual results and comparison errors. This tests intended decimal inputs within binary64 approximation, not exact decimal output; source arrays stay unchanged.

## 6.14-E2

Add a test that shape mismatch fails even when NumPy could broadcast the values.

**EXACT SOURCE SHAPE REJECTION**. NumPy can broadcast shapes (2,) and (1,) to (2,), potentially hiding a missing comparison value. With actual [1,1] and reference [1], the unchanged agrees helper instead raises ValueError before np.isclose. Equal values after implicit broadcasting do not establish a correct equal-shape result contract. Expected traceback is retained; original test listing is unchanged.

## 6.14-E3

Compare spacing near 1 and near 1e16, explaining why epsilon is not a constant absolute precision everywhere.

**SPACING PROBES + EXACT BINARY ORACLE**. Near positive 1, float64 spacing is 2^−52≈2.220446049250313e−16. Near 10^16, local spacing is 2, so adding 1 can be lost. The runner checks both and the lost increment. Epsilon describes the gap above 1; it is not a constant absolute accuracy budget at every magnitude or an error bound for an entire algorithm. Subnormal and negative-spacing conventions would require separate interpretation.

## 6.14-E4

Design separate tolerance policies for a dimensionless rate and a same-currency P&L amount.

**TOLERANCE DESIGN + SUPPLEMENTAL SOURCE PREDICATES**. Define policies in output units and document reference provenance, supported magnitudes and error budget. An illustrative software rate check uses dimensionless atol1e−12/rtol1e−10 and rejects 1e−7 versus zero. A separate illustrative USD P&L check uses atol1e−6 USD/rtol0 and accepts a 0.5 micro-dollar discrepancy near100 USD. These numbers are explicit examples for contract mechanics, not approved business materiality or accounting-rounding limits; actual choices require justified precision/error and decision requirements. A relative tolerance alone cannot manage a near-zero reference. Keep currency conversion, display rounding, ledger rounding and materiality as separate policies; never adjust tolerances solely to make failures pass.

## 6.14-E5

Construct an example where printed values match but an explicit underlying-value test fails.

**DISPLAY/UNDERLYING-VALUE COUNTEREXAMPLE**. Actual100.004 and reference100.003 both print as 100.00 with two decimal places on this runtime. Their underlying difference is approximately0.001, so agrees with rtol0/atol1e−4 returns False. This deliberately chosen example separates presentation from the explicit numerical criterion. Equal printed cents do not prove equal storage, exact accounting values or acceptable application error.

## 6.14-E6

Compare an ordered cumulative sum and a separate reduction against math.fsum for a documented cancellation fixture.

**NUMPY SUM EXPERIMENT + FSUM/FRACTION REFERENCE**. Use exact supplied-float fixture [1e16]+[1.0]*100+[−1e16], length102. Ordered float64 cumsum finishes at0; the separate np.sum returns84 on this runtime; math.fsum returns100. Fraction arithmetic over the supplied float values independently gives exactly100, with absolute errors100,16,0 respectively. The retained observation records each route and environment; the NumPy reduction result is not asserted as a portable constant. Different grouping can retain different increments, while every cumulative intermediate still has a defined ordered meaning. fsum is a useful reference here, not an exact-decimal accounting engine or guaranteed universal substitute. This is a supplemental library experiment, not missing manuscript code.

## 6.14-E7

Explain why higher precision cannot fix a mislabeled instrument return.

**EXACT RATIONAL SEMANTIC COUNTEREXAMPLE**. For weights [0.6,0.3,0.1], correctly aligned returns [0.1,−0.05,0] give 0.045. Swapping the first two returns while leaving their intended instrument assignment wrong gives exactly0 under rational arithmetic. More precision only computes the wrong mapping more accurately; it cannot infer the correct instrument. Preserve labels, join keys, interval/currency/adjustment conventions and source evidence before numerical comparison. The runner verifies the exact arithmetic contrast, not an external-data ingestion system.

## 6.14-E8

State the domain and evidence required before replacing an existing linked-return implementation with this transformed version.

**REPLACEMENT CONTRACT REVIEW + EXACT SOURCE LIMIT PROBES**. Before substituting this method, establish that the previous question is one scalar linked return over consecutive compatible intervals, not a gross-factor path, endpoint-label record, monetary ledger or different performance measure. Explicitly reconcile the narrower exact float64 domain (1–10000 finite entries in [−0.5,0.5]), unsupported inputs, output/exception behavior, input ownership, overflow/underflow and reference-oriented tolerances. Test independent known answers, tiny/ordinary/mixed signs, zero, boundaries, long paths, cancellation, original acceptance/failure behavior and supported environments before migration; retain both initial failures and reruns. This source rejects a simple return1 rather than silently extending its domain. For100 returns of−0.5 it returns rounded scalar−1 although exact gross2^−100 is still positive; a scalar simple return cannot replace every use of retained gross factors. Those probes are executed, while replacement/migration, universal error/performance claims and financial acceptance remain unexecuted. No implementation is replaced in this batch.
