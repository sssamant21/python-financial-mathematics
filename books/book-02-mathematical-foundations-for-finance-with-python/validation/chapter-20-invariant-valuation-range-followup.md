# Section 20.3 factor, PV/FV and cash-flow range

Date: 2026-11-05. Baseline: `df88087d11b755fa379796ad1efdd2932a7f2811`. Corrected executable pin: `ec2d14291906ca137698e6716779a4634495b18b`.

Section 20.3's discount-factor, PV and FV wrappers now use the local complete scaled valuation kernel after public validation. A scalar amount may be finite even when its standalone exponential factor is unrepresentable. PV therefore evaluates the complete amount rather than requiring a separately representable discount factor. Discount factor itself is the scaled evaluation for amount one. Nonzero factors/amounts rounding to zero and nonfinite results raise ValueError; valid zero-amount identities remain.

Independent 1,600-digit references cover seven factor cases, eight PV cases, six FV cases, three actual PV/FV round trips, three real cash-flow totals, six guards and seven actual assessment fields: 40 cases total. The initial run exited 1 with 16 failures; the corrected run exited 0 with all 40 passing. Four ulps and exact zero/nonzero classification are required. Eleven observed shared evaluation calls additionally verify report composition, split-payment sums, the actual returned FV feeding PV, and cash-flow integration. Helpers are restored afterward.

The selected round trips require representable intermediate monetary states. They do not require a separately representable factor and do not imply an inverse can cross an unrepresentable monetary state. Cash-flow terms are still rounded individually before fsum; the existing OverflowError for an overflowing aggregate is retained and tested. General cancellation/aggregate accuracy and all other copies remain separate obligations.

All 27 chapter sources compiled and 16 scripts passed, with matching before/after source hashes. Matrix, portfolio and account-transition scopes are unchanged by this batch; they retain their separate evidence and open numerical boundaries.

[Raw failures, rerun, scoped hashes and exact kernel provenance](chapter-20-invariant-valuation-range-followup.json) · [Runnable checker](../chapter-20/code/check_invariant_valuation_range.py) · [Local kernel](../chapter-20/code/_valuation_math.py).

The local kernel adapts selected calculation bodies from pinned Section 19.2/19.8 sources, recorded by path and blob in the raw evidence. It has no cross-chapter runtime imports or sys.path changes. Adaptation and assistant checks are not independent reviewer approval.

Replay from a clean checkout at the corrected pin: change to Book 02's chapter-20/code and run python check_invariant_valuation_range.py, assertions enabled. For initial failures, save that checker externally, select the stated baseline revision, overlay only the checker and run it there. Compile every chapter-20/code/*.py using py_compile.compile(path,doraise=True); run every check_/test_ basename separately from its parent directory in a fresh Python process with timeout=60. Compare the raw manifest Git blob SHA-1 values before/after. Include the local kernel in the corrected snapshot. Successful stdout is omitted from the scope summary.

COV-87 remains partial; 32 selected categories remain partially addressed and none closed. Section 19.8 end-period abs(rate*years)>4000 remains an explicit evaluation boundary. Selected assistant-derived references and Python 3.12.14/Linux checks only; no independent reviewer sign-off, supported-platform validation, release acceptance, canonical approval, general numerical accuracy or financial model validation.
