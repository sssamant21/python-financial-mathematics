# Chapter5 — Section5.1 local exercise review

Based on main `6bd4d4d5df47b662e743c4e7a4e5d50d5adb4ec8`. [Eight answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Results](results.json) · [Deliberate mutant](mutation.json)

CPython3.12.14 Linux: **nine command records passed their expectations**, plus **one source-restoration hash predicate passed**. Baseline and restored original suites each passed8 methods (16 invocations of8 existing methods). A separate deliberate mutated-copy run executed one existing method and failed as required. That nonzero raw failure is retained alongside corrected rerun; it is neither an unexpected manuscript defect nor another passing method. Historical unique-method/workflow totals unchanged.

Reproduce from repository root with standard library:

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-module-exercises/review.py
```

The runner reconstructs exact original core/runner/test listings into an owned temporary directory, records source/file hashes, then adds a clearly supplemental second caller. Two-runner input observations delegate to the original active_ids implementation and compare caller data without changing it. Original/reversed IDs and zero/fractional units use explicitly derived expectations; no amount arithmetic, valuation or independent numerical acceptance is implied.

Exercise3 moves the original display responsibility outside main while preserving ordinary script output; this makes quiet-import coverage substantively detect a problem rather than a NameError. Complete mutant text/hash and raw existing-test assertion failure are retained, then original bytes and full suite are restored. Exercise6 edits only a temporary core copy in one child process; cached import does not see saved changes but a fresh child does. Source bytes restored afterward. No repository manuscript source or running user notebook is edited.

All eight prompts have explicit answers. Two are design-only responses about maintenance and required valuation metadata. Main-guard reasoning and import-cache behavior are tied to executed demonstrations, while editor/notebook/platform follow-up remains unexecuted. New rejection/reversal assertions and second-runner behavior are supplemental checks, not new original unit-test methods or evidence of exhaustive side-effect isolation.

Together with project5.12-E2/E3,10 of96 local prompts now have scoped records;86 remain. Core12 workflow reviews and20 chapter-wide answers remain separate. No static checker, Windows/macOS, notebook/kernel, remote data or independent reviewer acceptance executed. F28/F32 remain open; F33 observer history remains retained.

Next: Section5.2 local exercises, then5.3 onward in queue order (skip already recorded5.12-E2/E3). Reassess source hashes before reusing this checkpoint.
