# V06 — Chapter 3 chapter-wide exercise review

Date: 2026-10-29. Source baseline: `098e8583d49ea0525b6cbc7f000fd7f9bbe9dadd`.

**PASS (scoped): all 20 Section3.15 exercise answers reviewed; 49 predicates passed, zero failed.** The existing combined project/solution suite also passed its 19 methods. That is a rerun of existing methods, not 19 new methods; historical totals are unchanged. Chapter3 labs, earlier section exercises and full project/checklist review remain separate and open.

| Evidence | Scope |
|---|---|
| [Answer review](ANSWERS.md), [register](answer-register.json) | 20 prompt-to-answer records, assumptions/timelines and prose review; no grading claim |
| [Runner](review.py), [results](results.json) | Exact source project/companion extraction, 49 predicates, rational oracles and recorded environment |
| [Mutation evidence](mutation-evidence.json) | Temporary known division defect gives156.25 versus expected100; canonical code unchanged |
| [Reproduction record](reproduction.json) | Exact fixture inputs/conventions, context, code hashes and numerical tolerances |
| [Existing suite log](existing-suite.log), [integration output](integration-output.txt) | Actual 19-method rerun and exact source demo output |

The three project Python fences and sole companion Python fence are saved unchanged in a temporary directory. The review imports the exact library and exact companion helper, runs independent exercise checks, and then executes the combined source suite in a subprocess. The only modified implementation is a separate temporary AST mutant used for Exercise18. No manuscript correction was needed; the answers and recorded numeric claims aligned with the reviewed prompts.

Numerical expectations use exact Fraction accumulation, discount and nominal conversion relationships. The absolute1e-30 bound is selected for the stated fixed40-digit fixtures, not a universal monetary tolerance. Caller precision6/ROUND_DOWN/Inexact trap+flag are snapshotted completely and preserved by the exact project function. Annotations, mutable defaults and local rebinding are demonstrated in clearly separate small teaching probes; they are not mislabeled manuscript code. The complete docstring contract and reproduction reasoning are prose review; a passing docstring-presence predicate does not establish full documentation correctness or financial applicability.

Reproduce from the repository root: `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-03-exercise-review/review.py`. CPython3.12.14, Linux x86_64, standard library only; all checks passed on the initial run. No new source fences/methods or changes to manuscript code were introduced. Optional mypy is not rerun in this batch; its existing evidence remains separate.

Next: formal step review of Chapter3's nine standalone labs and Section3.13 testing lab, including prerequisites, expected outputs, context/validation behavior, documentation drift and static-checking instructions; then earlier section exercises and full project/checklist review. Independent mathematical/model/source/editorial acceptance, broader numerical domains and platform checks remain open. Earlier Book1 F28/F32 gaps remain open.
