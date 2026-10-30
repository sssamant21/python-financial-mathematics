# Sections 7.13–7.16 — Formal workflow contracts

Four workflows each have eight derived units; these are not commands, predicates or unique methods. Setup partial;six assembly/execution categories pass within scope;interpretation reviewed conceptually.

## 7.13

Summarize supplied single-instrument events in an independently specified UTC half-hour reporting horizon.

**Prerequisites/input:** Exact price/volume frame,1–10000 events,unique aware complete DatetimeIndex. Ordinary finite nonnegative numeric values. Aware Timestamp boundaries aligned to UTC half hours; positive horizon<=1day,all events inside[start,end). Consistent price and event-volume units assumed.

**Outputs/step alignment:** UTC interval_end grid with at most48 right-labeled,left-closed,epoch-anchored bins. OHLC from chronologically sorted events,volume sum(min_count=1),event_count and has_observations. Leading/trailing empty bins preserved; financial measuresNaN,counts0.

**Independent expectation:** First[14:00,14:30) contains prices100,102,volume10+20=30,OHLC100/102/100/102. Boundary14:30 belongsnextbin close101. Counts[2,1,0,1],volumes30/5/NaN/7,sum42. Explicit end16:00 excluded. Single14:30event yields[0,1,0,0] with both edge gaps. Observedzero is distinct from emptyNaN.

**Limits:** Bins summarize supplied events,not certified complete feed or trading sessions. Bar label is neither close-observation time nor availability proof. Unique timestamps are a teaching grain,not general trade-feed grain. Cumulative volume cannot be summed as event volume; asfreq is grid selection,not OHLC. No venue calendar/multi-event ordering integration or exact accounting.

## 7.14

Build trailing three-observation and expanding descriptive price summaries while preserving warm-up and alignment.

**Prerequisites/input:** Series1–10000 complete finite nonnegative ordinary numeric prices,unique increasing aware DatetimeIndex. Unsorted input rejects instead of silently sorting. Single instrument/common price convention; irregular spacing intentional.

**Outputs/step alignment:** Owned float64 price,rolling_mean,rolling_std(ddof1),expanding_mean,prior_mean on UTC index. Three-observation window current-inclusive,right-aligned,min_periods3; prior_mean shifts computed mean one row. Mature values finite; leadingNaNs intentional.

**Independent expectation:** Three-row means102/104/106,standard deviations2 from squared deviations8/(3-1)=4. Expanding scalar means100/101/102/103/104. First2 rolling rows and first3 prior rowsNaN. At14:40,30min right-closed window excludes14:10 and returns104 rather than102. Final-price perturbation preserves all earlier outputs and lastprior104.

**Limits:** Price standard deviation has price units,not return volatility or annualized risk. Equal observation weights are not time weights. Shift1row is not30elapsed minutes or tradingday. Future-perturbation checks do not establish publication/decision availability. Overlapping samples,source completeness,extreme variance accuracy and platform acceptance remain outside scope.

## 7.15

Transform complete positive prices into adjacent-observation returns with explicit interval identities and endpoint reconciliation.

**Prerequisites/input:** Series2–10000 positive finite ordinary numeric prices,unique increasing aware index. Same instrument,currency,unit and adjustment basis,no flows/distributions/fees/FX. UTC-normalized copied numeric source; no implicit fill or inferred calendar.

**Outputs/step alignment:** Price,interval_start,elapsed,simple_return,gross_return,log_return,cumulative_price_return. First intervalNaN/NaT with baseline cumulative0. Finite supported mature outputs,positive gross and simple>-1; zero prices excluded from combined log-capable API.

**Independent expectation:** 110/100-1=1/10;99/110-1=-1/10;grossproduct(11/10)*(9/10)-1=-1/100 equals99/100-1. Adjacent sum0 differsfromlinked-.01. Elapsed3days then1day. Logsum agreeswithmath.log(99/100) within1e-12. First cumulative0 is baseline,not an observed firstintervalreturn.

**Limits:** Rowpair is not daily/session interval. No-fill does not prove expected schedule completeness. Positive-price returns do not establish total-return adjustment/corporate-action/cashflow correctness. Normal rounding and small-change/log cancellation remain; strict range guards are not arbitrary precision. Terminalzero could support a separate simple-only contract,not this combined API.

## 7.16

Reshape unique asset-time observations onto independent expected axes and compare only adjacent common-grid endpoints.

**Prerequisites/input:** Tuple1–100 unique trimmed assets<=64chars;aware complete increasing unique DatetimeIndex2–1000times,grid<=100000cells. Long frame1–100000 records exact time/asset/price,aware datetime timecolumn,ordinary positive finite prices,keys subsetofexpectedaxes andunique after UTC normalization.

**Outputs/step alignment:** Wide prices with expected ordered assets/times,unfilled wide adjacent-grid returns and complete_interval flag only when all expected endpoints exist. Structural absence retained; suppliedNaN rejects. No portfolio weights or partial averaging/renormalization.

**Independent expectation:** ALPHA100/110/99 =>+.1/-.1. BETA200/missing/220 =>both adjacent returnsNaN and completeflags[False,False,False]. SuppliedmiddleBETA210 =>[False,True,True],BETAreturns1/20 and1/21. Entire absentasset/time remainsvisible. BETAendpoint+.1 spans2days and is not missing1dayreturn.

**Limits:** Expected axes need independent provenance; UTC labels do not prove fresh synchronized quotes or availability. Common currency/per-unit and adjustment assumptions are not established by schemas. Synthetic weekend grid is not venue calendar. No covariance sample policy,portfolio performance,as-of matching or matrix-model acceptance. Gridcap is not peak-memory guarantee; float64 range/rounding limits remain.

All 12 explanatory fences execute unchanged, with their full hashes and namespace prerequisites recorded. Section 7.13 presupposes table and result: QA supplies original fixture and an empty result frame; the original resample statement creates grouped, and assignment adopts its output index. This tests the volume fragment alone, not a claim that the two fragments build full OHLC. Section 7.14 presupposes prices and rolling_mean; original fixture supplies prices and exact summaries supplies rolling_mean because the earlier prose names its computed mean variable mean. Original snippet statements are not renamed. Section 7.15 uses original prices fixture with pd/np imports. Section 7.16 starts from original records/expected_axes, then executes pivot, reindex and no-fill returns in order. These preludes are QA orchestration, not standalone source algorithms or solutions to still-pending local exercises.

Independent expectations use integer/rational arithmetic, explicit interval membership and prefix sums; math.log of the endpoint ratio supplies a separate logarithmic route. Original methods cover count/volume conservation, empty/leading gaps, timezone and source-order behavior, asfreq contrast, warm-up/min_periods/ddof, future perturbation, missing/no-fill mechanics, invalid axes/values, extreme ratios, complete/incomplete expected-grid behavior, long/wide roundtrip and ownership. Full original demo outputs match independently transcribed published-table expectations after whitespace-only normalization. No performance model, financial replacement implementation or live workflow was built.

No unexpected QA failure or manuscript defect surfaced. First-run evidence is retained. Common-grid and asset-specific intervals answer different questions; no missing interval is fabricated. Troubleshooting explanations align with tested conditions. Local exercises, Section 7.17 project/checklists, external completeness/calendar/adjustment metadata and independent acceptance remain pending.
