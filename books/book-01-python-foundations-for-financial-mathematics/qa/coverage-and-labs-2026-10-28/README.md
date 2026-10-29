# Book 1 — V05/V06 execution mapping and uncovered workflows

**Latest checkpoint:** [All manuscript Python fences now have a selection or disposition](../later-examples-2026-10-28/README.md); zero remain unmapped. The counts below retain this report’s historical snapshot.

**Status: IN PROGRESS.** The 13 newly selected workflow checks passed on CPython 3.12.14 / Linux x86_64 with glibc 2.39. This is a bounded gap-closing run, not completion of V05/V06. Source revision: `a4aebd6d937a97dd5ed3f6b6cbb947fb5f58e76f`. Recorded 2026-10-28; reviewer/owner: Codex. No manuscript Python payload was changed.

**Follow-up:** The [Chapters 1–3 batch](../early-examples-2026-10-28/README.md) classified all 430 early gaps and reduced the current no-exact-mapping queue to 169 fences. Counts below retain this initial snapshot.

## Full manuscript selection ledger

The [ledger](coverage-ledger.json) inventories 1,160 Python fences in 356 chapter/companion/index Markdown documents, with source path, zero-based Python-fence index, opening line and SHA-256. QA documentation is excluded. The [chapter queue](CHAPTER-QUEUE.md) shows remaining mapping work.

| State | Fences | Meaning |
|---|---:|---|
| Historical selection unchanged | 543 | Selection identified from existing runner/results; current payload matches the source at the evidence publication commit byte-for-byte |
| New scoped workflow passed | 16 | Source fences included in this run's 13 passing workflows; some fences support multiple workflows |
| Context fragment | 2 | The previously identified `break`/`continue` examples require an enclosing loop |
| No exact execution mapping | 599 | No selection is established by this mapping pass; classify context/prerequisites and locate evidence or execute a suitable case |
| Total | 1,160 | Exhaustive inventory of explicit manuscript Python fences in the recorded snapshot |

Historical selection means source inclusion in a previously recorded run, **not** line, branch, input-domain or output coverage. A module imported by tests can have an unexecuted main guard. The 543 count therefore must not be presented as 543 fully validated standalone examples. Current equality to the evidence publication source establishes payload continuity; it does not independently authenticate every historical log. Known code changes were already part of those evidence commits; later prose and formula presentation changes do not alter these selected payloads.

The mapping uses explicit selected indices from Chapters 1–3 results; Chapter 4 suite/project selection; Chapter 5 file assembly configuration; Chapters 6–8 implementation/test selections; later section reference-suite selections and documented snippets; and Chapter 21's initial assembly. It deliberately does not credit overwritten early Chapter 21 `__init__` listings. Historical reproduction scripts, environment limits, failures and corrections remain in their original evidence directories. A block without a mapping is not necessarily executable, previously untested or defective. Definitions, intentional exceptions, dependent fragments and duplicated examples require individual disposition.

The [449 lab/exercise heading candidates](lab-review-queue.json) form a separate **step-and-answer review queue**. They are heading candidates, not 449 distinct labs or 449 failed checks. Executing code fences does not establish that every prose instruction, worked answer, external-data prerequisite or release-decision exercise has been completed.

## Newly checked workflows

| Workflow | Fixture / expected outcome | Actual result |
|---|---|---|
| 19.2 CSV reader | Manuscript's two-row synthetic price fixture; exact string-valued records | PASS |
| 19.2 CSV reader variant | Controlled UTF-8 BOM and quoted comma in instrument name | PASS; BOM removed and quoted field retained |
| 19.2 CSV writer | Exact ordered headers and one `EXAMPLE,101.50` record | PASS; output parsed back and checked |
| 19.4 Excel row inspection | Controlled `Prices` workbook; header and one USD price row | PASS; exact printed row tuples |
| 20.2 assertion example | Arithmetic assertion succeeds without output | PASS under ordinary, non-optimized Python |
| 20.6 Decimal construction | Exact decimal string versus binary-float conversion expansion | PASS; both output lines matched exactly |
| 20.11 annotated function | 100 to 105 returns approximately .05; annotations present | PASS; this is not static type checking |
| 20.15 example use | Assemble the exact `finlib` files; print `NPV: 4.132231` | PASS |
| 21.3 scaffold example | Assemble this section's exact package; print `PV: 100.00 payment units` | PASS |
| 21.3 scaffold tests | Run all 12 supplied tests against this section's exact package | PASS; no skips |
| 21.1 architecture main guard | Print `PV: 100.00 USD; model=pv-one-v1` | PASS |
| 21.2 requirements main guard | Print `Ready for review: False` for its not-run requirement | PASS |
| 21.16 metadata main guard | SHA-256 equals independently specified canonical example bytes | PASS |

