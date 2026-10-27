# Book 2 — Mathematical Foundations for Finance with Python

## Master Table of Contents v1.0

**Status:** Established curriculum for section-by-section development.  
**Version date:** 2026-10-22.  
**Scope:** 21 chapters; complete numbered section plan.  
**Manuscript status:** Sections 1.1–1.15, 2.1–2.10, and 3.1–3.10, 4.1–4.10, 5.1–5.10, 6.1–6.10, 7.1–7.10, 8.1–8.10, 9.1–9.10, 10.1–10.10, and 11.1–11.10 and 12.1–12.10 and 13.1–13.10 and 14.1–14.10 published as Draft. Runtime validation remains pending for Sections 2.8–2.10, 3.1–3.10, 4.1–4.10, 5.1–5.10, 6.1–6.10, and 7.1–7.10; later sections are Planned.

## Purpose and Prerequisites

Develop the mathematical reasoning behind deterministic financial models: notation, algebra, functions, sequences and series, calculus, linear algebra, optimization, numerical reliability, and differential equations. Assume the Python, NumPy, plotting, reusable-function, and testing skills introduced in Book 01. Begin the mathematical explanations from first principles rather than assuming prior university calculus.

Financial examples connect the mathematics to cash flows, growth, discounting, sensitivities, exposure matching, and constrained decisions. Probability, statistical inference, stochastic processes, and Itô calculus receive their full treatment in Book 03. Financial instruments, derivative pricing, portfolio theory, advanced numerical methods, and production systems are developed in their respective later books.

## Structure and Writing Workflow

Follow Book 01's chapter and numbered-section organization. Each chapter includes a chapter project, exercises and applied problems, and separate companion solutions and reference implementations. Section counts reflect subject coverage rather than a fixed quota.

1. Complete one numbered section with explanations, derivations, assumptions, worked examples, Python implementation, practical exercises, and references.
2. Validate that section's mathematics and executable examples; record the scope of evidence and unresolved review items.
3. Push the section and update its chapter/book indexes before proceeding to the next section.
4. Finish the chapter project, chapter-wide exercises, and companion solutions before starting the next chapter.
5. Do not publish later chapters in a batch or label planned content as written.

Manuscript depth should follow Book 01's substantive treatment. The TOC is a plan, not a replacement for the manuscript. Core examples should run locally on a CPU with small, bundled or synthetic inputs; cloud accounts and paid data should not be prerequisites. Chapter 01 should require only the Python standard library.

## Editorial Workflow

**Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition**

Retain references in each substantive section from the Draft stage. Prefer official Python and scientific-computing documentation, authoritative mathematics sources, and established finance references where appropriate. Use original prose, derivations, examples, exercises, and code. Runtime tests and source-link checks are evidence, not automatic completion of the canonical editorial gates.

## Naming and Index Conventions

- Book index: `README.md`.
- Authoritative section sequence: `MASTER-TOC.md`.
- Chapter index: `chapter-01/README.md`.
- Example manuscript filename: `chapter-01/1.01-why-mathematical-foundations-matter-in-finance.md`.
- Chapter 01 solutions: `chapter-01/solutions/1.15-solutions-and-reference-implementations.md`.
- Chapter code and evidence should accompany the relevant manuscript when they are created.

Published sections link to their manuscript files; planned sections remain plain text.

---

# Chapter 1 — Mathematical Language, Notation, and Reasoning

