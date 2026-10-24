# Book 2 — Mathematical Foundations for Finance with Python

## Master Table of Contents v1.0

**Status:** Established curriculum for section-by-section development.  
**Version date:** 2026-10-22.  
**Scope:** 21 chapters; complete numbered section plan.  
**Manuscript status:** Sections 1.1–1.15, 2.1–2.10, and 3.1–3.10, and 4.1–4.2 published as Draft. Runtime validation remains pending for Sections 2.8–2.10, 3.1–3.10, and 4.1–4.2; later sections are Planned.

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
4.3 — Logarithm Rules and Their Domains  
4.4 — Discrete and Continuous Compounding  
4.5 — Solving for Time and Growth Rate  
4.6 — Products and Additive Log Changes  
4.7 — Stable Evaluation Near Zero  
4.8 — Growth Assumptions and Model Limits  
4.9 — Chapter Project — Growth and Rate Conversion Explorer  
4.10 — Exercises and Applied Problems

# Chapter 5 — Sequences, Recurrences, and Financial Growth

5.1 — Sequences and Time Indexing  
5.2 — Arithmetic and Geometric Sequences  
5.3 — First-Order Balance Recurrences  
5.4 — Closed Forms from Repeated Substitution  
5.5 — Fixed Points and Equilibria  
5.6 — Convergence and Stability  
5.7 — Variable Rates and Payment Schedules  
5.8 — Withdrawal and Depletion Boundaries  
5.9 — Chapter Project — Contribution and Withdrawal Recurrence Engine  
5.10 — Exercises and Applied Problems

# Chapter 6 — Summation, Series, and Cash-Flow Derivations

6.1 — Summation and Product Notation  
6.2 — Finite Geometric Sums  
6.3 — Infinite Geometric Series  
6.4 — Ordinary Annuities and Annuities Due  
6.5 — Growing Payment Streams  
6.6 — Perpetuities and Tail Conditions  
6.7 — Truncation and Approximation Error  
6.8 — Zero Rates and Independent Verification  
6.9 — Chapter Project — Cash-Flow Series Derivation and Verification Engine  
6.10 — Exercises and Applied Problems

# Chapter 7 — Limits and Continuity

7.1 — Limits and Approaching a Point  
7.2 — One-Sided Limits  
7.3 — Continuity and Types of Discontinuity  
7.4 — Limits at Infinity and Asymptotes  
7.5 — Exponential Limits and Continuous Compounding  
7.6 — Important Small-Change Limits  
7.7 — Intermediate Values and Root Existence  
7.8 — Numerical Investigation versus Proof  
7.9 — Chapter Project — Boundary and Continuity Investigation Lab  
7.10 — Exercises and Applied Problems

# Chapter 8 — Derivatives and Differentiation

8.1 — The Derivative as a Limit  
8.2 — Power, Sum, and Constant Rules  
8.3 — Product and Quotient Rules  
8.4 — The Chain Rule  
8.5 — Exponential and Logarithmic Derivatives  
8.6 — Higher Derivatives and Curvature  
8.7 — Implicit Differentiation  
8.8 — Numerical Derivatives and Step Selection  
8.9 — Chapter Project — Analytic and Numerical Derivative Comparator  
8.10 — Exercises and Applied Problems

# Chapter 9 — Financial Sensitivity and Taylor Approximation

9.1 — Absolute and Relative Sensitivity  
9.2 — Elasticity  
9.3 — First-Order Taylor Approximation  
9.4 — Second-Order Taylor Approximation  
9.5 — Remainder and Error Bounds  
9.6 — Discounted-Value Sensitivity  
9.7 — Kinks and One-Sided Sensitivities  
9.8 — Sensitivity Reports and Scenario Revaluation  
9.9 — Chapter Project — Valuation Sensitivity and Approximation Report  
9.10 — Exercises and Applied Problems

# Chapter 10 — Integration and Continuous Cash Flows

10.1 — Accumulation and Riemann Sums  
10.2 — Definite and Indefinite Integrals  
10.3 — The Fundamental Theorem of Calculus  
10.4 — Substitution and Integration by Parts  
10.5 — Discounting Continuous Payment Streams  
10.6 — Improper Integrals and Infinite Horizons  
10.7 — Numerical Quadrature  
10.8 — Discrete versus Continuous Payments  
10.9 — Chapter Project — Continuous Cash-Flow Valuation Engine  
10.10 — Exercises and Applied Problems

