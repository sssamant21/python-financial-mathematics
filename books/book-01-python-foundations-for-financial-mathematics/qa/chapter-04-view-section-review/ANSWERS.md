# Sections4.7–4.9 —27 scoped exercise records

Reviewed2026-10-29. New interfaces are explicit QA supplements; design-only policies are not described as executed features.

## 4.7-E1

The positive-quantity loop appends each q>0 in iteration order; [12.5,0,3] yields[12.5,3], matching the comprehension without changing its selection rule.

## 4.7-E2

Original build_active_views(sample_positions()) returns active IDs BOND-A then ETF-B. CASH-RESERVE/0 is absent deliberately, not an unknown instrument.

## 4.7-E3

Explicit include_zero variant validates the original complete input, then returns fresh rows and a lookup for all nonnegative positions in source order. Both output contracts now include CASH-RESERVE. Empty returns([],{}); canonical active-only function is unchanged.

## 4.7-E4

Dictionary overwrite destroys earlier duplicate quantities; a later length comparison can reveal collision count but cannot reconstruct lost values. Reject duplicates while original records are still available.

## 4.7-E5

A and a remain distinct under current case-sensitive IDs. An uppercase-normalization policy must detect collisions before insertion, preserve original/effective labels and state how corrections are handled; normalization cannot justify silent aggregation.

## 4.7-E6

Extended tagged_active requires exactly instrument_id,quantity,tags, with tags a list of exact strings; tag order/duplicates are retained. First show shallow-copy aliasing, then copy the tag list into each selected output. Original fields retain canonical validation; invalid tags reject. This is new teaching code, not a relaxed canonical schema.

## 4.7-E7

multi_portfolio accepts unique unpadded portfolio IDs and positions under the original per-portfolio contract. Active lookup uses(portfolio_id,instrument_id), so A in P1 and P2 is allowed while duplicate A within P1 rejects. Validate all inputs before returning; no lots or global portfolio history are modeled.

## 4.7-E8

An invalid final negative-quantity record raises ValueError even though it would not qualify as positive. Selection is not a substitute for validating the entire supplied snapshot.

## 4.7-E9

An explicit validation loop makes seen-ID state and per-record errors reviewable before construction; a single dense comprehension obscures duplicate detection and can discard identity on dictionary insertion. Use comprehensions for the already-validated output transformation.

## 4.8-E1

For USD minimum0, ascending amount then ID gives ZERO,ALPHA,ZETA,BETA. The exercised teaching transformation uses a fully validated original report before applying the new ascending tie rule.

## 4.8-E2

reverse=True on(amount,ID) reverses both components, putting ZETA before ALPHA on equal values. Desired descending amount/ascending ID needs a suitable key or stable two-pass sort; source implements the complete tie rule.

## 4.8-E3

At threshold100, a row100 is selected and row99 is not. These are exact supplied Decimal values; no rounding modifies the inclusive comparison.

## 4.8-E4

Original ranking is invariant under baseline,reversed and rotated input orders for the tested equal-valued rows. Expected USD order is BETA,ALPHA,ZETA with threshold100/limit3.

## 4.8-E5

Extended account_report requires exact account_id,instrument_id,currency,market_value; uniqueness is(account,instrument), allowing the same instrument in different accounts. Validate all rows, select an explicitly requested currency, sort amount descending then account/instrument ascending, return fresh records. Tests cover same instrument across accounts and duplicate within one account. This variant has no FX or lot model and deliberately does not claim all original limit/threshold options.

## 4.8-E6

Proposed missing-value workflow: preserve source row identity and raw input, validate required amount/type/finiteness, place unavailable amounts in a separate rejection report with field/reason rather than zero. Distinguish field absence from invalid representation. Return selected rows plus auditable rejected IDs/counts; define completeness before downstream use. This task defines policy, not implemented persistence.

## 4.8-E7

report_with_metadata keeps caller snapshot_id, explicit currency/minimum/limit and fresh canonical ranked rows. Changing report rows does not change source. Snapshot label is supplied metadata, not validated global version uniqueness or a data refresh.

## 4.8-E8

Quantities have instrument-specific units;100 bond units and100 option contracts can imply very different price/multiplier exposure. Ranking unit counts does not rank economic value without compatible prices, multipliers, currencies and observation basis.

## 4.8-E9

An otherwise excluded EUR-like row relabeled unsupported GBP still raises ValueError for a USD report, even at limit0. All supplied rows must satisfy source currency/schema rules before selection.

## 4.9-E1

Add E-00 on the first date while retaining E-0; grouped output contains both in event-ID order. Same date does not permit overwrite or implicit netting.

## 4.9-E2

Event ID identifies an observation/event within declared schedule scope; payment date orders it on a calendar. Multiple IDs can share a date; an ID correction/version policy is separate.

## 4.9-E3

Changing the schedule label to EUR leaves every numeric amount unchanged. That is a different labeled fixture, not evidence of an FX conversion. Actual conversion needs rate/source/as-of and rounding contracts.

## 4.9-E4

Numeric event ID raises TypeError; an extra event field raises ValueError. Both are exact-source schema checks; no invalid row is quietly dropped.

## 4.9-E5

parse_payment_date is a separate exact-str boundary accepting ASCII YYYY-MM-DD only. It rejects padding/noncanonical width before date.fromisoformat validates the calendar. 2028-02-29 passes;2027-02-29 and padded strings reject. Wrong type raises TypeError. No timezone/timestamp parsing or business-calendar adjustment is implied.

## 4.9-E6

Proposed status model: planned/settled are versions of a logical event only under an explicit lifecycle/revision rule. Keep unique(event_id,revision) observations, status/effective timestamps and original lineage; define the active projection. Do not append duplicate event IDs to the current unique-ID schedule or count planned and settled as two actual payments.

## 4.9-E7

Proposed daily net view: validate complete single-currency/investor-perspective schedule; retain immutable source/event-ID lineage; group by exact date and sum signed amounts under an explicit local Decimal policy (for example precision40/HALF_EVEN with declared traps). State whether/when currency quantization occurs, overflow/error limits and reconciliation tolerance. Return daily totals plus original IDs; never replace source events. This is a design, not executed netting/valuation.

## 4.9-E8

Period0 needs valuation origin/date and cash-flow timing; subsequent indices need period units/length, equal-period assumption, currency/sign perspective, day-count/calendar basis if dated, rate/compounding convention and source versions. A bare list supplies none automatically.

## 4.9-E9

Reversing input events yields identical normalized date/ID schedule and grouped view under the complete tie rule. No intraday or settlement ordering is inferred beyond that declared date/ID presentation.