1.1 — [Why Mathematical Foundations Matter in Finance](chapter-01/1.01-why-mathematical-foundations-matter-in-finance.md)  
1.2 — [Mathematical Objects and Number Systems](chapter-01/1.02-mathematical-objects-and-number-systems.md)  
1.3 — [Variables, Constants, and Parameters](chapter-01/1.03-variables-constants-and-parameters.md)  
1.4 — [Sets, Intervals, and Financial Domains](chapter-01/1.04-sets-intervals-and-financial-domains.md)  
1.5 — [Mathematical Notation and Indexed Quantities](chapter-01/1.05-mathematical-notation-and-indexed-quantities.md)  
1.6 — [Expressions, Equations, and Identities](chapter-01/1.06-expressions-equations-and-identities.md)  
1.7 — [Inequalities and Financial Constraints](chapter-01/1.07-inequalities-and-financial-constraints.md)  
1.8 — [Logic, Assumptions, and Implications](chapter-01/1.08-logic-assumptions-and-implications.md)  
1.9 — [Definitions, Propositions, and Counterexamples](chapter-01/1.09-definitions-propositions-and-counterexamples.md)  
1.10 — [Units, Dimensions, and Financial Conventions](chapter-01/1.10-units-dimensions-and-financial-conventions.md)  
1.11 — [Translating Financial Questions into Mathematics](chapter-01/1.11-translating-financial-questions-into-mathematics.md)  
1.12 — [Translating Mathematical Expressions into Python](chapter-01/1.12-translating-mathematical-expressions-into-python.md)  
1.13 — [Checking Mathematical and Computational Results](chapter-01/1.13-checking-mathematical-and-computational-results.md)  
1.14 — [Chapter Project — Financial Formula Validation Toolkit](chapter-01/1.14-chapter-project-financial-formula-validation-toolkit.md)  
1.15 — [Exercises and Applied Problems](chapter-01/1.15-exercises-and-applied-problems.md)

# Chapter 2 — Algebra and Equations for Financial Models

2.1 — [Algebraic Expressions and Equivalent Forms](chapter-02/2.01-algebraic-expressions-and-equivalent-forms.md)  
2.2 — [Linear Equations and Rearrangement](chapter-02/2.02-linear-equations-and-rearrangement.md)  
2.3 — [Fractions and Rational Equations](chapter-02/2.03-fractions-and-rational-equations.md)  
2.4 — [Powers, Roots, and Fractional Exponents](chapter-02/2.04-powers-roots-and-fractional-exponents.md)  
2.5 — [Quadratic Equations](chapter-02/2.05-quadratic-equations.md)  
2.6 — [Inequalities and Absolute Values](chapter-02/2.06-inequalities-and-absolute-values.md)  
2.7 — [Simultaneous Equations](chapter-02/2.07-simultaneous-equations.md)  
2.8 — [Scaling and Algebraic Validation](chapter-02/2.08-scaling-and-algebraic-validation.md)  
2.9 — [Chapter Project — Break-Even and Formula Rearrangement Analyzer](chapter-02/2.09-chapter-project-break-even-and-formula-rearrangement-analyzer.md)  
2.10 — [Exercises and Applied Problems](chapter-02/2.10-exercises-and-applied-problems.md)

# Chapter 3 — Functions and Financial Relationships

3.1 — [Inputs, Outputs, Domain, and Range](chapter-03/3.01-inputs-outputs-domain-and-range.md)  
3.2 — [Graphs and Financial Interpretation](chapter-03/3.02-graphs-and-financial-interpretation.md)  
3.3 — [Composition of Functions](chapter-03/3.03-composition-of-functions.md)  
3.4 — [Inverse Functions](chapter-03/3.04-inverse-functions.md)  
3.5 — [Piecewise Functions and Thresholds](chapter-03/3.05-piecewise-functions-and-thresholds.md)  
3.6 — [Monotonicity and Bounds](chapter-03/3.06-monotonicity-and-bounds.md)  
3.7 — [Convexity and Concavity Intuition](chapter-03/3.07-convexity-and-concavity-intuition.md)  
3.8 — [Function Specifications and Validation](chapter-03/3.08-function-specifications-and-validation.md)  
3.9 — [Chapter Project — Financial Function Explorer](chapter-03/3.09-chapter-project-financial-function-explorer.md)  
3.10 — Exercises and Applied Problems

# Chapter 4 — Exponential and Logarithmic Functions

