# Sections6.9–6.12 formal step/contract review

Four workflows,32derived units:24scoped-pass execution/file units,4partial setup records,4conceptual semantic reviews. Local exercises remain separate even where probes overlap.

## 6.9

**6.9-SETUP — PARTIAL**

Recorded explicit CPython3.12.14 interpreter,NumPy2.3.5 origin/version in preinstalled Linux runtime. Fresh pip/venv setup,Windows/macOS not executed.

**6.9-FILES — PASS_SCOPED**

Reconstructed2exact source/test listings as documented siblings in owned temporary lab;hashes recorded,no path edits,bytes unchanged.

**6.9-COMPILE — PASS_SCOPED**

Both exact payloads compile;no static checker inference.

**6.9-IMPORT — PASS_SCOPED**

Fresh ordinary module import has empty stdout/stderr;quiet streams are not file-access or sandbox evidence.

**6.9-APPLICATION — PASS_SCOPED**

Unchanged source main full stdout/newlines match documented example and stderr empty. Known-runtime diagnostic string equality is not imposed on every valid solver input/platform.

**6.9-REFERENCE — PASS_SCOPED**

Exact8existing test methods pass without failure/error/skip;raw command/stdout/stderr retained;not new unique tests.

**6.9-API — PASS_SCOPED**

Fraction ratios11/10,9/10,11/10; growth11/10,99/100,1089/1000;final89/1000versus additive1/10. N-1labels,changed timing unchanged ratios,independent storage,tiny positive gross despite simple-1,terminal-zero/extreme-ratio failures and restored policy.

**6.9-SEMANTICS — REVIEWED_CONCEPTUAL**

One positive-price asset path with N observations,N-1 observed intervals and copied start/end offsets. Gross ratios retained separately from simple returns; tiny positive ratios may still have simple return rounded-1. Strict positive prices exclude terminal zero by this API,unlike6.1 endpoint contract. Irregular timing is preserved,not annualized or filled. No distributions/fees/FX/total-return/expected-return claim; corporate-action consistency/completeness remain caller assertions.

## 6.10

**6.10-SETUP — PARTIAL**

Recorded explicit CPython3.12.14 interpreter,NumPy2.3.5 origin/version in preinstalled Linux runtime. Fresh pip/venv setup,Windows/macOS not executed.

**6.10-FILES — PASS_SCOPED**

Reconstructed2exact source/test listings as documented siblings in owned temporary lab;hashes recorded,no path edits,bytes unchanged.

**6.10-COMPILE — PASS_SCOPED**

Both exact payloads compile;no static checker inference.

**6.10-IMPORT — PASS_SCOPED**

Fresh ordinary module import has empty stdout/stderr;quiet streams are not file-access or sandbox evidence.

**6.10-APPLICATION — PASS_SCOPED**

Unchanged source main full stdout/newlines match documented example and stderr empty. Known-runtime diagnostic string equality is not imposed on every valid solver input/platform.

**6.10-REFERENCE — PASS_SCOPED**

Exact8existing test methods pass without failure/error/skip;raw command/stdout/stderr retained;not new unique tests.

**6.10-API — PASS_SCOPED**

Fraction opening weights3/5,3/10,1/10;contributions3/50,-3/200,0;return9/200;ending1045/1000value bridge. Near-one accepted without correcting supplied bytes;wrong ID order,zero denominator and invalid zero-weight component reject;output storage independent.

**6.10-SEMANTICS — REVIEWED_CONCEPTUAL**

Normalize nonnegative comparable opening values under positive denominator; cash belongs if included in portfolio. Validate supplied fractional long-only weights,never silently renormalize near-one input. Begin-interval weights differ from closing weights; repeated weights across time may imply rebalancing. Exact ID/order checks do not authenticate labels or common interval/currency. Contributions are fractional portfolio points,not currency P&L absent denominator. No leverage/financing/trades/flows/distributions/FX model.

