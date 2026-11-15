# Section20.16 exercise and lab review

Source based on `b0b66bee70c7e9156590b4ea17e0ec73caeaf621`. Exact executable fences unchanged:one exercise reference and four project fences. The12 exercise methods test the one-period teaching function;the12 project methods test finlib. These are24 existing unique methods/72invocations across three runs each,zero new historical unique methods. Keep separate from28 source predicates,three supplemental arithmetic demonstrations,40 exercise records and12 lab-step records.

Run `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-20-exercises-review/review.py [source_revision]` from repository root. It stages exact fences in a temporary directory and captures eight commands/stdout/stderr. [Baseline](baseline.json),[actual replay](baseline-replay.json),[current](results.json) all pass;no initial source failure or correction invented. Use `review.py <revision>` for an earlier source;it writes baseline.json,so preserve historical evidence before rerunning in this directory.

[40 prompt/answer records](answer-records.json) and[12 lab contracts](lab-step-records.json) distinguish executed claims from conceptual/design review. Independent rational expectations:110/(11/10)=100;two-period NPV500/121;95/(19/20)=100;two-year break-even0. Monetary near-zero checks use published illustrative abs1e-10;other magnitudes use scoped tolerances in JSON. Monthly conversion and Decimal/float representation demonstrations are supplemental,not project implementation execution.

Release recommendation:HOLD. No installed artifact,external reviewer,model suitability,all-range correctness or supported-platform acceptance. Retain project Horner range limit,20.11 static-checker gap,F28/F32/F209,F165tail/F185integration and other tracker findings. Next:21.1 Capstone Architecture formal workflow/answer review;Chapter20 broader acceptance remains open.

Executed source pinned to `9ebd2355077d8c7e8b9348b8f44eb78f57017402`;[source verification](publication-verification.json).
