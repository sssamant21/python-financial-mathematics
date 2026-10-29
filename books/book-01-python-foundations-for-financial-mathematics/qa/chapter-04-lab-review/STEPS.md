# Chapter4 Sections4.1–4.6 formal lab review

These six review units per lab are derived checklist items, not a preexisting numbered source lab or36 independent execution cases. Test methods are recorded separately.

## 4.1 — structured_information_lab

Exact five-field payment schema; copy validated immutable values to a fresh dictionary; exact date excludes datetime. Presence/type/domain/calendar and source-preservation tests remain separate from monetary arithmetic; downstream valuation context is not established.

- **Prerequisite/file layout** — Python3.10+ standard library; exact standalone source saved with the documented filename.
- **Contract and ownership** — Exact five-field payment schema; copy validated immutable values to a fresh dictionary; exact date excludes datetime. Presence/type/domain/calendar and source-preservation tests remain separate from monetary arithmetic; downstream valuation context is not established.
- **Execute source suite** — Six exact source methods passed with no skips; full stdout/stderr retained.
- **Interpret expected summary** — Ran6 tests andOK checked; method count is not subcase/assertion count.
- **Import behavior** — Fresh subprocess imports without stdout/stderr.
- **Limits/cleanup** — Temporary directory removed; no-O/OO; Windows/macOS not executed; no production or independent model acceptance inferred.

## 4.2 — lists_lab

List of finite Decimal amounts permits signs/zeros and duplicate receipts. Positive selection preserves order and new-list ownership. Entire input is validated; selection alone loses period metadata and is not a full payment schedule.

- **Prerequisite/file layout** — Python3.10+ standard library; exact standalone source saved with the documented filename.
- **Contract and ownership** — List of finite Decimal amounts permits signs/zeros and duplicate receipts. Positive selection preserves order and new-list ownership. Entire input is validated; selection alone loses period metadata and is not a full payment schedule.
- **Execute source suite** — Six exact source methods passed with no skips; full stdout/stderr retained.
- **Interpret expected summary** — Ran6 tests andOK checked; method count is not subcase/assertion count.
- **Import behavior** — Fresh subprocess imports without stdout/stderr.
- **Limits/cleanup** — Temporary directory removed; no-O/OO; Windows/macOS not executed; no production or independent model acceptance inferred.

## 4.3 — tuples_lab

Two-item period/amount tuples retain period identity, source order and duplicates. Positive selection does not enforce unique periods, sort a schedule or establish a time unit/currency. Invalid later rows reject before a partial result can escape.

- **Prerequisite/file layout** — Python3.10+ standard library; exact standalone source saved with the documented filename.
- **Contract and ownership** — Two-item period/amount tuples retain period identity, source order and duplicates. Positive selection does not enforce unique periods, sort a schedule or establish a time unit/currency. Invalid later rows reject before a partial result can escape.
- **Execute source suite** — Six exact source methods passed with no skips; full stdout/stderr retained.
- **Interpret expected summary** — Ran6 tests andOK checked; method count is not subcase/assertion count.
- **Import behavior** — Fresh subprocess imports without stdout/stderr.
- **Limits/cleanup** — Temporary directory removed; no-O/OO; Windows/macOS not executed; no production or independent model acceptance inferred.

## 4.4 — dictionaries_lab

Identifier index rejects duplicates rather than overwrite; exact/case-sensitive nonblank strings are not trimmed. Strict field set, teaching USD/EUR allowlist and finite signed/zero amounts are validated. Source ownership and local all-or-error behavior do not imply database transactions.

- **Prerequisite/file layout** — Python3.10+ standard library; exact standalone source saved with the documented filename.
- **Contract and ownership** — Identifier index rejects duplicates rather than overwrite; exact/case-sensitive nonblank strings are not trimmed. Strict field set, teaching USD/EUR allowlist and finite signed/zero amounts are validated. Source ownership and local all-or-error behavior do not imply database transactions.
- **Execute source suite** — Six exact source methods passed with no skips; full stdout/stderr retained.
- **Interpret expected summary** — Ran6 tests andOK checked; method count is not subcase/assertion count.
- **Import behavior** — Fresh subprocess imports without stdout/stderr.
- **Limits/cleanup** — Temporary directory removed; no-O/OO; Windows/macOS not executed; no production or independent model acceptance inferred.

## 4.5 — sets_lab

Expected membership must be unique; repeated received IDs become duplicate evidence. Four fresh sets omit source order, amounts and duplicate frequency. Identity reconciliation is not financial amount reconciliation or transaction approval.

- **Prerequisite/file layout** — Python3.10+ standard library; exact standalone source saved with the documented filename.
- **Contract and ownership** — Expected membership must be unique; repeated received IDs become duplicate evidence. Four fresh sets omit source order, amounts and duplicate frequency. Identity reconciliation is not financial amount reconciliation or transaction approval.
- **Execute source suite** — Six exact source methods passed with no skips; full stdout/stderr retained.
- **Interpret expected summary** — Ran6 tests andOK checked; method count is not subcase/assertion count.
- **Import behavior** — Fresh subprocess imports without stdout/stderr.
- **Limits/cleanup** — Temporary directory removed; no-O/OO; Windows/macOS not executed; no production or independent model acceptance inferred.

## 4.6 — nested_structures_lab

Nested strict schemas retain portfolio identity while flattening validated positions. Nonnegative finite Decimal quantities permit zero/fractions but omit shorts/lot-size constraints. No arithmetic, pricing or aggregation is performed; local input preservation is not concurrency/persistence safety.

- **Prerequisite/file layout** — Python3.10+ standard library; exact standalone source saved with the documented filename.
- **Contract and ownership** — Nested strict schemas retain portfolio identity while flattening validated positions. Nonnegative finite Decimal quantities permit zero/fractions but omit shorts/lot-size constraints. No arithmetic, pricing or aggregation is performed; local input preservation is not concurrency/persistence safety.
- **Execute source suite** — Six exact source methods passed with no skips; full stdout/stderr retained.
- **Interpret expected summary** — Ran6 tests andOK checked; method count is not subcase/assertion count.
- **Import behavior** — Fresh subprocess imports without stdout/stderr.
- **Limits/cleanup** — Temporary directory removed; no-O/OO; Windows/macOS not executed; no production or independent model acceptance inferred.

