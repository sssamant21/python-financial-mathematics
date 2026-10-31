# Section 7.13 — Eight scoped local answers

Unchanged original observed-event bars are separate from supplemental asfreq mechanics and independent scalar OHLC/volume expectations. E7 multiple-events-per-timestamp ordering and E8 external calendar/feed completeness remain designs. Full demonstration output is compared against explicitly transcribed published-table expectations;conservation concerns supplied events only.

## 7.13-E1

**Prompt:** Verify the first bin's OHLC and volume by hand.

**Scope:** SOURCE + SCALAR OHLC/VOLUME

The first[14:00,14:30) bin contains prices100 and102 with event volumes10 and20. Chronological open100,high102,low100,close102 and volume10+20=30 follow directly. All supplied bins account for4events and total42volume units. Prices are not additive volume-like flows;the sum202 is not a bar close or portfolio value.

## 7.13-E2

**Prompt:** Explain why the 14:30 event belongs to the bin labeled 15:00.

**Scope:** EXACT SOURCE INTERVAL MEMBERSHIP

closed="left" includes14:30 in[14:30,15:00),not[14:00,14:30). label="right" names that bin15:00;its open/close is101 with event_count1. Output label and endpoint membership are separate settings;the label is not the actual timestamp of the close observation or proof of availability.

## 7.13-E3

**Prompt:** Remove the first two events and inspect the newly visible leading empty bin.

**Scope:** EXACT SOURCE HORIZON

Remove the first two events. The independent14:00..16:00 reporting horizon still yields4bins and counts[0,1,0,1]. Leading14:30-labeled bin has unknownOHLC/volume rather than disappearing or becoming observedzero. Explicit horizon reindexing is different from inferring the report span from supplied events alone.

## 7.13-E4

**Prompt:** Set all supplied volumes to zero and distinguish observed zero from the empty bin's NaN.

**Scope:** EXACT SOURCE MISSING/ZERO CONTRAST

Set all supplied event volumes to0. The three nonempty bins have known volume0;the empty third bin has volumeNaN,event_count0,has_observationsFalse. min_count=1 prevents an empty group from becoming observedzero. Unknown/no-supplied-event state does not by itself mean confirmed no trading.

## 7.13-E5

**Prompt:** Add an event exactly at reporting end and explain the rejection.

**Scope:** EXACT SOURCE REJECTION

Append an event exactly16:00UTC. The half-open horizon[start,end) rejects it instead of silently assigning it outside the requested report. The existing15:45 event remains in the last bin closing103. Extending the report horizon would be a different explicit request,not an automatic adjustment.

## 7.13-E6

**Prompt:** Contrast asfreq with the bar close for the first interval.

**Scope:** SUPPLEMENTAL GRID-SELECTION CONTRAST

asfreq("30min") selects the exact14:00 observation100 for its first grid point;the first aggregated bar closes102 from the14:29 event. The14:29 event is off the asfreq grid. Grid selection does not compute OHLC or establish that intervening prices were unchanged;no interpolation/fill is authorized.

## 7.13-E7

**Prompt:** Design a multiple-events-per-timestamp key and deterministic within-time ordering policy.

**Scope:** COMPOSITE EVENT-GRAIN DESIGN — NOT IMPLEMENTED

Propose(source_or_venue,instrument_id,event_id) as stable event identity,with event_timeUTC and a source-backed sequence number for deterministic within-time order. For open/close,sort by eventtime then sequence after validating sequence uniqueness/continuity and revision/cancel policy;reject or flag ties whose order cannot be established. Do not invent economic order from arbitrary file position or delete legitimate simultaneous trades. Original bars still rejects duplicate instants,as probed;no event-ID/sequence-aware bar implementation was added.

## 7.13-E8

**Prompt:** List calendar and feed-completeness evidence required before treating an empty interval as confirmed no trading.

**Scope:** SOURCE LIMIT + EXTERNAL COMPLETENESS DESIGN

The original empty interval means no supplied events only. Before claiming confirmed no trading,need instrument/venue session and holiday/early-close calendars,timezone/rule versions,halt/status evidence,source availability and coverage guarantees,sequence-gap/replay checks,complete reporting horizon,late/corrected event policy and reconciliation controls. Removing the whole14:29 event still yields a locally valid3-event report with first-binclose100;count conservation cannot discover that omitted source event. A nonempty bin can also be incomplete. No exchange calendar or live feed certification was performed.

Original source demonstration, discovery and compileall pass with FutureWarning as error. No unexpected QA failure or manuscript defect surfaced; first-run outputs and expected rejection traces retained. No historical unique methods or earlier workflow cases added by overlapping reruns. F28/F32, F37 history and platform/input/numerical/independent acceptance limits remain intact.
