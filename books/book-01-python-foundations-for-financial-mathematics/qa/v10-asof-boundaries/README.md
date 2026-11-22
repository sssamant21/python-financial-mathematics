# V10 — Partial Section15.13 availability/clock/revision boundaries

Executed source pin: `e40e5540302f0767f169978f9964e94655d5fc1e`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-asof-boundaries/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-asof-boundaries/review.py replay
```

**68 predicates pass twice with identical rows:**25 numeric-clock cases,25 aware-time cases,six native/caller latency-boundary checks,five revision/metadata checks,two unit-convention checks and five invalid-clock/domain checks. Flags/lists/identities compare exactly. The independent reference is known elapsed integer seconds used to construct aware instants under explicit offsets−05:00,UTC,+05:30, not lexical local-time comparison. No new ZoneInfo/DST database or Windows/macOS platform evidence is asserted; earlier F139 DST evidence retains its own scope.

The source correctly flags only recorded availability strictly later than the recorded decision. It returnsFalse at equality. A separate caller convention with.1second processing delay makes recorded availability9.95 and decision10 not ready despite a native late flagFalse;9.8 is ready. These are caller readiness calculations, not a source order/execution API or measured latency. NativeFalse is a necessary timing-screen result, not strategy acceptance or proof of adequate processing/execution time.

For an original value100 available9 and revised value150 available12, native flags are[False,True] at decision10 and[False,False] at13. A **supplemental** latest-eligible-version selector consequently chooses100 then150. The source does not choose versions, authenticate source records or detect a revised value falsely supplied with availability9. Recorded backdating can pass the numeric screen; that illustrates absent authenticity inputs, not a comparison-code defect. Event/publication/availability/decision/execution clocks remain separate data contracts.

Numeric units are caller-declared: decision10seconds versus supplied availability9000milliseconds is wrongly treated as late unless the caller first converts9000ms to9seconds. No source unit conversion, synchronization, time-zone inference or source provenance is claimed. Source rejects booleans/nonfinite numeric ticks, lexical timestamps, naive datetimes and mixed clock families. Those rejection checks do not validate actual clock synchronization or delayed feeds.

The manuscript's timing/revision project and answer contracts align at this selected synthetic scope. Actual publication logs, immutable source versions, ingest delays, venue order fills, costs and calendars remain unavailable; no real as-of join or strategy audit is accepted. Prior24 local answers/twelve project tasks are not new records. Each run executes the full verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. Executed whole source matches F219's corrected-prose candidate; executable fence matches F139's earlier corrected listing. F139 fifteen baseline failures/42 arithmetic predicates and F219 wording correction retain scope. No source change/defect or new workflow/answer/step/historical-method totals.

Section15.13 remains partial:next ACF/volatility/nonstationarity/missingness/outlier/cost and supplied-project assumptions before15.14. V10/Book1,F28/F32/F209/F165/F185 and broad numerical/resource/data/model/platform/release/independent/canonical gates remain open. No independent or operational acceptance.
