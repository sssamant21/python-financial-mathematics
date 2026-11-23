# V10 — Section14.15 RNG/reproducibility assumptions

Pinned source `50191124b93345af6b74ccc971d94b86edbad98f`. Run `python -B review.py results` and `python -B review.py replay`. [Results](results.json) and [replay](replay.json) each record **34 predicates passed,zero failed**, source/formal-listing/illustration SHA256,Python/platform and captured native commands. No initial failure or financial-source correction occurred in this Book1 batch.

| Assumption | Executed source and independent reasoning |
|---|---|
| State and call order |256 actual uniforms match a separate local Random replay. Longer runs preserve prefixes;inserting a draw shifts the sequence. Cloning seed/state duplicates the experiment rather than establishing an independent worker stream. Shared module state stays unchanged through uniform/normal/scenario probes. |
| Other samplers |128 actual normal draws match separate gauss replay;256 actual weighted scenarios match uniform CDF bands. Moderate common weight scaling preserves draws. These are reproducibility checks on this runtime,not normality,calibration or arbitrary tiny-weight guarantees. |
| Paired constant shift |Three sample sizes and four shifts,including1e−300,check exact represented additive differences. That model has no paired Monte Carlo noise;this does not generalize to nonlinear stresses. |
| CRN/antithetic limits |Supplemental exact four-point uniform-grid laws give independent difference variance2v,positive-CRN0,and negative-CRN4v. Monotone antithetic means are constant,but symmetric nonmonotone squared deviations are identical pairs with variance v rather than independent-average v/2. These finite model identities illustrate covariance conditions,not empirical variance-reduction claims. |
| Manifest scope |Independent canonical JSON reproduces the hash. Scaling weights changes the byte identity despite the same sampling law. Shifting actual payoff values changes means by2 while the narrow seed/count/weight/generator manifest remains identical;that hash does not bind omitted payoff/source/runtime metadata or certify model accuracy. |

Each final run imports the formal listing,executes twelve existing methods,executes the separate uniform illustration verbatim,and compiles both fences:**six commands,24 invocations of twelve methods,two separate illustration executions**. Supplemental predicates do not add historical methods,workflows,answers or steps. F124 source/listing identities match [the prior formal review](../chapter-14-rng-review/README.md),retaining five initial failures,32 predicates,24 answers and ten project requirements.

Parallel substream independence,cryptographic security review,rare-tail weights,cross-runtime sequences and market calibration remain outside scope. Next: §14.16 chapter probability-simulator assumptions,then14.17 and other marked V10 interfaces. V10/Book1,F28/F32/F209/F165/F185 and broader acceptance remain open.