# Chapter 11 — Vectors and Financial Quantities

11.1 — Vectors, Components, and Labels  
11.2 — Vector Addition and Scalar Multiplication  
11.3 — Inner Products and Valuation  
11.4 — Norms and Distances  
11.5 — Orthogonality and Angles  
11.6 — Projection onto a Direction  
11.7 — Portfolio Weights and Exposure Constraints  
11.8 — Shape, Broadcasting, and Alignment Checks  
11.9 — Chapter Project — Vectorized Portfolio Exposure Calculator  
11.10 — Exercises and Applied Problems

# Chapter 12 — Matrices and Linear Systems

12.1 — Matrices and Dimensions  
12.2 — Matrix Multiplication and Transformations  
12.3 — Transpose, Identity, and Diagonal Matrices  
12.4 — Linear Systems and Elimination  
12.5 — Rank and Existence of Solutions  
12.6 — Inverse and Determinant  
12.7 — Condition Numbers and Perturbations  
12.8 — Residuals and Financial Interpretation  
12.9 — Chapter Project — Exposure Matching Linear Solver  
12.10 — Exercises and Applied Problems

# Chapter 13 — Vector Spaces, Projections, and Least Squares

13.1 — Span and Linear Combinations  
13.2 — Independence, Bases, and Dimension  
13.3 — Column Space and Null Space  
13.4 — Orthogonal Projection onto a Subspace  
13.5 — Least-Squares Objectives  
13.6 — QR Factorization and Stable Solvers  
13.7 — Weighted Least Squares and Units  
13.8 — Rank Deficiency and Regularization  
13.9 — Chapter Project — Least-Squares Replication Analyzer  
13.10 — Exercises and Applied Problems

# Chapter 14 — Eigenvalues, Quadratic Forms, and Matrix Decompositions

14.1 — Eigenvalues and Eigenvectors  
14.2 — Symmetric Matrices and Spectral Decomposition  
14.3 — Quadratic Forms  
14.4 — Positive Definite and Semidefinite Matrices  
14.5 — Cholesky Factorization  
14.6 — Singular Value Decomposition  
14.7 — Low-Rank Approximation  
14.8 — Decomposition Validation and Interpretation  
14.9 — Chapter Project — Quadratic Exposure and Decomposition Lab  
14.10 — Exercises and Applied Problems

# Chapter 15 — Multivariable Calculus

15.1 — Functions of Several Variables  
15.2 — Partial Derivatives  
15.3 — Total Differentials and the Chain Rule  
15.4 — Gradients and Directional Derivatives  
15.5 — Jacobians of Vector Functions  
15.6 — Hessians and Mixed Partials  
15.7 — Multivariable Taylor Approximation  
15.8 — Level Sets and Sensitivity Interpretation  
15.9 — Chapter Project — Multi-Input Valuation Sensitivity Engine  
15.10 — Exercises and Applied Problems

# Chapter 16 — Unconstrained Optimization and Convexity

16.1 — Objectives and Decision Variables  
16.2 — Stationary Points and First-Order Conditions  
16.3 — Second-Order Classification  
16.4 — Convex Sets and Convex Objectives  
16.5 — Gradient Descent  
16.6 — Newton and Quasi-Newton Methods  
16.7 — Scaling, Initial Guesses, and Local Methods  
16.8 — Calibration Residuals and Validation  
16.9 — Chapter Project — Deterministic Calibration Optimizer  
16.10 — Exercises and Applied Problems

# Chapter 17 — Constrained Optimization

17.1 — Feasible Sets and Constraint Types  
17.2 — Equality Constraints and Lagrange Multipliers  
17.3 — Inequality Constraints and KKT Conditions  
17.4 — Active Constraints and Complementarity  
17.5 — Linear Programming  
17.6 — Quadratic Programming  
17.7 — Financial Allocation Assumptions  
17.8 — Feasibility and Independent Optimality Checks  
17.9 — Chapter Project — Constrained Allocation Decision Engine  
17.10 — Exercises and Applied Problems

# Chapter 18 — Numerical Methods and Computational Reliability

18.1 — Error Taxonomy  
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

**Next manuscript section:** 4.3 — Logarithm Rules and Their Domains.
