# Chapter 1 — Scoped script and interactive-calculator validation

**Date:** 2026-10-28. **Reviewer / correction owner:** Codex. **Source:** Book 1 baseline `f429fb81b8d8f7d228100333c76019d583200d64`. Chapter 1 manuscripts were unchanged through `695f393a6c14d37973bdd0644fc5a062df6f9af7`; Section 1.12 is corrected with this evidence publication. Source SHA-256 values and selected Python-block indices are retained in [results.json](results.json); [source-correction.json](source-correction.json) identifies the original and corrected Section 1.12 source.

## Scoped result

PASS after correcting F14: eleven selected example groups, fifty-five interactive input/output cases across six complete programs, and seventeen extracted-directory compilation checks. These are script checks, not unittest methods; the Book 1 unittest-method total remains 2,996.

| Material | Scoped execution |
|---|---|
| Sections 1.1–1.9 and 1.11 | Ten selected example groups |
| Section 1.13 companion | One selected non-interactive example group |
| Section 1.10 validated input example | 6 interactive cases |
| Section 1.12 complete calculator | 18 interactive cases, including all six menu operations |
| Companion applied savings calculator | 6 interactive cases |
| Companion applied trade calculator | 4 interactive cases |
| Companion reconciliation checker | 4 interactive cases |
| Companion capstone console | 17 interactive cases, including all six menu operations |

Known-answer cases cover simple/compound interest, percentage change, profit/loss and return, posted fees and reconciliation. Boundary and rejection cases include period zero, zero rate, zero denominators, negative or invalid periods/frequency, non-finite and nonnumeric input, tolerance boundaries, invalid menu selection, fractional discrete periods, zero quantity, undefined percentage returns, and sub-cent gains/losses. The exact stdin, expected output fragments, statuses and log paths appear in the JSON record.

## F14 — Premature P/L rounding

**Severity:** Medium instructional financial-result defect. **State:** Corrected. **Owner:** Codex. **Original source revision:** unchanged baseline through the head above.

The complete Section 1.12 calculator rounded monetary profit/loss to cents before using it for sign classification and percentage return. With purchase 0.10, sale 0.104 and quantity 1, the unrounded gain is 0.004 and the return is 4%. The original code reported BREAK-EVEN and 0.00%. The corresponding loss fixture, sale 0.096, also became BREAK-EVEN instead of LOSS.

Original results are retained in [original-subcent-gain.log](original-subcent-gain.log), [original-subcent-loss.log](original-subcent-loss.log), and [original-failures.json](original-failures.json).

The calculator now retains `raw_profit_loss` for sign classification and percentage return, and rounds the displayed monetary amount separately. The manuscript explains this basis with the gain fixture. This aligns the complete program with its preceding unrounded P/L and percentage formulas and with the companion's raw-return treatment.

Both regression cases passed after the correction:

| Fixture | Displayed monetary P/L | Classification | Return |
|---|---:|---|---:|
| Purchase 0.10, sale 0.104, quantity 1 | 0.00 | PROFIT | 4.00% |
| Purchase 0.10, sale 0.096, quantity 1 | -0.00 | LOSS | -4.00% |

Signed zero here reflects the separately rounded Decimal display; it no longer controls the classification or return. All fifty-five interactive cases passed in the corrected run. This targeted correction does not approve every financial convention or numerical range.

## Environment and reproduction

Python 3.12.14 on Linux x86_64 with glibc 2.39. The environment-verification examples imported NumPy 2.3.5, pandas 2.2.3 and Matplotlib 3.10.8. The calculator implementations otherwise use the standard library.

From the repository root, choose a fresh output directory:

```sh
python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-01-runtime/run_reference_checks.py books/book-01-python-foundations-for-financial-mathematics/chapter-01 /tmp/chapter01-repro
```

The [runner](run_reference_checks.py) concatenates only the recorded selected fences for example groups. It extracts the six complete interactive programs without changing their code, supplies controlled stdin to a fresh process for each fixture, and requires zero exit status, empty stderr and all expected output fragments after whitespace normalization. Invalid-input scripts can deliberately print diagnostics while exiting zero, so output is checked explicitly. Programs run with `-W error::FutureWarning`, a thirty-second timeout and `MPLBACKEND=Agg`; compilation uses `python -m compileall -q .`. [all-checks.log](all-checks.log) retains detailed output.

## Remaining scope and milestone

Sections 1.1–1.3 retain their manuscript provenance note about controlled canonical reconstruction; execution does not authenticate inaccessible originals. Full OS setup, Windows/macOS commands, every illustrative fragment, every worked-answer argument, external data, all input domains and numerical-context limits were not validated here. The intentionally unsafe eval example was not executed. Earlier canonical labels remain publication history rather than independent acceptance decisions.

**Milestone:** every Book 1 chapter now has scoped runtime evidence. Comprehensive mathematical, source, editorial, platform and final-acceptance reviews remain pending.

**Next action:** Book 1 structural and internal-link validation (V01–V02).
