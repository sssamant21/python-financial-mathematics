# Section 8.12 — Effective financial chart design review

Baseline `b95dc56240bcf296e6bcfa6947e5c51e4fd8130a`. [Runner](review.py) · [Initial runner](initial-review.py) · [Initial results](initial-results.json) · [Corrected results](results.json) · [Answers](ANSWERS.md).

One formal workflow and eight local answers reviewed. Three documented commands, thirteen additional predicates and eight existing methods passed on the corrected rerun. Complete Python listings were saved verbatim as siblings under the documented lab directory; discovery, demonstration and compilation ran there. The fixture is embedded and requires no previous lab, external returns or desktop. Prepared Linux CPython 3.12.14, NumPy 2.3.5, pandas 2.2.3 and Matplotlib 3.10.8 were used. Fresh installs and other platforms were not executed.

**F44 (QA harness):** The initial reconstruction named the module financial_chart_design.py rather than the documented chart_design.py, so test imports failed. The exact initial runner and raw failure are retained; correcting both reconstructed filenames and the demonstration command resolved it. No manuscript defect or source fix is claimed. Initial and corrected test invocations are not new unique historical methods.

Independent fractions and labeled expectations verify signed bars; alternate tied values test the deterministic sort. Colour and monochrome PNGs were visually inspected for direct signed labels, hatching, zero visibility, time window, omitted EPSILON and reading order. SVG structure was parsed but not separately rendered. These synthetic fixture checks do not establish assistive-technology accessibility or source quality for real assets. The runner regenerates both PNGs and retains the colour hash; input/source hashes and full command outputs are in results. F28/F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-chart-design-review/review.py
```

Next: Section 8.13 project lab, acceptance/extension records and local answers.
