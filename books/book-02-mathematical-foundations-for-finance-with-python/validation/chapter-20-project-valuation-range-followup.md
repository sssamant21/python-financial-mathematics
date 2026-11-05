# Section 20.9 project valuation and Section 20.10 delegation

Date: 2026-11-05. Baseline: `a1fa0e326baecda17be1c1c19461c4f35629af8a`. Corrected executable revision: `503edbdc3e622f98acabea861a53ac1581b9132f`. Final combined Chapter 20 revision: `081a73dce77591e11377df37ff7b23c5d1836674`.

The project validates each complete input, evaluates the scaled term from the exact represented rate/time product, rounds each term, and sums the represented terms exactly before final conversion. Finite terms survive an unrepresentable standalone factor; finite totals survive an overflowing partial sum. Zero terms still require valid inputs. Genuine term and final overflow continue to raise OverflowError. Underflow to zero is permitted, and cancellation of separately overflowing mathematical terms remains outside this per-term rounding contract. The shared kernel's default underflow rejection remains unchanged for existing callers.

An independent 1,600-digit Decimal oracle evaluates selected complete terms and adds their represented results. The range checker exercises the real project and actual Section 20.10 imported callable, runs the 12-method assessment suite, checks one-shot iteration, and checks pending-dossier fields and fresh-instance isolation. The initial run had 17 mismatches across 48 rows, including paired project/delegation observations and precision-only differences; this is not a defect count. All 48 pass at the corrected pin. Project scope: 32 compiled files, 21 passing scripts, and matching hashes. The final chapter/full run also exercises both callers of the shared kernel with unchanged default behavior.

Final combined scope: 33 compiled files and 22 passing scripts, with matching Git blob hashes before and after. [Raw baseline, rerun and scoped hashes](chapter-20-project-valuation-range-followup.json) · [Runnable checker](../chapter-20/code/check_project_valuation_range.py).

Replay from Book 02's chapter-20/code at the corrected revision: run python check_project_valuation_range.py with assertions enabled. For the baseline, save the checker externally, check out the stated baseline and overlay only that checker. Compile each .py via py_compile.compile(path,doraise=True), run check_/test_ basenames in separate processes from their parent directories with a 60-second timeout, and verify raw Git blob hashes before and after. Successful stdout is omitted from the scope summary.

Selected assistant-run Linux evidence only. No independent sign-off, supported-platform validation, release acceptance or canonical approval.