All subprocesses exited zero; stderr was empty. Checks use only synthetic fixtures, no external financial data or service calls. Each subprocess has a 45-second timeout; the runner exits nonzero on a timeout, exit failure or oracle mismatch. Package examples run from separate temporary source directories with inherited Python path overrides removed. These are source-tree workflows, not installed-distribution acceptance. No graphical output was produced by this batch. The Excel workflow is row inspection, not workbook schema/financial validation.

[workflow-results.json](workflow-results.json) records commands, source and code hashes, source indices, outcomes and log paths. The matching stdout/stderr logs are retained under `logs/`. Fixture construction and explicit output/state oracles are in [run_gap_workflows.py](run_gap_workflows.py).

The existing **2,996 reference test-method total remains unchanged**. The 12 scaffold tests reproduce already-listed methods against an additional exact assembly; adding them again would double count curriculum tests. The 13 workflow cases and 16 source fences are different units and must not be added to the method total. This batch does not independently verify all 40 worked answers or all twelve lab steps in Section 20.15.

## F24 — scaffold execution evidence gap

**Severity:** Low (evidence/assembly gap). **Owner:** Codex. **Affected source:** Section 21.3 at the revision above. **State:** RESOLVED for this exact source-tree scaffold workflow; broader coverage remains open.

The initial Chapter 21 assembly writes the toolkit's time-value module from Section 21.5 and imports that package when it runs Section 21.3's tests. It does not assemble Section 21.3's exact package files or run its example-use block. Thus the initial 218-test evidence alone does not establish this particular scaffold workflow. Reproduce by inspecting [capstone-assembly.py](../initial-2026-10-27/capstone-assembly.py) and [standalone-assembly.py](../initial-2026-10-27/standalone-assembly.py). The new `toolkit-scaffold-example` and `toolkit-scaffold-tests` cases assemble Section 21.3 blocks 0/1 and execute blocks 2/3 with exact output and 12-test/no-skip checks. No algorithm correction or invalidation of the earlier integrated run is implied.

## Reproduction

Use the [V04 Python 3.12 requirements](../syntax-dependencies-2026-10-28/requirements.txt) in an isolated environment. From this evidence directory:

```bash
python run_gap_workflows.py ../.. /tmp/book1-gap-reproduction
python build_coverage_ledger.py /absolute/path/to/repository /tmp/book1-ledger-reproduction /tmp/book1-gap-reproduction/results.json
```

Choose new output directories. The ledger requires repository Git history, including each evidence directory's publication commit; a shallow checkout may need the corresponding history fetched. It verifies code continuity with `git show` and checks new-run payload hashes. Output identities are unique and every new-run source must map back to an inventoried fence. [Source-manifest hashes](source-manifest.json) bind the current manuscript snapshot; changing source requires affected checks to be repeated. Installed dependencies use the V04 environment: openpyxl 3.1.5 and markdown-it-py 4.0.0 are needed by this workflow/mapping batch. Other V04 scientific packages are not exercised here.

## Next work

Start with the **430 unmapped Chapter 1–3 fences**: classify complete programs, context-dependent snippets, definitions and expected-error demonstrations; establish suitable fixtures/oracles before execution. Then work through the remaining pandas/visualization, numerical/simulation and capstone mappings. Independently review lab steps and worked answers using the separate queue. Windows/macOS, notebooks, installed artifacts, external datasets and full supported-version behavior remain pending; source selection and ordinary execution do not establish financial/model acceptance.
