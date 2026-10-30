# Section 6.6 — Eight scoped answers

Prerequisites: Section 6.1 prepared runtime and unchanged sibling files; exact float64 nonempty vectors; caller-guaranteed identity/label alignment, chronology where relevant, and compatible currency/per-unit conventions. Review: Codex executor, 2026-10-30; not independent acceptance.

## 6.6-E1

Add a fourth shock of 0.25 and derive the output row for all three positions.

**EXACT SOURCE + INDEPENDENT RATIONAL ORACLE**. Append common proportional shock 0.25 to [-0.1,0,0.1], retaining the shock-label order. Signed opening marks are 10×100=1000, −5×80=−400, 0×50=0. The added row is [250,−100,0]; the full source result has shape (4,3), dtype float64 and 96 element bytes. Rational multiplication independently derives all four rows; the equal-shaped pairing error cannot hide in this nonsquare fixture. Signed zero is treated numerically as zero.

## 6.6-E2

Predict np.broadcast_shapes((7, 1), (1, 4)) and verify it without allocating a 7-by-4 calculation result.

**SHAPE-ONLY SOURCE-LIBRARY PROBE**. Aligned trailing dimensions are 1 versus 4, then 7 versus 1, so np.broadcast_shapes((7,1),(1,4)) returns (7,4). The runner calls only this shape utility for this exercise, without creating a 7-by-4 arithmetic table. Shape compatibility alone establishes no scenario/position meaning or whole-process allocation measurement.

## 6.6-E3

Add a test for one scenario and multiple positions, preserving shape (1, N).

**EXACT SOURCE SHAPE/VALUES PROBES**. A one-element float64 shock vector [0.25], with three aligned positions, must produce shape (1,3), not (3,). The source returns [[250,−100,0]]. Additional controlled zero-shock and total-loss shock −1 cases retain shape (1,3) and have expected rows [0,0,0] and [−1000,400,0]. Keep both axes even when a length is one; do not squeeze away the scenario role.

## 6.6-E4

Design an instrument-specific shock matrix contract rather than reusing the common-shock vector silently.

**DESIGN REVIEW + ORIGINAL API REJECTION**. Define a new instrument-specific H array of shape (S,N), axis 0 scenario and axis 1 position. q and P remain aligned (N,) vectors; output change[s,i]=(q[i]P[i])H[s,i]. Require exact float64, nonempty dimensions, finite inputs, nonnegative prices, every H>=−1, exact matched label order and cell budget S×N; preserve source arrays and strict arithmetic/finite-output policy. Scenario and position IDs must accompany ingestion. No probability or aggregation is implied. Under H=[[-0.1,0,0.25],[0.2,−0.5,0]], rational outputs are [[−100,0,0],[200,200,0]]. The unchanged common-shock API correctly rejects a 2-D shock matrix. Only the rational design example is evaluated; a new matrix API and its full validation suite are not implemented.

## 6.6-E5

Calculate the element payload for 10,000 scenarios and 2,000 positions; distinguish it from peak process memory.

**INDEPENDENT INTEGER PAYLOAD + EXACT SOURCE BUDGET REJECTION**. 10,000×2,000=20,000,000 float64 cells; 8 bytes each gives 160,000,000 bytes =160 decimal MB =152.587890625 MiB. This is output element payload only. Input vectors, validation masks, opening marks, finite-output checks, Python/allocator overhead and other process allocations add memory. Peak RSS was not measured. The runner allocates only small input vectors and verifies the unchanged default 1,000,000-cell budget rejects this request. Code review confirms this check precedes output arithmetic; no huge result is materialized or OS reservation claimed.

## 6.6-E6

Add a test proving a zero-quantity position still rejects an invalid price.

**EXACT SOURCE REJECTION PROBES**. For quantity [0] and shock [0], supply price [−1], [NaN], then [+inf] independently. The unchanged source rejects all three with ValueError, with input bytes unchanged. Flat exposure does not grant permission to disregard invalid supplied data. Expected traces are retained separately from unexpected failures; no manuscript test listing is changed.

## 6.6-E7

Explain why forcing a broadcast view writable would undermine an ordinary independent-scenario assumption.

**SHARED-STORAGE PROBE + CONCEPTUAL OWNERSHIP REVIEW**. np.broadcast_to on an owned length-three vector creates a read-only (2,3) view sharing storage and with zero scenario stride. Ordinary assignment raises ValueError. A deliberate view.copy() permits an independent edit. On a separate disposable owned vector only, forcing the broadcast view writable and setting [0,0]=999 changes the backing vector and both displayed scenario entries to 999. Distinct logical rows can refer to one storage location; forcing writability breaks an ordinary independent-scenario assumption. Never use the forced-write counterexample as an operational pattern. No concurrent-write safety or general setflags compatibility is claimed.

## 6.6-E8

Outline chunk processing that preserves scenario labels and avoids an unintended reduction axis.

**CHUNK DESIGN + CONTROLLED SOURCE CALLS**. Choose a scenario chunk size C with C×N within a positive cell budget and iterate lo=0,C,2C,...; hi=min(lo+C,S). Pass the original aligned q/P and shocks[lo:hi] to the unchanged source. Retain scenario_labels[lo:hi] and fixed position IDs with each (hi−lo,N) result. This runner executes five controlled scenarios in chunks (2,3),(2,3),(1,3), verifies all values with a rational oracle, and checks every ordered scenario label appears once. It collects the tiny fixture to verify assembly; that is not a bounded-memory streaming implementation. For large work, validate all input/label/domain contracts up front, write each chunk to a controlled sink with range/hash/status metadata, and mark completion only after every range succeeds. A later-chunk failure must leave an explicit incomplete report; concurrency needs a separate snapshot policy. Do not reduce axes unless the downstream contract explicitly requires it: sum(axis=1) would total positions per scenario only for compatible units/currencies, while sum(axis=0) totals scenarios and needs a separate interpretation/probability policy. Streaming sink, failure recovery and aggregation are designs only.