4.1 — [Exponential Growth and Decay](chapter-04/4.01-exponential-growth-and-decay.md)  
4.2 — [Natural Exponential and Logarithm](chapter-04/4.02-natural-exponential-and-logarithm.md)  
4.3 — [Logarithm Rules and Their Domains](chapter-04/4.03-logarithm-rules-and-their-domains.md)  
4.4 — [Discrete and Continuous Compounding](chapter-04/4.04-discrete-and-continuous-compounding.md)  
4.5 — [Solving for Time and Growth Rate](chapter-04/4.05-solving-for-time-and-growth-rate.md)  
4.6 — [Products and Additive Log Changes](chapter-04/4.06-products-and-additive-log-changes.md)  
4.7 — Stable Evaluation Near Zero  
4.8 — Growth Assumptions and Model Limits  
4.9 — [Chapter Project — Growth and Rate Conversion Explorer](chapter-04/4.09-growth-and-rate-conversion-explorer.md)  
4.10 — [Exercises and Applied Problems](chapter-04/4.10-exercises-and-applied-problems.md)

# Chapter 5 — Sequences, Recurrences, and Financial Growth

5.1 — [Sequences and Time Indexing](chapter-05/5.01-sequences-and-time-indexing.md)  
5.2 — [Arithmetic and Geometric Sequences](chapter-05/5.02-arithmetic-and-geometric-sequences.md)  
5.3 — [First-Order Balance Recurrences](chapter-05/5.03-first-order-balance-recurrences.md)  
5.4 — [Closed Forms from Repeated Substitution](chapter-05/5.04-closed-forms-from-repeated-substitution.md)  
5.5 — [Fixed Points and Equilibria](chapter-05/5.05-fixed-points-and-equilibria.md)  
5.6 — [Convergence and Stability](chapter-05/5.06-convergence-and-stability.md)  
5.7 — [Variable Rates and Payment Schedules](chapter-05/5.07-variable-rates-and-payment-schedules.md)  
5.8 — [Withdrawal and Depletion Boundaries](chapter-05/5.08-withdrawal-and-depletion-boundaries.md)  
5.9 — [Chapter Project — Contribution and Withdrawal Recurrence Engine](chapter-05/5.09-contribution-and-withdrawal-recurrence-engine.md)  
5.10 — Exercises and Applied Problems

# Chapter 6 — Summation, Series, and Cash-Flow Derivations

6.1 — [Summation and Product Notation](chapter-06/6.01-summation-and-product-notation.md)  
6.2 — [Finite Geometric Sums](chapter-06/6.02-finite-geometric-sums.md)  
6.3 — [Infinite Geometric Series](chapter-06/6.03-infinite-geometric-series.md)  
6.4 — [Ordinary Annuities and Annuities Due](chapter-06/6.04-ordinary-annuities-and-annuities-due.md)  
6.5 — [Growing Payment Streams](chapter-06/6.05-growing-payment-streams.md)  
6.6 — [Perpetuities and Tail Conditions](chapter-06/6.06-perpetuities-and-tail-conditions.md)  
6.7 — [Truncation and Approximation Error](chapter-06/6.07-truncation-and-approximation-error.md)  
6.8 — [Zero Rates and Independent Verification](chapter-06/6.08-zero-rates-and-independent-verification.md)  
6.9 — [Chapter Project — Cash-Flow Series Derivation and Verification Engine](chapter-06/6.09-cash-flow-series-derivation-and-verification-engine.md)  
6.10 — [Exercises and Applied Problems](chapter-06/6.10-exercises-and-applied-problems.md)

# Chapter 7 — Limits and Continuity