## 6.11

**6.11-SETUP — PARTIAL**

Recorded explicit CPython3.12.14 interpreter,NumPy2.3.5 origin/version in preinstalled Linux runtime. Fresh pip/venv setup,Windows/macOS not executed.

**6.11-FILES — PASS_SCOPED**

Reconstructed2exact source/test listings as documented siblings in owned temporary lab;hashes recorded,no path edits,bytes unchanged.

**6.11-COMPILE — PASS_SCOPED**

Both exact payloads compile;no static checker inference.

**6.11-IMPORT — PASS_SCOPED**

Fresh ordinary module import has empty stdout/stderr;quiet streams are not file-access or sandbox evidence.

**6.11-APPLICATION — PASS_SCOPED**

Unchanged source main full stdout/newlines match documented example and stderr empty. Known-runtime diagnostic string equality is not imposed on every valid solver input/platform.

**6.11-REFERENCE — PASS_SCOPED**

Exact8existing test methods pass without failure/error/skip;raw command/stdout/stderr retained;not new unique tests.

**6.11-API — PASS_SCOPED**

Exact scalar cells[[9/200,1/200],[-9/100,-1/100],[1/5000,1/1000]];3x2outputlabels;consistent column permutation invariance and one-sided rejection;input9vs8budget and separate output-only12vs6budget reject;transpose sharing/result independence.

**6.11-SEMANTICS — REVIEWED_CONCEPTUAL**

R axes scenarios/instruments,W axes portfolios/instruments; R@W.T contracts instrument axis and retains scenarios/portfolios. Alternatives are not time path/probabilities; fixed opening W intentionally reused. Transpose can share storage. IDs must align and complete finite inputs validated before budget check. max_cells applies per input/output matrix,not total process workspace or prevention of reading existing large inputs. Cash yield is supplied convention,not implicit accrual engine. No optimizer,contribution cube or calibrated risk model.

## 6.12

**6.12-SETUP — PARTIAL**

Recorded explicit CPython3.12.14 interpreter,NumPy2.3.5 origin/version in preinstalled Linux runtime. Fresh pip/venv setup,Windows/macOS not executed.

**6.12-FILES — PASS_SCOPED**

Reconstructed2exact source/test listings as documented siblings in owned temporary lab;hashes recorded,no path edits,bytes unchanged.

**6.12-COMPILE — PASS_SCOPED**

Both exact payloads compile;no static checker inference.

**6.12-IMPORT — PASS_SCOPED**

Fresh ordinary module import has empty stdout/stderr;quiet streams are not file-access or sandbox evidence.

**6.12-APPLICATION — PASS_SCOPED**

Unchanged source main full stdout/newlines match documented example and stderr empty. Known-runtime diagnostic string equality is not imposed on every valid solver input/platform.

**6.12-REFERENCE — PASS_SCOPED**

Exact8existing test methods pass without failure/error/skip;raw command/stdout/stderr retained;not new unique tests.

**6.12-API — PASS_SCOPED**

Manual elimination50/50,signed150/-50;reconstructed100/150;analytic cond2=(7+3sqrt5)/2 via precision60 Decimal;normalized gate,zero-target convention,singular/ill-conditioned rejection and independent storage. Raw-solver sensitivity compared to exact binary-input Fraction elimination,then guarded API rejection verified separately.

**6.12-SEMANTICS — REVIEWED_CONCEPTUAL**

A rows payoff states,columns instrument unknowns;b aligned state targets,x signed units. Square exact-match solving is distinct from least-squares/optimization/trade execution. Residual<=1e-12 and cond2<=1e8 are numerical teaching gates,not universal economic tolerances. Small residual does not establish low sensitivity; scale/units/uncertain coefficients matter. Gate precedes solve; backend exceptions remain failures,no fallback. Economic existence/tradability/shorting/cost/funding constraints and off-table states remain unmodeled.
