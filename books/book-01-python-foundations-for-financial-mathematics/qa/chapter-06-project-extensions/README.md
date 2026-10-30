# Chapter 6 — Section 6.16 project extensions

Based on main `09e9d92f60041c64d51d58c8118651ae45c3bc9b`. [Eight answers](ANSWERS.md) · [Prompt/hash register](answer-register.json) · [Runner](review.py) · [Supplemental implementations](extensions.py) · [Results](results.json) · [Timings](timings.json) · [Tiny-change diagnostic](tiny-change.json)

CPython 3.12.14, NumPy 2.3.5, Linux shared host: **3 original command checks and 43 predicates passed** on the first run; eight original methods passed once. No unexpected failure or manuscript change. Exercise records, predicates, commands, extension implementations, formal workflows and historical unique methods remain separate; overlapping reruns add no historical unique methods or workflow cases.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-project-extensions/review.py
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-06-project-extensions/audit_queue.py
```

The runner reconstructs unchanged portfolio.py/test_portfolio.py inside a temporary numpy_lab_616 folder and executes all three documented commands from its parent: demo, discovery and compileall. Source/listing hashes and byte equality identify what ran. Dataclass module registration is preserved during in-process exact-source calls. The separate [queue audit](queue-audit.json) checks metadata/links/hashes; it is not a fourth manuscript command or a rerun of earlier chapters/sections.

Supplemental helpers implement percentage-point rendering, named-row lookup, mapping/pair price alignment, batch portfolios, explicit distributions and a validated-once resident snapshot. Independent hand/rational expectations verify supplied cash quotes, batch outcomes, updated distribution/valuation routes and tiny changes. Return/value comparisons use rtol/atol 1e−12 only for controlled moderate fixtures. Duplicate wire IDs are observable only before an ordinary dict discards them; the pair adapter demonstrates that boundary and rejects raw Boolean mixtures, but does not resolve all ingestion or shared-input gaps.

Timings compare repeated original validated/copying calls with a separately prevalidated owned resident snapshot, preserving common Report output representation but different setup/validation boundaries. Raw five-sample, 20-call records are retained without speed assertions. No peak-memory, isolated hardware or production claim is made. The tiny-change record explicitly retains direct P&L 8 versus return reconstruction 6.661338147750939 and exact expected 6; this is a documented extreme-scale accuracy limitation, not certification or a universal formula ranking.

**All 128 Chapter 6 local prompts now have scoped review records.** All 16 core workflows, 20 chapter-wide answers and 20 separate project checklist/equation/axis records remain separately counted. This closes the listed Chapter 6 formal review queue, not comprehensive chapter validation. Earlier conceptual-only statistical, peak-memory, time-path and other designs remain unexecuted implementations/acceptance limits. Existing method totals, source-fence mappings and historical failure evidence are unchanged.

Preinstalled environment reuse is scoped. Fresh setup, Windows/macOS, notebooks, concurrency/transactional snapshots, general arbitrary-wire/schema and monetary precision, entitlement/FX/financing integration, independent financial/statistical review and final acceptance remain unexecuted. F28/F32 and F33–F36 history remain intact; original mixed-Boolean/numeric source preconditions are not silently closed by the new one-vector adapter. Next: **Chapter 7 Section 7.18 chapter-wide worked-answer and companion alignment review**, then its formal workflows/local queue.
