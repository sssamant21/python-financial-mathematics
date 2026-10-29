# V06 — Chapter4 chapter-wide exercise review

Date:2026-10-29. Baseline:`3e185649bf53f5a72ad9e1869d17762110444a26`.

**PASS(scoped):all20 Section4.14 answers reviewed;48 predicates passed, zero failed.** The exact project/companion suite also passed23 existing methods (10 project+13 companion). These reruns add zero unique methods; predicate, method and exercise counts are separate. No full Chapter4 completion percentage is asserted.

[Answers](ANSWERS.md) · [Hashed register](answer-register.json) · [Runner](review.py) · [Actual outputs/results](results.json) · [Next heading queue](next-review-queue.json)

The complete project module and sole companion implementation fence are extracted unchanged into a temporary directory. The review executes the original functions and runs their source suites in a fresh subprocess. Independently specified expected structures/order/counts avoid defining expected output by a second call to the same implementation. Quantities are units, not prices/values; no financial discounting, FX or lot aggregation is claimed.

Fixtures cover zero/fractional quantities, inclusive thresholds, reversed report order, empty inputs, duplicates, invalid final rows even when no subset qualifies, fresh record dictionaries, retained scalar snapshot/membership, same-day signed/zero events, duplicate event IDs across dates, exact date versus datetime, full unused-catalog validation, stored-zero lookup and theS0→S3 command sequence. Exact reference test19 covers all six requested rejection cases with baseline preservation. Conceptual Exercises1/5/6/14/15/20 are prose reviews, not additional automated tests. Source hashes bind the reviewed answers/code; no original numerical or representation defect was identified in this batch.

Reproduce: `python books/book-01-python-foundations-for-financial-mathematics/qa/chapter-04-exercise-review/review.py` from repository root. CPython3.12.14 Linux x86_64, standard library only. All48 checks and the existing23-method suite passed on the first run. Static typing was not rerun in this batch; earlier evidence is separate. Manuscript and Python fences remain unchanged.

Limits:full numerical/magnitude/input/branch/platform coverage and independent financial/model/editorial/source acceptance remain open. Currency/lot/calendar/price/concurrency/persistence concepts are contracts or future designs, not implemented production assurances. Book1 F28 notebook/platform and F32 shared-input integration gaps remain open.

Next:Chapter4 formal lab-step review, then earlier section exercises and full Section4.13 requirements/checklists/extensions. The heading discovery queue is only a candidate list, not evidence those tasks are complete.
