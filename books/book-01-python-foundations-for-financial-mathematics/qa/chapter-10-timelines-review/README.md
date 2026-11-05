# Section10.2 — Cash-flow timelines lab and local-answer review

Baseline `329a968bb391865dfd65d662a759f3dcb858c7be`. [Runner](review.py) · [Initial failures](initial-results.json) · [Corrected results](results.json) · [Ten answer records](ANSWERS.md).

**One core workflow and ten local prompts scoped; two documented commands,26 supplemental predicates and ten existing methods passed after F52/F53 correction.** The single Python listing was extracted verbatim as cash_flow_timelines.py, executed and compiled in an isolated temporary directory. Initial two commands and ten existing methods passed, while six of25 supplemental predicates failed. The final run adds a nonzero reordering fixture with all six permutations; its aggregate is one predicate, not six workflows or tests. Regression assertions were added to the existing validation method; no historical unique methods were added.

F52 (medium numerical/instructional severity; owner manuscript maintainer/QA executor): a distant nonzero flow at an extreme valid positive quote lost its factor to zero; a smallest positive float amount at one year and100% EAR lost its PV to zero. Both returned0 silently. Discount factor and nonzero PV underflow are now rejected explicitly. Overflow is normalized to a validation error; exhaustive range support is not claimed. Two initial failures and corrected rejection are retained.

F53 (medium input-contract severity; same owner): empty input bypassed origin and basis validation (two probes), while datetime timestamps were admitted by date subclass checks and a twelve-hour interval became zero through timedelta.days (two probes). The API now explicitly requires calendar dates, rejects datetime, and validates origin/basis before event traversal even for empty schedules. Four initial failures and corrected rejection are retained. All six regression cases are within the existing test_10_validation method. Reproduce initial failures with the runner against the baseline source at the same relative path; the added permutation case also passes baseline.

Save/run/compile steps, exact filename and self-contained imports hold. Prepared Linux CPython3.12.14, standard library only; no prior module/data/network dependency. Exact integer day counts and Fractions independently derive year fractions, annual PV and NPV. Decimal at precision100 independently derives actual leap-year and ACT/360 valuations, rather than assuming a calendar anniversary is always one model year. Labels and same-date rows remain separate in the stable schedule. Prompt10's traceability rationale is conceptual; retention is directly inspected in source objects.

No date settlement, holiday/business-day adjustment, ACT/ACT,30/360, intraday/timezone scheduling, fixed-point currency, fresh installation, Windows or notebook workflow is executed. Source math-rendering/editorial acceptance remains separate. F28/F32, platform and independent acceptance remain open. The Python source has scoped numerical/validation fixes; no financial certification is implied.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-10-timelines-review/review.py
```

Next: Section10.3 formal lab and local answers.
