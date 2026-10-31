# Section 7.9 — Eight scoped local answers

The original loader and explicit time arithmetic are separated from E7/E8 key/availability designs. QA answers correspond to supplied prompts without changing the manuscript. The valid fixture correction is stated rather than silently ignoring the intentional duplicate example.

## 7.9-E1

**Prompt:** Show that 09:30−05:00 and 14:30Z represent the same instant in the winter fixture.

**Scope:** EXPLICIT TIME ARITHMETIC

09:30 with offset−05:00 adds5hours to reach14:30UTC. Standard-library datetime.fromisoformat/astimezone independently yields2026-01-30T14:30:00+00:00;explicit pandas UTC parsing of that token and14:30Z identifies the same instant. Numeric offset describes this instant,not a geographic timezone identity.

## 7.9-E2

**Prompt:** Remove the offset from one timestamp and explain why rejection is preferable to an inferred source zone.

**Scope:** EXACT SOURCE REJECTION

Remove the offset from one timestamp in the otherwise valid corrected fixture. price_series raises ValueError at the explicit syntax boundary instead of assuming UTC or guessing a source zone. Naive wall time alone cannot identify a global instant;wrong zone inference could reorder observations,collapse keys or select the wrong interval.

## 7.9-E3

**Prompt:** Reverse source-row order and verify that the sorted output preserves every timestamp-price pairing.

**Scope:** EXACT SOURCE + PAIRING ORACLE

Use the documented valid demo fixture,changing its second15:00UTC encoding to16:30+01:00 before reversing rows. Original source returns identical sorted pairs14:30UTC->100,15:00UTC->101,15:30UTC->102 for both orders. The uncorrected original fixture intentionally has two encodings of15:00UTC and still rejects. Sorting complete records preserves pairing;sorting timestamps separately and attaching unsorted prices would not.

## 7.9-E4

**Prompt:** Compare inclusive and half-open selections from 15:00 through 15:30 UTC.

**Scope:** SOURCE RESULT + INTERVAL MECHANICS

For start15:00UTC,end15:30UTC,series.loc[start:end] includes both endpoint observations101,102(count2). Explicit >=start and <end selects only101(count1). Adjacent half-open windows avoid double-counting a boundary observation when that convention matches the reporting contract;no convention is universally correct.

## 7.9-E5

**Prompt:** Localize a winter New York wall time, convert to UTC, and verify a round trip.

**Scope:** SUPPLEMENTAL LOCALIZATION/ROUNDTRIP

Localize naive2026-01-30 09:30 to America/New_York with ambiguous/nonexistent bothraise,then tz_convert("UTC") to14:30UTC. Conversion back preserves the aware index and naive local clock fields. Localization supplies a source-zone interpretation;conversion preserves an already identified instant. This executes only the recorded host/provider,not universal platform acceptance.

## 7.9-E6

**Prompt:** Explain why a fixed −05:00 offset is not a complete year-round New York timezone policy.

**Scope:** HOST TIMEZONE MECHANICS + POLICY INTERPRETATION

On recorded pytz/tzdata2026.5,the fixture January NewYork wall time uses−05:00,while July30 09:30 uses−04:00 and becomes13:30UTC. Hard-coding−05:00 for that July wall time produces14:30UTC,a one-hour different instant. A regional zone carries date-dependent rules;an offset alone does not. Source geographic zone,rule data and ambiguity policies must be explicit;these examples do not establish all historical/future rules or venue calendars.

## 7.9-E7

**Prompt:** Propose a composite key for multi-asset observations sharing timestamps.

**Scope:** COMPOSITE-KEY DESIGN — NOT IMPLEMENTED

For one price per instrument per instant,propose(stable_instrument_id,event_time_utc) with explicit currency/unit/adjustment context. Several assets may legitimately share one timestamp. If multiple venues,revisions or events per instrument/instant are valid,extend grain with venue,event_id or revision identity and define authoritative selection/order policy separately. Normalize instants before key checks;never globally deduplicate timestamps or choose a duplicate winner solely by input order. No multi-asset loader or precedence algorithm was implemented.

## 7.9-E8

**Prompt:** List event/publication/ingestion timestamps needed before using these prices in a historical decision simulation.

**Scope:** INFORMATION-AVAILABILITY DESIGN — NOT EXECUTED SIMULATION

Retain original event/observation time,publication/release time,ingestion/receipt time and revision/version availability,plus exact historical decision cutoff. Require aware zones/offsets,source instrument/venue,price adjustment basis,calendar/session,quote-age policy and reproducible batch/version lineage. A point-in-time simulation must select only the version actually available by that decision time and apply event/valuation timing constraints;later revisions must not leak backward. Sorted UTC observations alone cannot establish availability,remove look-ahead bias or prove a complete expected schedule. No backtest or live feed was exercised.

Original reference methods additionally execute explicit DST nonexistent/ambiguous exception-name checks,invalid stamps/prices/schema,interval and ownership checks. These are eight existing methods,not additional unique methods. Results record pytz provider type and pytz/tzdata versions;installed versions do not prove every timezone or platform scenario. First-run evidence and expected source rejection traces retained;no unexpected failure or manuscript defect. F28/F32 and earlier findings/failures remain intact.
