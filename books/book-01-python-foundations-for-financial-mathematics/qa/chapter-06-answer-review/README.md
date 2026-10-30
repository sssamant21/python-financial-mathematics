# Chapter6 — chapter-wide answer review

Based on main `ddb839244c0831b8595dcebe709b4d88316290c4`. [20 answers](ANSWERS.md) · [Prompt/alignment register](answer-register.json) · [Runner](review.py) · [Results/benchmarks](results.json) · [Exact-source local observations](observed-locals.json) · [128 local exercise queue](section-exercise-queue.json) · [16 formal workflow queue](workflow-queue.json) · [F35 initial failure/correction](FAILURE-AND-RERUN.md)

CPython3.12.14,NumPy2.3.5,Linux: **45 predicates and2 command records passed**. Corrected exact companion source runs20 existing methods through documented explicit discovery, then the supplemental observer reruns the same20 methods. Thus40 corrected method invocations of20 existing unique methods; the initial20-method pass is separate retained history. No new historical unique methods or supplemental workflow cases are added. Compilation is a separate predicate; no timing/performance benchmark was run.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-answer-review/review.py
```

The runner reconstructs the exact current code fence unchanged in an owned numpy_lab_617 directory and uses the documented custom discovery pattern. The observer traces local values from that same listing without rewriting it; no execution or timing equivalence beyond the specific regression observations is asserted under tracing. Large payload data is omitted from local snapshots while shape/dtype/nbytes remain. Standalone source suite, trace rerun, independently derived Fraction/precision80 Decimal benchmarks, supplemental fresh-copy/shape demonstrations and conceptual answers are distinguished in the answers/results.

Known expectations include signed P&L50/20/0, exact discounted-flow Fraction, linked-1%, opening weighted4.5%, scenario/portfolio matrix, exact2x2 solution, high-precision tiny linked changes, payload160000bytes and holdings reconciliation. Explicit tolerances apply after shape/finite checks; a1e-12 absolute threshold is not reused for tiny1e-17 results. Random same-protocol repetition is not independent statistical or cross-platform validation.

F35 corrects one substantive prompt omission: Problem18 now supplies callable Python/NumPy list-to-list functions with actual known-answer/list-return and unequal-length checks. The unchanged number of unittest methods must not be interpreted as no changed checks. Original source/alignment failure and corrected rerun are retained; the current source-fence ledger hash is updated with prior payload evidence preserved.

All20 chapter-wide answers have scoped records. At this answer-batch baseline,16 core workflows and128 local exercise/project-extension prompts were inventoried as pending. Follow the linked queues for current status. Section6.16 project/checklist work is separate from these answers. No fresh NumPy install, static checking, Windows/macOS, notebook/server, remote data, production, comprehensive financial review or independent acceptance. F28/F32 remain open; F33/F34 histories retained. Next: Sections6.1–6.4 formal workflow review, then remaining workflows/local prompts/project scope.

Earlier checkpoint: [Sections6.1–6.4 workflow review](../chapter-06-early-lab-review/README.md) records4 scoped workflows,13 command checks and36 predicates.12 workflows and128 local prompts remain pending. Next:Sections6.5–6.8; initial answer records/results are unchanged.

Earlier checkpoint: [Sections6.5–6.8 workflow review](../chapter-06-middle-lab-review/README.md) adds4 scoped workflows,13 command checks,51 predicates and32 existing methods rerun.8 of16 workflows recorded;8 workflows/128 local prompts remain. Next:Sections6.9–6.12.

Earlier checkpoint: [Sections6.9–6.12workflow review](../chapter-06-later-lab-review/README.md) adds4scoped workflows,13commands,50predicates and32existing methods.12of16workflows recorded;4workflows/128local prompts remain. Next:Sections6.13–6.16 and project/checklist review.

Earlier checkpoint: [Sections6.13–6.16/project review](../chapter-06-final-workflow-review/README.md) records14commands,66predicates,32existingmethods and20separateprojectrecords. All16coreworkflows scoped;128localprompts pending. Next:Section6.1localexercises.

Earlier checkpoint: [Section 6.1 local exercises](../chapter-06-motivation-exercises/README.md) now records eight answers, three command checks, 23 predicates and eight existing methods rerun. Local queue: 8/128 reviewed, 120 pending. All 16 core workflows remain separate. Next: Section 6.2 local exercises.

Earlier checkpoint: [Section 6.2 local exercises](../chapter-06-snapshot-exercises/README.md) records eight answers, three commands, 20 predicates and eight existing methods rerun. Local queue: 16/128 reviewed, 112 pending. Next: Section 6.3.

Earlier checkpoint: [Section 6.3 local exercises](../chapter-06-creation-exercises/README.md) records eight answers, three commands, 29 predicates and eight existing methods rerun. Local queue: 24/128 reviewed, 104 pending. Next: Section 6.4.

Earlier checkpoint: [Section 6.4 local exercises](../chapter-06-indexing-exercises/README.md) records eight answers, two command checks, 29 predicates and eight existing methods rerun. Local queue: 32/128 reviewed, 96 pending. Next: Section 6.5.

Earlier checkpoint: [Section 6.5 local exercises](../chapter-06-vectorized-exercises/README.md) records eight answers, two command checks, 29 predicates and eight existing methods rerun. Local queue: 40/128 reviewed, 88 pending. Next: Section 6.6.

Earlier checkpoint: [Section 6.6 local exercises](../chapter-06-broadcasting-exercises/README.md) records eight answers, two command checks, 29 predicates and eight existing methods rerun. Local queue: 48/128 reviewed, 80 pending. Next: Section 6.7.

Earlier checkpoint: [Section 6.7 local exercises](../chapter-06-aggregation-exercises/README.md) records eight answers, two final command checks and 27 final predicates. Eight existing methods passed in each of two runs; initial QA variance-constant failure/corrected rerun retained under F36. Local queue: 56/128 reviewed, 72 pending. Next: Section 6.8.

Earlier checkpoint: [Section 6.8 local exercises](../chapter-06-cashflow-exercises/README.md) records eight answers, two command checks, 24 predicates and eight existing methods rerun. Local queue: 64/128 reviewed, 64 pending. Next: Section 6.9.

Earlier checkpoint: [Section 6.9 local exercises](../chapter-06-return-exercises/README.md) records eight answers, two command checks, 25 predicates and eight existing methods rerun. Local queue: 72/128 reviewed, 56 pending. Next: Section 6.10.

Earlier checkpoint: [Section 6.10 local exercises](../chapter-06-weight-exercises/README.md) records eight answers, two command checks, 32 predicates and eight existing methods rerun. Local queue: 80/128 reviewed, 48 pending. Next: Section 6.11.

Earlier checkpoint: [Section 6.11 local exercises](../chapter-06-matrix-exercises/README.md) records eight answers, two command checks, 23 predicates and eight existing methods rerun. Local queue: 88/128 reviewed, 40 pending. Next: Section 6.12.

Earlier checkpoint: [Section 6.12 local exercises](../chapter-06-linear-exercises/README.md) records eight answers, two final command checks, 29 final predicates and eight existing methods in the retained run. Local queue: 96/128 reviewed, 32 pending. Next: Section 6.13.

Earlier checkpoint: [Section 6.13 local exercises](../chapter-06-random-exercises/README.md) records eight answers, two command checks, 23 predicates and eight existing methods rerun. Saved innovations/replay manifest retained; E7/E8 conceptual only. Local queue: 104/128 reviewed, 24 pending. Next: Section 6.14.

Earlier checkpoint: [Section 6.14 local exercises](../chapter-06-precision-exercises/README.md) records eight answers, two command checks, 24 predicates and eight existing methods rerun. Local queue: 112/128 reviewed, 16 pending. Next: Section 6.15.

Current checkpoint: [Section 6.15 local exercises](../chapter-06-performance-exercises/README.md) records eight answers, two command checks, 24 predicates and eight existing methods rerun. Original/supplemental timing and full local profile evidence retained; peak-memory design unexecuted. Local queue: 120/128 reviewed, 8 pending. Next: Section 6.16 project extensions.
