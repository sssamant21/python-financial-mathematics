# V-237 — Section10.4 complete linear-PV composition

Baseline: `31f4962bb9efee1a6e09d65c72a59187f0ce14c4`. [Runnable review](review.txt), [baseline](baseline.json), [baseline replay](baseline-replay.json), [corrected](first.json), [replay](replay.json), [moment support](moment-support.json), [kernel support](kernel-support.json), [Chapter10 support](chapter-support.json), [full-runtime delta](runtime-delta.json). Corresponding support .txt runners are retained and preserve their original baseline pins.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-complete-pv-2026-11-21/review.txt baseline --baseline
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-complete-pv-2026-11-21/review.txt first
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-complete-pv-2026-11-21/review.txt replay
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-complete-pv-2026-11-21/moment-support.txt moment-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-complete-pv-2026-11-21/kernel-support.txt kernel-support
python books/book-02-mathematical-foundations-for-finance-with-python/validation/ch10-complete-pv-2026-11-21/chapter-support.txt chapter-support --chapter
```

Baseline/replay retain **fourteen passes/seven failed predicates** for complete signed cancellation, zero coefficients paired with unreportable components, finite coefficient-scaled growing streams and exact leading-exponential cancellation. These selected complete-expression range extensions are not seven independent financial-model bugs. Both corrected runs pass **21 predicates** identically, including true final overflow, zero-horizon validation, signed PV, tiny/minimum rates and allowed final underflow.

The source validates all inputs first. Zero stream/horizon returns zero; zero rate combines exact represented aT+bT²/2. Otherwise it forms exact rational N0=ar+b and N1=N0+brT, then evaluates (N0−N1 exp(−rT))/r² before one float report. An exactly zero N1 is reported before exponent guards. This preserves ∫0^6000(−11999+2t)exp(2t)dt=6000: the antiderivative(t−6000)exp(2t) has an exactly zero upper coefficient, even though both separately reported components overflow.

Moderate exponent evaluation uses a fresh2000-digit context. For rT>10000, the omitted term has magnitude below2^3174 exp(−10000), far below binary64 reporting scale. For rT<−10000 and nonzero N1, binary64 rational products imply |N1/r²|>2^-5270 while |N0/r²|<2^3173; the exponential term exceeds any possible compensation and the final value is rejected. Exactly zero N1 is handled first. True final overflow→ValueError, final underflow0 permitted. Cutoffs/context/selected predicates do not prove universal correct rounding, especially at reporting ties, or resource/model acceptance.

Independent expectations integrate the combined linear rate's exponential power series termwise using800-digit direct powers/factorials and exact rational coefficients; they do not call source component reports or the source exponential closed form. Three unchanged-term checks avoid treating an isolated zero coefficient as convergence. Zero-rate and zero-stream cases use exact identities; the high-exponent cancellation uses the explicit antiderivative above. Strong-discount references use the rational Laplace limit only where the omitted term is below reporting scale. Arithmetic comparisons use rtol5e-14/atol0; exception/zero checks exact.

Each scoped run executes CLI, strengthened checker and compilation (three commands). Seven native regressions are added. Prior37 moment and55 kernel/report predicates pass, including ordinary report fields and false certification/reviewer flags. Chapter support passes33 earlier predicates, compiles/verifies21 Python files and executes11 checkers/10CLI labs (22 commands). Candidate Git blob SHA/SHA256 identify the tested source/checker; baseline commit does not contain fixes. Existing exercise/lab records remain distinct from new predicates.

**Section10.4 remains in progress.** Next:midpoint finite-grid/zero-width/preflight/callback/complete-sum contracts and assessment reporting ranges, then full pinned runtime refresh before10.5. Their implementations are unchanged. Latest full is V234 at7e98df4194191241042e19c5dba66873a8b4a852. Fresh642/429/643 inventory;641 of643 required blobs match, only10.4 source/checker differ. Only direct importer is the companion checker, which passes with the Chapter10 support run. No new full-book runtime or section/book completion is claimed.

All38 selected COV categories remain partial, none closed. Broader numerical/resource/provenance/model/supported-platform/release/independent/canonical acceptance stays open. Book1 has separate trackers.
