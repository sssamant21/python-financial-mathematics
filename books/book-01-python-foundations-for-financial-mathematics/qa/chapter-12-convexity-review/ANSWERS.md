# Section 12.11 — Answers and mini-project

| Prompt | Review |
|---|---|
| 1–4 | Convexity is normalized second price derivative, (d²P/dy²)/P. Positive fixed cash flows give positive curvature. |
| 5–6 | The first-order estimate is −D_ModΔy; add 0.5 × convexity × Δy² for the quadratic estimate. |
| 7 | 100 bp = 0.01. |
| 8 | −2.7 × 0.01 = −2.70%. |
| 9 | 0.5 × 9.5 × 0.01² = 0.000475 = 0.0475%. |
| 10 | Combined illustrative change is −2.6525%. |
| 11 | Squaring the shock leaves a positive correction for either sign. |
| 12–14 | 6% annual coupon gives 30 per half year, six payments and 1,000 par under the matching 6% yield. |
| 15 | The zero-coupon formula n(n+1)/[m²(1+i)²] matches the source. |
| 16 | The observer independently derives [P(y+h)−2P(y)+P(y−h)]/h² from backward prices. |
| 17 | The approximation is not exact; higher-order terms remain. |
| 18 | Conceptual: options can change expected cash flows, so effective convexity need not match this fixed-flow model. |

Run and compile the named standalone file. The observer calls the exact listing at all eight specified signed shocks. It records both absolute approximation errors, checks all three reported changes against independently derived values, and confirms that the quadratic error is smaller and nonzero in each case. Inputs use nominal annual yields with the same semiannual compounding convention.
