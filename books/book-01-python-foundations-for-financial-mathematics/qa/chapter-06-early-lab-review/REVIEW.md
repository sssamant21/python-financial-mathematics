# Sections6.1–6.4 — formal prerequisite/step/contract review

These are4 workflows with8 derived review units each,not32 labs. Setup is PARTIAL because this run reuses the recorded installed runtime; semantic contract rows are conceptual reviews,not platform or financial acceptance. Local exercise prompts remain in their separate pending queue even if an overlapping behavior was probed here.

## 6.1

**6.1-SETUP — PARTIAL**

Selected interpreter and NumPy origin/version recorded. Reused preinstalled3.12.14/2.3.5; fresh venv/index installation and platform shell routes not executed.

**6.1-FILES — PASS_SCOPED**

Reconstructed exact two source/test listings as documented sibling filenames in a separate owned temporary lab; all source and listing hashes retained; no path edits.

**6.1-COMPILE — PASS_SCOPED**

Both exact file payloads compile under selected interpreter. No static type-checker inference.

**6.1-IMPORT — PASS_SCOPED**

Fresh child module import has exactly empty stdout/stderr. This is quiet-import evidence,not application file-access instrumentation or OS sandboxing.

**6.1-APPLICATION — PASS_SCOPED**

Exact original main ran; full stdout matches documented expected text including ordering/format/newlines and stderr empty. Independently derived API/attribute/selection checks supply another oracle.

**6.1-REFERENCE — PASS_SCOPED**

Exact original test discovery ran8 existing methods with no skip/failure/error; raw stderr/stdout retained. Existing methods not added again to historical unique totals.

**6.1-API — PASS_SCOPED**

Fraction ratios5%,-5%,0; zero-end-100%; result shape/dtype/new storage; unchanged input bytes; overflow failure/error-policy restoration; documented underflow-100%; mismatched shape rejected.

**6.1-SEMANTICS — REVIEWED_CONCEPTUAL**

Inputs are aligned price observations sharing currency/per-unit convention and interval. Positive starts/nonnegative ends; end0 is a valid total price loss, missing is not zero. Binary ratios exclude dividends/fees/FX/annualization. Underflow may collapse a tiny positive ratio to0 and return-1; finite operands can overflow. Equal shapes do not establish instrument identity; tolerance is illustrative,not materiality.

## 6.2

**6.2-SETUP — PARTIAL**

Selected interpreter and NumPy origin/version recorded. Reused preinstalled3.12.14/2.3.5; fresh venv/index installation and platform shell routes not executed.

**6.2-FILES — PASS_SCOPED**

Reconstructed exact two source/test listings as documented sibling filenames in a separate owned temporary lab; all source and listing hashes retained; no path edits.

**6.2-COMPILE — PASS_SCOPED**

Both exact file payloads compile under selected interpreter. No static type-checker inference.

**6.2-IMPORT — PASS_SCOPED**

Fresh child module import has exactly empty stdout/stderr. This is quiet-import evidence,not application file-access instrumentation or OS sandboxing.

**6.2-APPLICATION — PASS_SCOPED**

Exact original main ran; full stdout matches documented expected text including ordering/format/newlines and stderr empty. Independently derived API/attribute/selection checks supply another oracle.

**6.2-REFERENCE — PASS_SCOPED**

Exact original test discovery ran8 existing methods with no skip/failure/error; raw stderr/stdout retained. Existing methods not added again to historical unique totals.

**6.2-API — PASS_SCOPED**

Independent shape/size/payload calculation2*3*8=48; result edits do not change source; transposed read-only input becomes independent writable C-order copy; original writeability preserved; exact copied values; duplicate dates rejected.

**6.2-SEMANTICS — REVIEWED_CONCEPTUAL**

