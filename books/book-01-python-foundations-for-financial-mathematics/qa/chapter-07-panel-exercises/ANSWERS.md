# Section 7.16 — Worked answers

**7.16-E1. Add BETA's middle price as 210 and verify two complete intervals with scalar per-asset checks.**

Adding BETA 210 at the middle instant produces two complete intervals. ALPHA: 110/100 − 1 = 10%, 99/110 − 1 = −10%. BETA: 210/200 − 1 = 5%, 220/210 − 1 = 1/21 ≈ 4.7619%. The first row remains a baseline without a prior interval.

**7.16-E2. Remove all BETA records and explain why the expected BETA column must remain visible.**

The expected BETA column remains on the independently supplied asset axis. Its prices and returns are unknown throughout, so no interval is complete across both assets. Inferring the axis from received rows would silently shrink the universe.

**7.16-E3. Remove every record at the middle instant and inspect the expected all-missing row.**

Removing all middle records leaves the expected middle row present with both prices missing. Each daily interval needs that row at one endpoint, so all adjacent-grid returns remain undefined. The source does not bridge the missing row.

**7.16-E4. Duplicate an ALPHA-time key and explain why pivot-table averaging would require a separate policy.**

A conflicting duplicate ALPHA key fails the uniqueness check. Averaging 100 and 102 would give 101, a different price that requires an explicit aggregation rule and quote provenance. A duplicate may instead be a correction or an ingestion error.

**7.16-E5. Reverse expected asset order and confirm that column labels and values move together.**

The order becomes BETA, ALPHA. Reindexing the new output back to ALPHA, BETA restores both price and return matrices exactly, including NaNs. Complete-interval flags are unchanged.

**7.16-E6. Calculate BETA's own two-day return and explain why it is not the missing one-day return.**

BETA’s observed endpoints are 200 and 220, so the two-day price return is 10%. There is no BETA quote at the intervening expected instant, so this ratio cannot determine either daily return.

**7.16-E7. Design a common two-day endpoint comparison without relabeling it as daily performance.**

Define common start and end UTC instants and require a valid positive price for each asset at both. The Jan 30 to Feb 1 comparison gives ALPHA −1% and BETA +10%; label it a two-day endpoint return, and retain the missing middle observation in coverage metadata. This does not change the source daily matrix.

**7.16-E8. Specify the metadata and completeness checks required before exporting a return matrix for portfolio risk calculations.**

Export ordered asset labels and exact start/end instants, calendar and horizon, units/currency and FX convention, field and adjustment policy, dataset version/provenance, missingness flags and completeness rule. Check unique keys, finite supported values and identical asset intervals; reject incomplete rows or apply an explicitly approved missing-data policy before covariance. Do not infer risk readiness from a rectangular shape.
