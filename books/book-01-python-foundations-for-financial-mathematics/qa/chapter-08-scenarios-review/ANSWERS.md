# Section 8.11 — Worked answer review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Reference | Principal USD 1000, 5% effective annual rate, ten whole years and no flows, costs or inflation adjustment. Reference balance is 1000×(21/20)^10 ≈ USD 1628.89. | Exact source and rational oracle |
| 2. Shock units | 100 basis points is 0.01 in decimal rate; adding it to 0.05 gives 0.06. | Independent fractions |
| 3. Local units | The derivative is 1000×10×1.05^9 ≈ USD 15513 per unit decimal rate. Multiplying by 0.01 gives a first-order estimate of about USD 155.13; full revaluation differs because of curvature. | Supplemental exact derivative and finite-shock arithmetic |
| 4. Joint case | The roughly USD 623.30 increase changes both effective rate from 5% to 7% and horizon from ten to twelve years. It cannot be attributed solely to rate. | Source case inputs and rational deltas |
| 5. Orientation | Rates are rows; horizons are columns. In the plotted arrays 5% is row two and ten years is column one, hence [2,1]. | Exact source grid and mesh |
| 6. Color | Color represents modeled terminal USD balance; it does not encode likelihood. | Source colorbar and conceptual review |
| 7. Cell extent | Each cell shows the output at its labeled sampled inputs. The surrounding rectangle is a rendering geometry, not a bound on all values inside it. | Source sample grid and conceptual review |
| 8. Probability | A 95% prediction interval needs a probabilistic model, target and horizon, estimation/validation method and a declared coverage interpretation. The deterministic scenarios supply no such evidence. | Conceptual review |
