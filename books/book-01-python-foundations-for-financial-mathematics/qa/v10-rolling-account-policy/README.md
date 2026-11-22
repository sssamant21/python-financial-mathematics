# V10 — Section15.12 local-window wealth and window/project policies

Executable source pin: `5c543db206151d5be9eb609a6e5e4fb5fe5e377b`. [Runnable review](review.py), [first](first.json), [replay](replay.json).

```bash
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-rolling-account-policy/review.py first
python books/book-01-python-foundations-for-financial-mathematics/qa/v10-rolling-account-policy/review.py replay
```

**420 predicates pass twice with identical rows:**405 native compounded-window fields over all81 ordered four-return paths from{−1,0,.1}, with windows2/3;15 account/window/project-policy checks. Exact fresh-capital gross products are independent references. Numeric tolerance rtol5e-14,atol1e-15; source arrays, labels and fixture hashes compare exactly where appropriate. This deterministic grid is not a sampled financial distribution or81 independent statistical observations.

For [.1,−1,.1,.1], native two-period returns are[−1,−1,.21]. The final window excludes the loss and asks what **fresh capital invested at that window's start** would earn. A supplemental global account starting at1 before all four returns has wealth[1.1,0,0,0] and cannot recover without a separately specified replenishment/new-account convention. No source global-account API or financial bankruptcy recovery is claimed. The oracle compares separate estimands; a rolling return above−1 after the loss exits is not a source defect.

For [1,1,1,9], a fixed three-observation mean ends at11/3, while caller-assembled expanding-prefix means are[1,1,1,3]. Source full-prefix mean calls supply the latter; there is no exported expanding-window API. A one-output-position lag gives[None,1] for the two fixed-window means, without enforcing real publication/execution clocks. Warm-up and observation-count conventions remain explicit. The manuscript's EWMA v_t=lambda v_(t−1)+(1−lambda)r_(t−1)^2 is a separate zero-mean-innovation recursion requiring initialization, frequency and lambda choices; it has no native implementation, and no EWMA test or deployment is claimed.

The prescribed A/B30-label synthetic project fixture hash matches earlier evidence. For w5/10/20, perturbing only A after label20 preserves every native mean ending by20; first complete outputs map to labels5/10/20. These are numeric dependency/caller-label contracts, not data-availability or execution-delay validation. The prior project retains58 endings,232 core metrics,58 supplemental annualized SD fields and its lag/expanding records; none are recounted as new answers/workflows/steps or independent observations. Real calendars, imputation, publication times, costs, orders and robust inference remain outside these numeric APIs and F32 integration stays open.

Each run executes the full verbatim demo/twelve existing methods and compilation:four command records/24 invocations of twelve existing methods total. Whole-source/fence identity matches F138 corrected evidence; the initial observer crash,twelve baseline failures/54 corrected predicates and earlier89 mean/585 distribution predicates retain scope. No source change/defect or new historical-method/workflow/answer/step totals.

The selected15.12 V10 assumption crosswalk is recorded; next15.13 statistical-pitfall/bias/leakage/selection assumptions, preserving earlier arithmetic evidence. V10/Book1,F28/F32/F209/F165/F185 and broader numerical/resource/data/model/platform/release/independent/canonical gates remain open. No independent/supported-platform/financial acceptance.
