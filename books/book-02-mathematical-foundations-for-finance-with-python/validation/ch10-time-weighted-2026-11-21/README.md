# V-236 — Section10.4 phi and scaled time-weighted moment

Baseline: `6673f03dc6d20f4fcb9c01c34e7878b84addfc6d`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](first.json), [replay](replay.json), [kernel support](kernel-support.json), [kernel runner](kernel-support.txt), [Chapter10 support](chapter-support.json), [chapter runner](chapter-support.txt), [full-runtime delta](runtime-delta.json).

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-time-weighted-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-time-weighted-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-time-weighted-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-time-weighted-2026-11-21/kernel-support.txt kernel-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-time-weighted-2026-11-21/chapter-support.txt chapter-support --chapter
```

Both baseline runs retain **28 passes/nine failed predicates**: two finite negative-phi reports, selected finite/underflow scaled moments despite intermediate exponent/horizon²/phi overflow, and final-overflow exception normalization. These predicates are not nine independent financial-model defects. Finite-result range extensions are explicit. Both corrected runs pass **37 predicates** identically: fifteen phi cases (including both sides of the.1 series boundary), sixteen scaled-time cases, and six exception/input cases.

Source phi uses a fresh800-digit context: a near-zero moment recurrence until the context stops changing, otherwise a high-precision closed form. Time-weighted integration forms exact represented rate×horizon and horizon² and retains the moment internally until the complete product reports. It can return1 for rate1/horizon1e200 or a finite tiny value for rate−1e308/horizon1e−305 even though an intermediate float square or standalone moment is unreportable. True final overflow raises ValueError; final underflow0 remains allowed; no signed-zero or universal correct-rounding/resource guarantee is added.

Positive x>10000 uses exact1/x² before Decimal reporting, omitting the numerator term(1+x)exp(−x), bounded by10001exp(−10000). For x=−u<−10000, phi(−u)≥exp(u/2)/4; even the smallest nonzero binary64 horizon²≥2^-2148 cannot compensate that into finite binary64 range. This unscaled/scaled rejection does not settle cancellation or coefficient compensation in a complete linear PV, which remains unfinished.

The independent oracle integrates the exponential power series termwise on[0,1] using800-digit direct power/factorial terms divided by k+2. It does not call Decimal.exp, source phi, or the source moment recurrence. For positive x>1000 it uses the1/x² asymptote with omitted relative tail below approximately1001exp(−1000), far below the stated tolerance. Signed/scaled moment references combine exact represented inputs before float conversion. Arithmetic comparisons use rtol5e-14/atol0; exceptions/zero checks exact. Boundary/near-zero behavior is selected numerical evidence, not a proof across all floats.

Each scoped run executes full CLI, strengthened native checker and compilation (three commands). Nine regressions extend the existing checker. Prior kernel/report55 predicates pass (all ordinary report fields and false certification/reviewer flags retained). Chapter support passes33 earlier predicates, compiles/verifies21 Python files and executes11 checkers/10CLI labs (22 commands). Copied runners preserve their original baseline pins deliberately. Candidate Git blob SHA/SHA256 identities identify the tested source/checker; baseline pin does not contain fixes.

Earlier six lab-review units/fourteen exercises remain separate from new predicates. **Section10.4 remains in progress.** Next: complete linear-PV coefficient/cancellation contracts, midpoint grid/callback and assessment reporting ranges, then full pinned runtime refresh before10.5. Those implementations are unchanged; component reports are not independent oracles for full composition. Latest full run is V234 at7e98df4194191241042e19c5dba66873a8b4a852. Fresh inventory642/429/643;641 of643 required blobs match, only10.4 source/checker differ. No new full-book runtime or section/book completion is claimed.

All38 selected COV categories remain partial, none closed; broader numerical/resource/provenance/model/supported-platform/release/independent/canonical acceptance remains open. Book1 has separate trackers.
