# V10 — Section14.16 integrated probability-simulator assumptions

Pinned source `fa4f0ff5ab47be843c18525195fed5c2041b7f72`. Run `python -B review.py results` and `python -B review.py replay`. [Results](results.json) and [replay](replay.json) each record **26 predicates passed,zero failed**, source/implementation/driver SHA256,Python/platform and captured commands. No initial failure or financial-source change occurred.

| Integrated contract | Exact source and independent model/replay distinction |
|---|---|
| Actual draw summaries |256 actual scenario draws match independent uniform CDF bands. Integer sums and rational centered variance with90digit square roots check mean/sample SD/IID plug-in SE. Loss rate uses explicit negative-payoff counts;two tail summaries use the declared interpolated empirical rank. |
| Stress |Negative/zero/positive additive stresses preserve the actual ordinary payoff mapping and shifted mean. A1-unit shock at1e16 rounds to the same binary payoff;the returned rounded payoff is not an exact paired-difference guarantee. This observed reporting limit is retained rather than claiming all tiny shifts resolve. |
| Bootstrap |128 actual native bootstrap means are reproduced through independent uniform indices;exact rational sample variance supplies bootstrap SE. Resampling cannot create outcomes absent from the empirical support and does not quantify wrong-model or unseen-tail risk. |
| Independent defaults |256 actual native four-loan count trials match separate Bernoulli replay. Exhaustive product paths give mean1/variance.75 at PD.25. A shared indicator keeps identical marginal PD/mean but gives count variance3;the native helper does not implement correlated defaults. |
| Provenance |Independent canonical JSON reproduces the actual base manifest. Payoff changes alter the digest;bootstrap repetitions,stress settings,driver/source/runtime metadata are outside that payload and remain necessary separate evidence. |

Each final run imports the exact implementation,executes twelve existing native methods,executes the exact20,000-draw experiment driver(including its500 bootstrap repetitions),and compiles both fences:**six commands,24 invocations of twelve methods,two exact driver executions** across the runs. Full console outputs are retained. These executions are separate from the256/128-size supplemental probes. No new historical methods,workflows,answers or project-step totals.

F125 entire-source and implementation hashes match [the prior formal project review](../chapter-14-simulator-review/README.md),retaining seven initial failures,48 predicates,24 answers and all five acceptance phases/ten-step evidence within their original scopes. The prior1,000/40,000-draw uncertainty comparisons are retained by unchanged source identity;they are not claimed as new executions here.

Missing correlated-default/market calibration,dependence-aware bootstrap,tiny-weight/cross-runtime support and production/independent acceptance remain open. Next: §14.17 applied probability exercises/model assumptions,then other marked V10 interfaces. V10/Book1,F28/F32/F209/F165/F185 and broader acceptance remain open.