Axes date then instrument; exact immutable label tuples have matching lengths/unique unpadded text. Labels are not date-parsed, chronologically verified or authenticated. Writable C-order numeric copy gives independence from later ordinary mutations,not immutability or transactional concurrent capture. Stored zero is allowed even though downstream denominator APIs differ;48bytes is payload,not process memory.

## 6.3

**6.3-SETUP — PARTIAL**

Selected interpreter and NumPy origin/version recorded. Reused preinstalled3.12.14/2.3.5; fresh venv/index installation and platform shell routes not executed.

**6.3-FILES — PASS_SCOPED**

Reconstructed exact two source/test listings as documented sibling filenames in a separate owned temporary lab; all source and listing hashes retained; no path edits.

**6.3-COMPILE — PASS_SCOPED**

Both exact file payloads compile under selected interpreter. No static type-checker inference.

**6.3-IMPORT — PASS_SCOPED**

Fresh child module import has exactly empty stdout/stderr. This is quiet-import evidence,not application file-access instrumentation or OS sandboxing.

**6.3-APPLICATION — PASS_SCOPED**

Exact original main ran; full stdout matches documented expected text including ordering/format/newlines and stderr empty. Independently derived API/attribute/selection checks supply another oracle.

**6.3-REFERENCE — PASS_SCOPED**

Exact original test discovery ran8 existing methods with no skip/failure/error; raw stderr/stdout retained. Existing methods not added again to historical unique totals.

**6.3-API — PASS_SCOPED**

Rates1/100,1/40,1/25; independently derived grid-1/100+i/200; fifteen uncomputed NaNs and false flags; integer periods1..4 and neutral factors; independent arrays across calls; boolean wire rejection; truncation and16777217->16777216 float32 loss.

**6.3-SEMANTICS — REVIEWED_CONCEPTUAL**

Rates are decimal fractions; shifts are additive percentage points. Exact wire text validated before float conversion; bounds[-1,1],six fractional digits,1..1000 items,negative zero numerical0. Periods are abstract indices,not dates. NaN/false marks unfinished workspace; it is not a completed missing-value policy. Native dtypes are deliberate; truncation/float32 information loss is not accounting rounding. No valuation/status-update protocol is implemented.

## 6.4

**6.4-SETUP — PARTIAL**

Selected interpreter and NumPy origin/version recorded. Reused preinstalled3.12.14/2.3.5; fresh venv/index installation and platform shell routes not executed.

**6.4-FILES — PASS_SCOPED**

Reconstructed exact two source/test listings as documented sibling filenames in a separate owned temporary lab; all source and listing hashes retained; no path edits.

**6.4-COMPILE — PASS_SCOPED**

Both exact file payloads compile under selected interpreter. No static type-checker inference.

**6.4-IMPORT — PASS_SCOPED**

Fresh child module import has exactly empty stdout/stderr. This is quiet-import evidence,not application file-access instrumentation or OS sandboxing.

**6.4-APPLICATION — PASS_SCOPED**

Exact original main ran; full stdout matches documented expected text including ordering/format/newlines and stderr empty. Independently derived API/attribute/selection checks supply another oracle.

**6.4-REFERENCE — PASS_SCOPED**

Exact original test discovery ran8 existing methods with no skip/failure/error; raw stderr/stdout retained. Existing methods not added again to historical unique totals.

**6.4-API — PASS_SCOPED**

Plain-list oracle for C,A across dates; independent storage; empty request(3,0); coordinate-pair versus rectangle oracle; latest-row>=80 mask selects A data/ID; invalid unselected source value rejected.

**6.4-SEMANTICS — REVIEWED_CONCEPTUAL**

Axis0 is stored observation order,not necessarily chronology. Axis1 IDs must correspond to actual source data. Selection returns requested order and independent storage,allowing empty request with retained dates axis. All source values validated including unselected columns. Paired coordinates differ from cross-product rectangles; masks/data/IDs must align. Advanced-copy edits differ from direct assignment. Threshold is an indexing example,not investment screening.