7.1 — [Limits and Approaching a Point](chapter-07/7.01-limits-and-approaching-a-point.md)  
7.2 — [One-Sided Limits](chapter-07/7.02-one-sided-limits.md)  
7.3 — [Continuity and Types of Discontinuity](chapter-07/7.03-continuity-and-types-of-discontinuity.md)  
7.4 — [Limits at Infinity and Asymptotes](chapter-07/7.04-limits-at-infinity-and-asymptotes.md)  
7.5 — [Exponential Limits and Continuous Compounding](chapter-07/7.05-exponential-limits-and-continuous-compounding.md)  
7.6 — [Important Small-Change Limits](chapter-07/7.06-important-small-change-limits.md)  
7.7 — [Intermediate Values and Root Existence](chapter-07/7.07-intermediate-values-and-root-existence.md)  
7.8 — [Numerical Investigation versus Proof](chapter-07/7.08-numerical-investigation-versus-proof.md)  
7.9 — [Chapter Project — Boundary and Continuity Investigation Lab](chapter-07/7.09-chapter-project-boundary-and-continuity-investigation-lab.md)  
7.10 — Exercises and Applied Problems

# Chapter 8 — Derivatives and Differentiation

8.1 — [The Derivative as a Limit](chapter-08/8.01-the-derivative-as-a-limit.md)  
8.2 — [Power, Sum, and Constant Rules](chapter-08/8.02-power-sum-and-constant-rules.md)  
8.3 — [Product and Quotient Rules](chapter-08/8.03-product-and-quotient-rules.md)  
8.4 — [The Chain Rule](chapter-08/8.04-the-chain-rule.md)  
8.5 — [Exponential and Logarithmic Derivatives](chapter-08/8.05-exponential-and-logarithmic-derivatives.md)  
8.6 — [Higher Derivatives and Curvature](chapter-08/8.06-higher-derivatives-and-curvature.md)  
8.7 — [Implicit Differentiation](chapter-08/8.07-implicit-differentiation.md)  
8.8 — [Numerical Derivatives and Step Selection](chapter-08/8.08-numerical-derivatives-and-step-selection.md)  
8.9 — [Chapter Project — Analytic and Numerical Derivative Comparator](chapter-08/8.09-analytic-and-numerical-derivative-comparator.md)  
8.10 — [Exercises and Applied Problems](chapter-08/8.10-exercises-and-applied-problems.md)

# Chapter 9 — Financial Sensitivity and Taylor Approximation

9.1 — [Absolute and Relative Sensitivity](chapter-09/9.01-absolute-and-relative-sensitivity.md)  
9.2 — [Elasticity](chapter-09/9.02-elasticity.md)  
9.3 — [First-Order Taylor Approximation](chapter-09/9.03-first-order-taylor-approximation.md)  
9.4 — [Second-Order Taylor Approximation](chapter-09/9.04-second-order-taylor-approximation.md)  
9.5 — [Remainder and Error Bounds](chapter-09/9.05-remainder-and-error-bounds.md)  
9.6 — [Discounted-Value Sensitivity](chapter-09/9.06-discounted-value-sensitivity.md)  
9.7 — [Kinks and One-Sided Sensitivities](chapter-09/9.07-kinks-and-one-sided-sensitivities.md)  
9.8 — [Sensitivity Reports and Scenario Revaluation](chapter-09/9.08-sensitivity-reports-and-scenario-revaluation.md)  
9.9 — [Chapter Project — Valuation Sensitivity and Approximation Report](chapter-09/9.09-valuation-sensitivity-and-approximation-report-project.md)  
9.10 — [Exercises and Applied Problems](chapter-09/9.10-exercises-and-applied-problems.md)

# Chapter 10 — Integration and Continuous Cash Flows

10.1 — [Accumulation and Riemann Sums](chapter-10/10.01-accumulation-and-riemann-sums.md)  
10.2 — [Definite and Indefinite Integrals](chapter-10/10.02-definite-and-indefinite-integrals.md)  
10.3 — [The Fundamental Theorem of Calculus](chapter-10/10.03-fundamental-theorem-of-calculus.md)  
10.4 — [Substitution and Integration by Parts](chapter-10/10.04-substitution-and-integration-by-parts.md)  
10.5 — [Discounting Continuous Payment Streams](chapter-10/10.05-discounting-continuous-payment-streams.md)  
10.6 — [Improper Integrals and Infinite Horizons](chapter-10/10.06-improper-integrals-and-infinite-horizons.md)  
10.7 — [Numerical Quadrature](chapter-10/10.07-numerical-quadrature.md)  
10.8 — [Discrete versus Continuous Payments](chapter-10/10.08-discrete-versus-continuous-payments.md)  
10.9 — [Chapter Project — Continuous Cash-Flow Valuation Engine](chapter-10/10.09-continuous-cash-flow-valuation-engine.md)  
10.10 — Exercises and Applied Problems

