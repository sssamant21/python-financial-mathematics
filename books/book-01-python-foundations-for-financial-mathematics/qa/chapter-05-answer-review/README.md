# Chapter 5 — chapter-wide worked-answer review

Based on main `29db9a61` (full revision in source repository history). All20 Section5.13 prompts have scoped answer/alignment records. [Answers](ANSWERS.md) · [Register](answer-register.json) · [Runner](review.py) · [Results](results.json) · [96 pending section exercises](section-exercise-queue.json) · [12 pending formal workflow records](workflow-queue.json)

CPython3.12.14 Linux: **29 source/oracle predicates passed**. Exact regular-wheel verifier rerun: base8 methods and extended12 methods passed with no skips. These are20 invocations of12 existing installed methods, not20 distinct methods; no historical unique-method/workflow totals change. The final integrated driver logs and source hashes are retained. A successful preliminary run using the existing packaging driver is retained under [preflight](preflight/results.json), separately from final evidence; it repeats the same8/12 methods and adds no unique coverage. No runtime-test failures or manuscript corrections occurred. An initial queue-generation filename parse error was corrected before publication; [error and rerun note](generation-note.md) retained.

[Base log](base.log) · [Extended log](extended.log) · [Driver transcript](installed-driver.log) · [Builder evidence](builder-evidence.json) · [Builder install](builder-install.log)

Reproduce from repository root after preparing the exact builder with the [existing provenance-checked preparation workflow](../chapter-05-runtime/backend-resolution/README.md):

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-05-answer-review/review.py --builder /path/to/builder/bin/python
```

Without --builder the runner explicitly records installed checks NOT_RUN; source probes alone are not installed acceptance. Source extraction uses unchanged core and configuration fences; the installed driver assembles unchanged project listings and applies only the companion-prescribed class insertion and success-message update. It checks actual8/12 unittest discovery, regular-wheel fresh installation, external -I origin, CLI parity, invalid args, pip check and temporary cleanup. Source and selected-code hashes bind evidence to reviewed inputs.

Builder: pip25.0.1, setuptools84.0.0, Python3.12.14. Backend wheel SHA256 matched separately fetched version-specific PyPI metadata; only this preparation used external download/metadata access. Subsequent project build/install used published offline options. Temporary package wheels/runtimes are removed; no retained-wheel recipient handoff or reproducible-build identity is claimed. Base/extended wheel hashes differ and are recorded, not asserted equal.

Numerical expectation: independent Fraction/integer-cent ties-to-even logic gives sum-then-round30.01 and round-each-then-sum30.00 for10.005+20.005. Eight fixture comparisons cover even/odd half-cent ties, zero, four-place amounts, a carry to1000000, and1000 maximum-sized rows. Full bounds justify fresh precision28 for addition/quantization; source rejects1001 rows and1000000.0001. Hostile caller precision2, rounding and trap/flags remain unchanged. Configuration source executes the all-layer precedence example and rejects a present empty environment setting.

Completion checklist: all20 answers recorded; all four companion extension methods discovered; known total independently checked; origin and actual count inspected; no failures hidden; Linux only recorded. The educational100-point rubric has not been assigned by an independent grader. Conceptual identity, authorization, release and research claims are design reviews, not remote/security/financial certification.

Remaining: formal step/prerequisite/checklist review for Sections5.1–5.12,96 local extension prompts, retained-wheel handoff/source-distribution/platform work and independent acceptance. Existing F28 notebook/platform and F32 shared-input gaps remain open. Next batch: Sections5.1–5.5 formal module/package lab-step review, then continue remaining labs/exercises. Do not repeat the20 answers unless source hashes change.
