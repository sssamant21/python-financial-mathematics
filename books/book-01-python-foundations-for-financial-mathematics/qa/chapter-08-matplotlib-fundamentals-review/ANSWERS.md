# Section 8.2 — Worked answer review

| Prompt | Reviewed answer | Evidence |
|---|---|---|
| 1. Figure and upper label ownership | The Figure contains both Axes; the upper Axes exposes its y-label, managed by its y-axis. | Exact source objects |
| 2. Axis versus Axes | `balance_ax.yaxis` is the vertical Axis inside the upper Axes. It manages the vertical label, ticks and scale, not the full plotting panel. | Exact source objects |
| 3. Subplot indexing | With `squeeze=False`, one panel still yields an array of shape (1, 1); select `axes[0, 0]`. | Supplemental direct call |
| 4. Line return value | The call returns a list. A one-target unpack extracts one Line2D and fails if the list length is not exactly one. | Supplemental direct call; source uses unpacking |
| 5. Year-two lower value | With gross annual ratio 21/20, year-two balance is 1000×(21/20)² = 1102.50. Lower panel shows 1102.50−1000 = USD 102.50; 1102.50−1050 = USD 52.50 is the year-two increment. | Exact source and rational arithmetic |
| 6. Raster sizing | 10×200 by 4×200 = 2000×800 pixels for the uncropped export. Cropping may change dimensions. | Supplemental PNG header |
| 7. Lifecycle | Close in `finally` even if SVG fails. The earlier PNG can remain, so report each output separately. | Simulated I/O failure against exact source main |
| 8. Style scope | With the surrounding font size 17, the source uses 10 for the legend and restores the surrounding value. This checks that setting only, not all external rendering dependencies. | Exact source under controlled rc context |