# Chapter 11 — Vectors and Financial Quantities

11.1 — [Vectors, Components, and Labels](chapter-11/11.01-vectors-components-and-labels.md)  
11.2 — [Vector Addition and Scalar Multiplication](chapter-11/11.02-vector-addition-and-scalar-multiplication.md)  
11.3 — [Inner Products and Valuation](chapter-11/11.03-inner-products-and-valuation.md)  
11.4 — [Norms and Distances](chapter-11/11.04-norms-and-distances.md)  
11.5 — [Orthogonality and Angles](chapter-11/11.05-orthogonality-and-angles.md)  
11.6 — [Projection onto a Direction](chapter-11/11.06-projection-onto-a-direction.md)  
11.7 — [Portfolio Weights and Exposure Constraints](chapter-11/11.07-portfolio-weights-and-exposure-constraints.md)  
11.8 — [Shape, Broadcasting, and Alignment Checks](chapter-11/11.08-shape-broadcasting-and-alignment-checks.md)  
11.9 — [Chapter Project — Vectorized Portfolio Exposure Calculator](chapter-11/11.09-chapter-project-vectorized-portfolio-exposure-calculator.md)  
11.10 — [Exercises and Applied Problems](chapter-11/11.10-exercises-and-applied-problems.md)

# Chapter 12 — Matrices and Linear Systems

12.1 — [Matrices and Dimensions](chapter-12/12.01-matrices-and-dimensions.md)  
12.2 — [Matrix Multiplication and Transformations](chapter-12/12.02-matrix-multiplication-and-transformations.md)  
12.3 — [Transpose, Identity, and Diagonal Matrices](chapter-12/12.03-transpose-identity-and-diagonal-matrices.md)  
12.4 — [Linear Systems and Elimination](chapter-12/12.04-linear-systems-and-elimination.md)  
12.5 — [Rank and Existence of Solutions](chapter-12/12.05-rank-and-existence-of-solutions.md)  
12.6 — [Inverse and Determinant](chapter-12/12.06-inverse-and-determinant.md)  
12.7 — [Condition Numbers and Perturbations](chapter-12/12.07-condition-numbers-and-perturbations.md)  
12.8 — [Residuals and Financial Interpretation](chapter-12/12.08-residuals-and-financial-interpretation.md)  
12.9 — [Chapter Project — Exposure Matching Linear Solver](chapter-12/12.09-chapter-project-exposure-matching-linear-solver.md)  
12.10 — Exercises and Applied Problems

# Chapter 13 — Vector Spaces, Projections, and Least Squares

13.1 — [Span and Linear Combinations](chapter-13/13.01-span-and-linear-combinations.md)  
13.2 — [Independence, Bases, and Dimension](chapter-13/13.02-independence-bases-and-dimension.md)  
13.3 — [Column Space and Null Space](chapter-13/13.03-column-space-and-null-space.md)  
13.4 — [Orthogonal Projection onto a Subspace](chapter-13/13.04-orthogonal-projection-onto-a-subspace.md)  
13.5 — [Least-Squares Objectives](chapter-13/13.05-least-squares-objectives.md)  
13.6 — [QR Factorization and Stable Solvers](chapter-13/13.06-qr-factorization-and-stable-solvers.md)  
13.7 — [Weighted Least Squares and Units](chapter-13/13.07-weighted-least-squares-and-units.md)  
13.8 — [Rank Deficiency and Regularization](chapter-13/13.08-rank-deficiency-and-regularization.md)  
13.9 — [Chapter Project — Least-Squares Replication Analyzer](chapter-13/13.09-chapter-project-least-squares-replication-analyzer.md)  
13.10 — [Exercises and Applied Problems](chapter-13/13.10-exercises-and-applied-problems.md)

