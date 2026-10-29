# Chapter 19 — Scenario provenance and event-report follow-up

**Date:** 2026-10-29
**Scope:** Section 19.9 portion of COV-83.
**Status:** Input-report contract reconciled and selected event boundaries checked; independent review pending.

## Confirmed contract gap and correction

The manuscript promised initial balance, rate, continuous flow and horizon, but the simulator omitted them from returned reports. Each result now includes an inputs snapshot containing those validated numeric values and the full normalized jump schedule. The snapshot is created before time-zero processing and survives all terminal returns, including events that prevent later scheduled transfers.

The report also identifies the constant-rate account model and states its time-zero-jump and future-coincidence policies. Its nested schedule uses immutable numeric pairs rather than references to the caller's mutable lists. JSON renders those pairs as arrays. Scheduled count, applied count and event trace remain separate: retained scheduled inputs do not mean every transfer was applied.

The manuscript now explains the input schema, direct floating-point event comparisons, and negative-jump trace behavior. A jump can log a negative raw post-transfer balance while the terminal model result clamps the reported balance to zero. No event-time tolerance or overdraft policy was added.

## Selected regression evidence

Ten scenarios assert the complete input snapshot, terminal status, scheduled count, model and policy metadata, repeatable sorted JSON serialization, successful JSON round-trip and independence from later caller-list mutation. They include ordinary completion, initial depletion, a skipped late deposit, negative-jump depletion, negative and rescuing time-zero transfers, exact depletion coincidence, adjacent representable transfer times, and zero horizon.

Additional exact event-log assertions cover:
- A withdrawal of 150 from a balance of 100 at year one, followed by depletion and no later transfer.
- A time-zero deposit rescuing a zero initial balance.
- A deposit immediately before year-two depletion, at year two, and immediately after it, using math.nextafter. Only the first is applied.

These simple zero-rate cases independently determine crossing time and balances. They do not certify all near-coincident events under nonzero-rate rounding, Section 19.7's distinct intentional policy, nonterminal overdrafts or general transaction idempotency.

## Runtime and publication

Baseline tree: `48c7e5fab38521320e497db7aa393a5531560008`. All 21 Chapter 19 Python sources were fetched at that revision; the scoped snapshot replaced only the Section 19.9 simulator and checker.

Python 3.12.14/Linux: 21/21 files compiled with py_compile; 11/11 check scripts exited zero, with assertions enabled, their code directory as working directory and a 15-second per-script timeout. The Section 19.9 CLI also exited zero and its output parsed as JSON; the late-deposit scenario retained its scheduled input despite zero applied jumps. This is a scoped follow-up, not a new full-book run.

| File | Commit | Blob |
|---|---|---|
| [section_19_09.py](../chapter-19/code/section_19_09.py) | `dc00308d8fe95ca7d3475b49644875009ba0b49f` | `7630bbadf395ecc9033bfd4fd58b8c60cf57a06d` |
| [check_section_19_09.py](../chapter-19/code/check_section_19_09.py) | `7a7f807182d50f39765c5e150758eb56c1750de0` | `06f760fb4887afd7c04553d3300c3c2f80be3d0f` |
| [19.09-chapter-project-continuous-account-growth-and-depletion-simulator.md](../chapter-19/19.09-chapter-project-continuous-account-growth-and-depletion-simulator.md) | `bfb15cc283639857d293bf695fdc09da0cbb39f5` | `9c2802a16c6b10814b830db2c2bed6750d4a0810` |

COV-83 remains partially open for broader event numerics, cross-section policies and independent review. Production provenance, durable transaction identifiers and ledger controls remain optional extensions rather than implemented guarantees.

[Chapter 19 map](coverage-chapter-19.md) · [Remediation queue](substantive-coverage-index.md) · [Progress tracker](PROGRESS.md).
