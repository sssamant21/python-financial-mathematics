# Section 9.2 — Worked practice review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Borrower/lender | Borrower flows are {0:2000, 1:−1100, 2:−1100}; lender representations reverse the signs of those transfers. The borrower sum is −200 USD, not a rate. A counterparty ledger needs actual transfer identities where fees involve third parties. | Exact source and integer monetary oracle |
| 2. Beginning/end | End dates [1,2,3] become beginning dates [0,1,2]; each investor deposit remains −100. This changes timing, not viewpoint or amount. | Exact source alternate schedules |
| 3. Zero net | The receipt50 and fee−50 at time2 are two events with distinct IDs and net0. An explicitly empty complete schedule yields the same grid but a different ledger. | Exact source alternate schedule |
| 4. Unconfirmed completeness | No supplied time2 row cannot establish zero when completeness is unknown. Resolve that information or retain a richer unknown state before valuation. The teaching helper has no completeness detector. | Contract review only |
| 5. Sum versus return | The fixture's undiscounted sum is155 USD. It neither translates dated flows to a common date nor measures capital exposure over time, so it is not an NPV, account balance or investment rate. | Source fixture sum and conceptual review |

The fixture totals are {0:−1000,1:75,2:0,3:1080}. Five events survive netting, including two at1 and two at3. For three intervals the dense grid has four boundaries. Sorting IDs within a boundary is a display convention; it does not infer intraperiod sequence.