# Chapter 14 — Eigenvalues, Quadratic Forms, and Matrix Decompositions

14.1 — [Eigenvalues and Eigenvectors](chapter-14/14.01-eigenvalues-and-eigenvectors.md)  
14.2 — [Symmetric Matrices and Spectral Decomposition](chapter-14/14.02-symmetric-matrices-and-spectral-decomposition.md)  
14.3 — [Quadratic Forms](chapter-14/14.03-quadratic-forms.md)  
14.4 — [Positive Definite and Semidefinite Matrices](chapter-14/14.04-positive-definite-and-semidefinite-matrices.md)  
14.5 — [Cholesky Factorization](chapter-14/14.05-cholesky-factorization.md)  
14.6 — [Singular Value Decomposition](chapter-14/14.06-singular-value-decomposition.md)  
14.7 — [Low-Rank Approximation](chapter-14/14.07-low-rank-approximation.md)  
14.8 — [Decomposition Validation and Interpretation](chapter-14/14.08-decomposition-validation-and-interpretation.md)  
14.9 — [Chapter Project — Quadratic Exposure and Decomposition Lab](chapter-14/14.09-chapter-project-quadratic-exposure-and-decomposition-lab.md)  
14.10 — Exercises and Applied Problems

# Chapter 15 — Multivariable Calculus

15.1 — [Functions of Several Variables](chapter-15/15.01-functions-of-several-variables.md)  
15.2 — [Partial Derivatives](chapter-15/15.02-partial-derivatives.md)  
15.3 — [Total Differentials and the Chain Rule](chapter-15/15.03-total-differentials-and-the-chain-rule.md)  
15.4 — [Gradients and Directional Derivatives](chapter-15/15.04-gradients-and-directional-derivatives.md)  
15.5 — [Jacobians of Vector Functions](chapter-15/15.05-jacobians-of-vector-functions.md)  
15.6 — [Hessians and Mixed Partials](chapter-15/15.06-hessians-and-mixed-partials.md)  
15.7 — [Multivariable Taylor Approximation](chapter-15/15.07-multivariable-taylor-approximation.md)  
15.8 — [Level Sets and Sensitivity Interpretation](chapter-15/15.08-level-sets-and-sensitivity-interpretation.md)  
15.9 — [Chapter Project — Multi-Input Valuation Sensitivity Engine](chapter-15/15.09-chapter-project-multi-input-valuation-sensitivity-engine.md)  
15.10 — Exercises and Applied Problems

# Chapter 16 — Unconstrained Optimization and Convexity

16.1 — [Objectives and Decision Variables](chapter-16/16.01-objectives-and-decision-variables.md)  
16.2 — [Stationary Points and First-Order Conditions](chapter-16/16.02-stationary-points-and-first-order-conditions.md)  
16.3 — [Second-Order Classification](chapter-16/16.03-second-order-classification.md)  
16.4 — [Convex Sets and Convex Objectives](chapter-16/16.04-convex-sets-and-convex-objectives.md)  
16.5 — [Gradient Descent](chapter-16/16.05-gradient-descent.md)  
16.6 — [Newton and Quasi-Newton Methods](chapter-16/16.06-newton-and-quasi-newton-methods.md)  
16.7 — [Scaling, Initial Guesses, and Local Methods](chapter-16/16.07-scaling-initial-guesses-and-local-methods.md)  
16.8 — [Calibration Residuals and Validation](chapter-16/16.08-calibration-residuals-and-validation.md)  
16.9 — [Chapter Project — Deterministic Calibration Optimizer](chapter-16/16.09-chapter-project-deterministic-calibration-optimizer.md)  
16.10 — Exercises and Applied Problems

# Chapter 17 — Constrained Optimization

