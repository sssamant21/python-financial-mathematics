# Book 1 — Initial QA Progress

**Status:** In progress; Book 1 is not comprehensively validated or certified.  
**Source snapshot:** `f429fb81b8d8f7d228100333c76019d583200d64`.  
**Run date:** 2026-10-27 UTC. The Chapter 21 runtime checks additionally include the Section 21.13 UTC-comparison fix published with this record.

## Scope and results

| Check | Observed result | Scope and limits |
|---|---|---|
| Locked manuscript inventory | 322/322 section numbers have matching manuscript files | Filename inventory only; not a content, title, link or completeness certification. |
| Markdown snapshot | 358 Book 1 Markdown files retrieved | Snapshot at the source revision above; other repository content was not inventoried. |
| Python syntax screening | 1,152 fenced Python blocks parsed; 0 syntax errors | AST parsing only; blocks may be fragments or depend on other blocks. Not runtime or mathematical validation. |
| Initial local-link heuristic | 10 candidates reviewed as notation false positives | Regex is not a full Markdown parser; links, anchors and external URLs remain to be comprehensively checked. |
| Chapter 21 reference suites | 218 tests passed, including 2 DST regression tests | Extracted source-tree teaching package and standalone examples; not installed-wheel, Windows, financial-model or complete Book 1 validation. |
| Chapter 20.14–20.16 | 36 reference tests passed | Extracted teaching examples only; other Chapter 20 sections remain outside this run. |
| One Chapter 21 chart | Rendered at 960×720 with Agg and visually inspected | Labels, timestamps and plotted points were visible in this example; this is not a full accessibility or visual audit. |

## Finding and correction

Section 21.13 compared aware datetimes directly. During a repeated daylight-saving hour, Python comparisons between datetimes with the same timezone object can compare wall times in a way that accepts a record whose actual availability instant precedes its observation instant. A reproduction using New York on 2025-11-02 accepted observation 06:15 UTC with availability 05:30 UTC. The reference implementation now compares UTC instants for record ordering, the cutoff and pair ordering, while preserving the original datetime fields. Two regression cases cover rejection of reversed availability and correct pair order across the repeated hour. The 218-test run includes those changes. IANA timezone data is required for the two tests.

## Environment and commands

- CPython 3.12.14; Linux 6.18.55 x86_64, glibc 2.39; Matplotlib 3.10.8; backend Agg.
- Chapter 21 examples were extracted from the pinned manuscript plus the Section 21.13 fix with [capstone-assembly.py](capstone-assembly.py) and [standalone-assembly.py](standalone-assembly.py). The scripts expect the pinned Book 1 snapshot under `qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/` in the current directory and write disposable files under `/tmp/book1_capstone`.
- From `/tmp/book1_capstone`: `PYTHONPATH=/tmp/book1_capstone/src:/tmp/book1_capstone MPLBACKEND=Agg python -m unittest discover -s tests -v`. Exit 0; [full output](capstone-tests.log).
- Chapter 20.14–20.16 examples were extracted with [chapter20-assembly.py](chapter20-assembly.py) from the same pinned snapshot. From `/tmp/book1_ch20`: `PYTHONPATH=/tmp/book1_ch20 python -m unittest discover -s tests -v`. Exit 0; [full output](chapter20-tests.log).
- The static scan used [static-audit.py](static-audit.py); it expects the same snapshot and writes a JSON result under `/tmp`. The link portion is heuristic and requires manual review.
- A synthetic Section 21.14 price chart was saved to a temporary local PNG and inspected. The chart and its source data are not retained in this repository; no assertion of a full visual review is made.

## Outstanding work

Runtime checks for the remaining sections, independent mathematical and source review, edge-case analysis, clean-wheel and platform checks, comprehensive links and references, copyright and editorial review, accessibility review, and review of the historical claims in the indexes remain pending. A failed or skipped check must retain its actual status and reason. Re-run affected checks when source, environment or scope changes. No canonical or production approval is implied by this progress record.
