# Section 8.9 — Payoff diagrams review

Baseline `e5cfc81a96ea8a64bdec3adedab1f11086ee753a`. [Runner](review.py) · [Initial failure](initial-results.json) · [Corrected results](results.json) · [Worked answers](ANSWERS.md).

One formal lab and eight local answers reviewed. Three documented commands, twelve additional predicates and eight existing methods passed after correction. Exact complete program and test listings were reconstructed as siblings and discovery, demonstration and compilation ran in the lab directory. Prepared Linux CPython 3.12.14, NumPy 2.3.5 and Matplotlib 3.10.8 were used. Embedded scenarios require no previous lab, pandas, external option data or desktop. Fresh installations and other platforms were not executed.

**F41:** The declared real-scalar boundary admitted Fraction objects but NumPy's finiteness check raised TypeError. The initial failure is retained; bounds are now checked before and after float conversion and calculations use normalized scalars. The existing known-answer method now includes Fraction assertions; no new historical method. To reproduce the initial failure, use this runner at the same relative path in a worktree of the baseline.

Independent positive-part formulas verify complete call and put scenario arrays, premium shifts, multiplier scaling and the terminal identity. The two-point interpolation example is supplemental; the source figure includes strike and break-even coordinates. The PNG was visually inspected for kinks, payoff/profit distinction, units and break-even labels. The runner regenerates it and records its hash. These checks establish neither pre-expiration value nor an option-pricing parity relation. F28/F32 and independent acceptance remain open.

```bash
python3 -B books/book-01-python-foundations-for-financial-mathematics/qa/chapter-08-payoff-review/review.py
```

Next: Section 8.10 formal lab and local answers.