17.1 — [Feasible Sets and Constraint Types](chapter-17/17.01-feasible-sets-and-constraint-types.md)  
17.2 — [Equality Constraints and Lagrange Multipliers](chapter-17/17.02-equality-constraints-and-lagrange-multipliers.md)  
17.3 — [Inequality Constraints and KKT Conditions](chapter-17/17.03-inequality-constraints-and-kkt-conditions.md)  
17.4 — [Active Constraints and Complementarity](chapter-17/17.04-active-constraints-and-complementarity.md)  
17.5 — [Linear Programming](chapter-17/17.05-linear-programming.md)  
17.6 — [Quadratic Programming](chapter-17/17.06-quadratic-programming.md)  
17.7 — [Financial Allocation Assumptions](chapter-17/17.07-financial-allocation-assumptions.md)  
17.8 — [Feasibility and Independent Optimality Checks](chapter-17/17.08-feasibility-and-independent-optimality-checks.md)  
17.9 — [Chapter Project — Constrained Allocation Decision Engine](chapter-17/17.09-chapter-project-constrained-allocation-decision-engine.md)  
17.10 — [Exercises and Applied Problems](chapter-17/17.10-exercises-and-applied-problems.md)

# Chapter 18 — Numerical Methods and Computational Reliability

18.1 — [Error Taxonomy](chapter-18/18.01-error-taxonomy.md)  
18.2 — Floating-Point Arithmetic and Cancellation  
18.3 — Bracketing and Bisection  
18.4 — Newton and Safeguarded Root Finding  
18.5 — Multiple Roots and Cash-Flow Equations  
18.6 — Interpolation and Extrapolation  
18.7 — Numerical Differentiation and Integration  
18.8 — Stopping Rules and Diagnostics  
18.9 — Chapter Project — Financial Numerical Solver and Diagnostics  
18.10 — Exercises and Applied Problems

# Chapter 19 — Differential Equations and Continuous-Time Models

19.1 — Differential Models and Initial Conditions  
19.2 — Separable Equations  
19.3 — Linear First-Order Equations  
19.4 — Equilibria and Local Stability  
19.5 — Euler Time Stepping  
19.6 — Runge-Kutta and Adaptive Solvers  
19.7 — Depletion, Events, and Boundary Rules  
19.8 — Validation and Discrete-Time Comparison  
19.9 — Chapter Project — Continuous Account Growth and Depletion Simulator  
19.10 — Exercises and Applied Problems

# Chapter 20 — Testing and Validating Mathematical Models

20.1 — Model Validation and Software Verification  
20.2 — Known-Value and Analytic Benchmarks  
20.3 — Financial and Mathematical Invariants  
20.4 — Boundary and Invalid Inputs  
20.5 — Floating-Point Tolerances  
20.6 — Property and Metamorphic Checks  
20.7 — Reproducibility and Evidence  
20.8 — Review Findings and Release Gates  
20.9 — Chapter Project — Mathematical Model Validation Dossier  
20.10 — Exercises and Applied Problems

# Chapter 21 — Integrated Capstone: Financial Mathematics Foundations Toolkit

21.1 — Capstone Requirements and Assumptions  
21.2 — Architecture and Module Interfaces  
21.3 — Cash-Flow and Rate Module  
21.4 — Sensitivity and Approximation Module  
21.5 — Linear Algebra and Replication Module  
21.6 — Optimization and Feasibility Module  
21.7 — Continuous-Time Module and Scenario Report  
21.8 — Testing, Documentation, and Transition to Book 03  
21.9 — Chapter Project — Financial Mathematics Foundations Toolkit  
21.10 — Exercises and Applied Problems

---

## Structure Change Policy

Preserve the exact chapter and section numbers/titles during manuscript development. Renaming, adding, removing, or reordering established entries requires an explicit agreed change, a recorded TOC version update, and reconciliation of affected manuscript and progress indexes. Do not silently renumber or orphan published files.

## Version History

- **v1.0 — 2026-10-22:** Established the 21-chapter curriculum and complete numbered section sequence. Publication begins with this TOC; manuscript work proceeds one section at a time.

**Next manuscript section:** 18.2 — Floating-Point Arithmetic and Cancellation.
