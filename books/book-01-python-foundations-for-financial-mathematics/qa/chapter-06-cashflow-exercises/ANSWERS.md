# Section 6.8 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling listings; aligned exact int64 periods/float64 amounts within teaching bounds. Caller establishes perspective, currency, event completeness and abstract period origin/unit. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.8-E1

Add a payment of -25 at period 2, preserving order, and derive the new cumulative vector and nominal net.

**EXACT SOURCE + INDEPENDENT RATIONAL ORACLE**. Insert period 2 and payment −25 into both vectors in order: periods [0,1,2,3,4], amounts [−1000,200,−25,−50,1000]. Ordered rational addition gives cumulative [−1000,−800,−825,−875,125], nominal net 125. The new event is a known payment, not a gap fill. All stored output values match; perspective, USD and abstract-period assumptions remain those of the source fixture.

## 6.8-E2

Reverse the investor perspective and explain which amounts and cumulative values change sign.

**EXACT SOURCE PERSPECTIVE PROBE**. Reverse to the counterparty perspective by negating every supplied signed flow, giving [1000,−200,50,−1000]. Cumulative values become [1000,800,850,−150] and nominal net −150. Periods stay [0,1,3,4]. These are the same events with opposite receipt/payment signs, not a new investment or changed timing. Rename the perspective metadata as well; the numeric kernel cannot do that for the caller.

## 6.8-E3

Create a dense representation only after stating that the gap at period 2 is a known no-flow period.

**EXACT SOURCE DENSE REPRESENTATION + COMPLETENESS PRECONDITION**. Only after asserting a complete source schedule and known no flow at offset 2, use dense periods [0,1,2,3,4] with amounts [−1000,200,0,−50,1000]. Cumulative values are [−1000,−800,−800,−850,150]. The repeated −800 records no change over that known no-flow slot; net remains 150. This controlled construction does not infer completeness from an absent row or implement a general imputation adapter. An unknown amount must remain missing/incomplete and is not the same as zero.

## 6.8-E4

Add tests for the maximum allowed period offset and an amount exactly at the negative magnitude bound.

**EXACT SOURCE INCLUSIVE-BOUNDARY PROBES**. A one-event schedule at period 1,000,000 with amount −1,000,000,000,000 is accepted: cumulative and nominal net equal −1e12. A first event later than zero is permitted; no initial event is invented. Period 1,000,001 and amount −1e12−1 independently raise ValueError. These exercise both inclusive endpoints and adjacent outside values, without changing the teaching bounds or claiming arbitrary monetary precision.

## 6.8-E5

Propose an upstream grouping policy for a receipt and payment at the same period while preserving gross-event evidence.

**GROUPING DESIGN + SUPPLEMENTAL CONTROLLED EXAMPLE**. Before grouping, require consistent perspective, currency, time origin/unit, legally permitted netting and complete known finite event amounts. Group by that full key plus period, preserving immutable raw event IDs, amounts, source references and grouping-rule version. Retain gross receipts, gross payments, event count/IDs and net, with an audit link from grouped row to raw records. The controlled period-2 receipt 200/payment −50 retains IDs receipt/payment, gross receipts 200, gross payments magnitude 50 and net 150; pass the explicitly grouped single event to source. The unchanged source rejects duplicate periods [2,2]. Opposite 50/−50 nets to zero but gross movement is 100, so retain the zero group and evidence rather than dropping it. This is a design plus a tiny rational grouping example, not a general ingestion/accounting implementation; rounding and representation at the upstream boundary need an explicit policy.

## 6.8-E6

Demonstrate how sorting only periods corrupts an intentionally unsorted pair of vectors.

**EXACT SOURCE + PAIRED-SORT COUNTEREXAMPLE**. Start with intentionally unsorted periods [3,0,4,1] paired with amounts [−50,−1000,1000,200]. Original source rejects them. Stable argsort of periods, applied to both vectors, restores [(0,−1000),(1,200),(3,−50),(4,1000)]. Sorting only periods produces [(0,−50),(1,−1000),(3,1000),(4,200)] and source accepts that numerically valid but semantically false schedule. Its cumulative [−50,−1050,−50,150] is wrong despite the same nominal net 150. Identity/timing alignment is a caller contract; shape and a correct final sum cannot prove it. Source does not sort silently.

## 6.8-E7

Explain why changing period offsets does not change this implementation's nominal net.

**EXACT SOURCE TIMING-INVARIANCE PROBE**. Replace offsets [0,1,3,4] with [0,10,30,40] while keeping the same aligned amounts. The source preserves the new timing but returns identical cumulative [−1000,−800,−850,150] and net 150 because cumsum uses event order and amounts, not elapsed time. This is nominal addition only; it does not imply time is irrelevant to valuation, accrual, year fractions or account balances.

## 6.8-E8

Specify the additional assumptions needed for a present-value calculation without adding an unstated rate convention.

**VALUATION DESIGN + EXPLICIT SUPPLEMENTAL RATIONAL EXAMPLE**. A PV boundary must specify valuation instant, investor perspective, currency, full cash-flow/event meaning, settlement/timing origin, calendar/time zone where relevant, day-count/year fractions, discount-curve provenance and as-of date, quote type, compounding, rate units, interpolation/extrapolation, cash flows at valuation time, accrued/clean-versus-dirty treatment if relevant, credit/default and FX scope, numerical bounds/rounding and missing-input policy. Define discount factors D(t) under those assumptions and calculate sum c(t)D(t); do not assume an abstract period is a year or that one annual rate applies to every event. For an explicitly separate example only, annual periods 0 and1 with annual-effective rate 10% and flows [−100,110] give rational PV −100+110/(1+1/10)=0. The unchanged source returns nominal net 10 on those amounts. That illustrates the distinction without adding a discount-rate convention or valuation capability to the source. No calendar/curve/valuation API or independent model approval is claimed.
