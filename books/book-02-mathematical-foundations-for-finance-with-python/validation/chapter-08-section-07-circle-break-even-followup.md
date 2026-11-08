# V-128 — Section8.7 circle/break-even numerical contracts

Candidate based on `7789936172ba8ca0545bc051eddee4f9ee08a3cd`. [Original eight-probe screen](chapter-08-section-07-circle-break-even-baseline.md) retained. [Expanded baseline](chapter-08-section-07-circle-break-even-baseline-expanded.json):113 passed/29 mismatches out of142. [Baseline replay](chapter-08-section-07-circle-break-even-baseline-expanded-replay.json) reproduces all142 observations identically. [Corrected](chapter-08-section-07-circle-break-even-corrected.json):142 passed/0 failed. Mismatches are predicates, not distinct defects or categories.

Circle oracle computes the complete radius²-x² square root at200/400 Decimal digits; final floats agree. Source instead forms exact rational (radius-x)(radius+x), then sqrt at100 Decimal digits; comparisons use rtol4e-15,atol0, with zero/sign checks exact. Cases include huge/tiny radii,positive/negative boundaries,adjacent boundary values,smallest subnormal,maximum finite radius and35 seeded inputs. It avoids intermediate radius/product range loss and boundary NaN, preserving domain/validation priority. Decimal backend is shared; selected precision agreement is not a correct-rounding proof or arithmetic-library certification.

Independent exact rational references derive q=k/gap and sensitivity=-k/gap² on complete represented inputs. Named vectors plus35 seeded tuples check signed-price/cost preservation,normal controls,complete range,finite-output ValueError,signed underflow and validation priority. A separate supplemental composition probe verifies that complete sensitivity does not require the quantity helper first; that probe establishes an explicit composition requirement rather than a prior promise violation. Finite-output exception conventions are also explicit policy adoption. No caller-context/resource/model acceptance is inferred.

```bash
python books/book-02-mathematical-foundations-for-finance-with-python/chapter-08/code/check_section_07_circle_break_even.py
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-circle-break-even-observer.txt . baseline-expanded 7789936172ba8ca0545bc051eddee4f9ee08a3cd
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-circle-break-even-observer.txt . baseline-expanded-replay 7789936172ba8ca0545bc051eddee4f9ee08a3cd
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-circle-break-even-observer.txt . corrected
python books/book-02-mathematical-foundations-for-finance-with-python/validation/chapter-08-section-07-circle-break-even-scope-runner.txt .
```

All50 Chapter8 Python files compiled and40 check/test scripts passed; exact50 source/check blobs verified before/after in [scope evidence](chapter-08-section-07-circle-break-even-scope.json). Actual stdout/stderr,Python/platform and fresh inventory are retained. Fresh inventory592 Python/379 scripts/593 required Python-fixture blobs is not a full runtime. [V-127](runtime-refresh-2026-11-08-r6.md) remains the latest full candidate Linux pass,at its earlier pin(591/378/592). No observer failure occurred in this batch.

Thirty-five selected COV categories remain partially addressed; none closed. Independent mathematical/editorial/platform/release/canonical acceptance,conditioning/branch/resource scope remain open. Next: Section8.7 bond price/derivative/reciprocal-yield sensitivity numerical/input/output contracts, then exposure/slope and centered copy. Book1 progresses separately.
