# Book 1 — Python Foundations for Financial Mathematics

## Master Table of Contents v1.0 — APPROVED AND LOCKED

**Status:** Authoritative  
**Approved:** 2026-08-27  
**Scope:** Complete Book 1 structure  
**Change policy:** Do not renumber, rename, add, remove, or reorder chapters/sections without explicit approval and a recorded TOC version change.

## Editorial Workflow

Every substantive manuscript section follows:

**Draft → Technical + Source Review → Production + Copyright Review → Revised Final / Canonical Edition**

Canonical manuscripts retain verified references. Python behavior should preferentially use official Python documentation; NumPy, pandas, SciPy, Matplotlib, and Jupyter behavior should use official project documentation; financial theory should use authoritative textbooks, standards, regulators, exchanges, central banks, or recognized academic sources as appropriate. Exposition, examples, exercises, tables, and diagrams should be independently developed unless reuse is explicitly licensed and attributed.

---

# Chapter 1 — Introduction to Python for Financial Mathematics

1.1 — What Is Financial Mathematics?  
1.2 — Why Python for Financial Mathematics?  
1.3 — Python in Finance and Quantitative Computing  
1.4 — Financial Mathematics vs. Quantitative Finance vs. Financial Engineering  
1.5 — Setting Up the Python Environment  
1.6 — Your First Python Program for Financial Mathematics  
1.7 — Python Variables, Data Types, and Financial Data Representation  
1.8 — Operators and Financial Calculations  
1.9 — Expressions, Precedence, and Mathematical Translation  
1.10 — Working with Financial Inputs and Outputs  
1.11 — Numerical Precision, Rounding, and Tolerances  
1.12 — Chapter Project — Basic Financial Calculator  
1.13 — Exercises and Applied Problems

# Chapter 2 — Python Control Flow for Financial Models

2.1 — Boolean Expressions and Financial Conditions  
2.2 — Comparison and Logical Operators  
2.3 — `if`, `elif`, and `else`  
2.4 — Modeling Financial Decision Rules  
2.5 — `for` Loops  
2.6 — `while` Loops  
2.7 — Iterating Across Cash Flows and Periods  
2.8 — `range()` and Financial Time Periods  
2.9 — Nested Control Flow  
2.10 — `break`, `continue`, and Loop Control  
2.11 — Defensive Input Validation  
2.12 — Chapter Project — Investment Scenario Analyzer  
2.13 — Exercises and Applied Problems

# Chapter 3 — Functions and Reusable Financial Models

3.1 — Why Functions Matter in Financial Computing  
3.2 — Defining and Calling Functions  
3.3 — Parameters and Arguments  
3.4 — Return Values  
3.5 — Default and Keyword Arguments  
3.6 — Variable Scope  
3.7 — Type Hints for Financial Functions  
3.8 — Docstrings and Financial Assumptions  
3.9 — Designing Present- and Future-Value Functions  
3.10 — Reusable Rate and Discounting Functions  
3.11 — Function Composition  
3.12 — Pure Functions and Reproducibility  
3.13 — Testing Financial Functions  
3.14 — Chapter Project — Financial Mathematics Function Library  
3.15 — Exercises and Applied Problems

# Chapter 4 — Python Data Structures for Financial Information

4.1 — Financial Data as Structured Information  
4.2 — Lists  
4.3 — Tuples  
4.4 — Dictionaries  
4.5 — Sets  
4.6 — Nested Financial Structures  
4.7 — List and Dictionary Comprehensions  
4.8 — Sorting and Filtering Financial Records  
4.9 — Representing Cash-Flow Schedules  
4.10 — Representing Securities and Portfolios  
4.11 — Mutable vs. Immutable Data  
4.12 — Choosing Appropriate Data Structures  
4.13 — Chapter Project — Portfolio Holdings Manager  
4.14 — Exercises and Applied Problems

# Chapter 5 — Modules, Packages, Environments, and Reproducibility

5.1 — Python Modules  
5.2 — Importing Modules  
5.3 — The Python Standard Library  
5.4 — Creating Financial Utility Modules  
5.5 — Python Packages  
5.6 — `pip` and Dependency Management  
5.7 — Virtual Environments  
5.8 — Dependency Pinning and Reproducibility  
5.9 — Project Directory Structure  
5.10 — Configuration and Environment Separation  
5.11 — Reproducible Financial Research  
5.12 — Chapter Project — Reusable Financial Python Package  
5.13 — Exercises and Applied Problems

# Chapter 6 — NumPy for Financial Mathematics

6.1 — Why NumPy?  
6.2 — NumPy Arrays  
6.3 — Array Creation and Data Types  
6.4 — Indexing and Slicing  
6.5 — Vectorized Financial Calculations  
6.6 — Broadcasting  
6.7 — Aggregation and Statistical Operations  
6.8 — Cash-Flow Vectors  
6.9 — Return Vectors  
6.10 — Portfolio Weight Vectors  
6.11 — Matrices and Financial Models  
6.12 — Linear Algebra with NumPy  
6.13 — Random Number Generation  
6.14 — Numerical Precision and NumPy  
6.15 — Performance: Python Loops vs. Vectorization  
6.16 — Chapter Project — Vectorized Portfolio Calculator  
6.17 — Exercises and Applied Problems

# Chapter 7 — pandas for Financial Data Analysis

7.1 — Why pandas?  
7.2 — `Series`  
7.3 — `DataFrame`  
7.4 — Indexing and Selection  
7.5 — Reading Financial Data  
7.6 — Data Types and Conversion  
7.7 — Missing Financial Data  
7.8 — Cleaning Financial Datasets  
7.9 — Date and Time Indexes  
7.10 — Sorting, Filtering, and Querying  
7.11 — Grouping and Aggregation  
7.12 — Joining and Merging Financial Data  
7.13 — Resampling Time Series  
7.14 — Rolling and Expanding Calculations  
7.15 — Price-to-Return Transformation  
7.16 — Multi-Asset Datasets  
7.17 — Chapter Project — Financial Time-Series Analyzer  
7.18 — Exercises and Applied Problems

# Chapter 8 — Visualization for Financial Mathematics

8.1 — Why Visualization Matters  
8.2 — Matplotlib Fundamentals  
8.3 — Line Charts  
8.4 — Financial Time-Series Charts  
8.5 — Return Charts  
8.6 — Histograms and Return Distributions  
8.7 — Scatter Plots and Relationships  
8.8 — Portfolio Visualizations  
8.9 — Payoff Diagrams  
8.10 — Interest and Investment Growth Curves  
8.11 — Sensitivity and Scenario Charts  
8.12 — Effective Financial Chart Design  
8.13 — Chapter Project — Financial Analytics Dashboard  
8.14 — Exercises and Applied Problems

# Chapter 9 — Time Value of Money with Python

9.1 — The Time Value of Money  
9.2 — Financial Timelines  
9.3 — Simple Interest  
9.4 — Compound Interest  
9.5 — Present Value  
9.6 — Future Value  
9.7 — Discount Factors  
9.8 — Multiple Cash Flows  
9.9 — Net Present Value  
9.10 — Effective vs. Nominal Rates  
9.11 — Compounding Frequency  
9.12 — Continuous Compounding  
9.13 — Solving for Rate  
9.14 — Solving for Time  
9.15 — Python TVM Functions  
9.16 — Chapter Project — Time Value of Money Engine  
9.17 — Exercises and Applied Problems

# Chapter 10 — Cash Flows, Annuities, and Perpetuities

10.1 — Cash-Flow Mathematics  
10.2 — Cash-Flow Timelines  
10.3 — Level Annuities  
10.4 — Ordinary Annuities  
10.5 — Annuities Due  
10.6 — Deferred Annuities  
10.7 — Growing Annuities  
10.8 — Perpetuities  
10.9 — Growing Perpetuities  
10.10 — Present and Future Values of Payment Streams  
10.11 — Irregular Cash Flows  
10.12 — NPV  
10.13 — IRR and Numerical Root Finding  
10.14 — Chapter Project — Cash-Flow Valuation Engine  
10.15 — Exercises and Applied Problems

# Chapter 11 — Loans, Mortgages, and Amortization

11.1 — Loan Mathematics  
11.2 — Principal, Rate, Term, and Payment  
11.3 — Level-Payment Loans  
11.4 — Solving for Payment  
11.5 — Interest and Principal Components  
11.6 — Outstanding Loan Balance  
11.7 — Amortization Schedules  
11.8 — Mortgages  
11.9 — Extra Payments and Prepayment  
11.10 — Refinancing Analysis  
11.11 — Effective Borrowing Cost  
11.12 — Numerical and Rounding Considerations  
11.13 — Chapter Project — Loan and Mortgage Analyzer  
11.14 — Exercises and Applied Problems

# Chapter 12 — Fixed-Income Mathematics and Bond Analytics

12.1 — Introduction to Fixed Income  
12.2 — Bond Cash Flows  
12.3 — Coupon Bonds  
12.4 — Zero-Coupon Bonds  
12.5 — Bond Pricing  
12.6 — Yield to Maturity  
12.7 — Yield and Price Relationships  
12.8 — Accrued Interest and Clean vs. Dirty Price  
12.9 — Duration  
12.10 — Modified Duration  
12.11 — Convexity  
12.12 — Interest-Rate Sensitivity  
12.13 — Yield Curves  
12.14 — Discount Factors and Spot Rates  
12.15 — Forward Rates  
12.16 — Chapter Project — Bond Analytics Engine  
12.17 — Exercises and Applied Problems

# Chapter 13 — Returns and Investment Performance

13.1 — Measuring Investment Returns  
13.2 — Simple Returns  
13.3 — Gross Returns  
13.4 — Logarithmic Returns  
13.5 — Multi-Period Returns  
13.6 — Annualization  
13.7 — Dividends and Total Return  
13.8 — Arithmetic vs. Geometric Mean Return  
13.9 — Time-Weighted Return  
13.10 — Money-Weighted Return  
13.11 — Volatility  
13.12 — Drawdowns  
13.13 — Risk-Adjusted Performance Concepts  
13.14 — Chapter Project — Investment Performance Analyzer  
13.15 — Exercises and Applied Problems

# Chapter 14 — Probability for Financial Mathematics

14.1 — Why Probability Matters in Finance  
14.2 — Sample Spaces and Events  
14.3 — Probability Rules  
14.4 — Conditional Probability  
14.5 — Independence  
14.6 — Random Variables  
14.7 — Discrete Random Variables  
14.8 — Continuous Random Variables  
14.9 — Expected Value  
14.10 — Variance and Standard Deviation  
14.11 — Covariance and Correlation  
14.12 — Common Probability Distributions  
14.13 — Normal Distribution  
14.14 — Sampling with Python  
14.15 — Random Number Generation and Reproducibility  
14.16 — Chapter Project — Financial Probability Simulator  
14.17 — Exercises and Applied Problems

# Chapter 15 — Statistics for Financial Data

15.1 — Descriptive Statistics  
15.2 — Mean, Median, and Quantiles  
15.3 — Variance and Standard Deviation  
15.4 — Skewness and Kurtosis  
15.5 — Covariance  
15.6 — Correlation  
15.7 — Sampling and Estimation  
15.8 — Confidence Intervals  
15.9 — Hypothesis Testing Foundations  
15.10 — Linear Regression  
15.11 — Financial Return Statistics  
15.12 — Rolling Statistics  
15.13 — Statistical Pitfalls in Financial Data  
15.14 — Chapter Project — Financial Statistical Analysis Toolkit  
15.15 — Exercises and Applied Problems

# Chapter 16 — Portfolio Mathematics

16.1 — Portfolio Fundamentals  
16.2 — Portfolio Weights  
16.3 — Portfolio Return  
16.4 — Expected Portfolio Return  
16.5 — Covariance Matrices  
16.6 — Portfolio Variance  
16.7 — Portfolio Volatility  
16.8 — Diversification  
16.9 — Two-Asset Portfolios  
16.10 — Multi-Asset Portfolios  
16.11 — Correlation and Diversification  
16.12 — Efficient Portfolio Concepts  
16.13 — Portfolio Constraints  
16.14 — Rebalancing Mathematics  
16.15 — Chapter Project — Portfolio Risk and Return Engine  
16.16 — Exercises and Applied Problems

# Chapter 17 — Numerical Methods with SciPy

17.1 — Why Numerical Methods Are Needed  
17.2 — Closed-Form vs. Numerical Solutions  
17.3 — Numerical Root Finding  
17.4 — Solving Yield and IRR Problems  
17.5 — Optimization Fundamentals  
17.6 — Constrained Optimization  
17.7 — Portfolio Optimization  
17.8 — Numerical Integration  
17.9 — Interpolation  
17.10 — Curve Construction Concepts  
17.11 — Numerical Stability  
17.12 — Convergence and Error  
17.13 — Validation of Numerical Results  
17.14 — Chapter Project — Financial Numerical Solver  
17.15 — Exercises and Applied Problems

# Chapter 18 — Monte Carlo Simulation for Finance

18.1 — Simulation Fundamentals  
18.2 — Random Number Generators  
18.3 — Reproducible Simulation  
18.4 — Simulating Financial Outcomes  
18.5 — Return Simulations  
18.6 — Price-Path Simulation  
18.7 — Scenario Analysis  
18.8 — Monte Carlo Estimation  
18.9 — Convergence  
18.10 — Confidence and Simulation Error  
18.11 — Portfolio Simulation  
18.12 — Risk Simulation  
18.13 — Computational Performance  
18.14 — Chapter Project — Monte Carlo Financial Simulator  
18.15 — Exercises and Applied Problems

# Chapter 19 — Financial Data Engineering Foundations

19.1 — Financial Data Sources and Formats  
19.2 — CSV and Text Data  
19.3 — JSON Data  
19.4 — Excel Data  
19.5 — APIs and Financial Data  
19.6 — Parsing and Validation  
19.7 — Schema and Data Types  
19.8 — Missing and Invalid Values  
19.9 — Date and Timestamp Normalization  
19.10 — Currency and Unit Normalization  
19.11 — Data Quality Checks  
19.12 — Reproducible Data Pipelines  
19.13 — Avoiding Look-Ahead and Data Leakage  
19.14 — Chapter Project — Financial Data Pipeline  
19.15 — Exercises and Applied Problems

# Chapter 20 — Testing and Engineering Financial Python

20.1 — Why Financial Code Must Be Tested  
20.2 — Assertions and Known-Value Tests  
20.3 — Unit Testing  
20.4 — Boundary and Edge Cases  
20.5 — Testing Floating-Point Results  
20.6 — Testing Decimal Calculations  
20.7 — Financial Invariants  
20.8 — Input Validation  
20.9 — Exception Handling  
20.10 — Logging  
20.11 — Type Hints  
20.12 — Documentation  
20.13 — Reproducibility  
20.14 — Model Validation vs. Software Validation  
20.15 — Chapter Project — Production-Quality Financial Library  
20.16 — Exercises and Applied Problems

# Chapter 21 — Integrated Capstone: Financial Mathematics Toolkit

21.1 — Capstone Architecture  
21.2 — Requirements and Assumptions  
21.3 — Project Structure  
21.4 — Numerical and Decimal Policies  
21.5 — Time-Value-of-Money Module  
21.6 — Cash-Flow Module  
21.7 — Loan Module  
21.8 — Bond Module  
21.9 — Return and Performance Module  
21.10 — Portfolio Module  
21.11 — Statistical Module  
21.12 — Simulation Module  
21.13 — Data Validation Layer  
21.14 — Visualization Layer  
21.15 — Testing and Verification  
21.16 — Documentation and Reproducibility  
21.17 — Final Integrated Case Study  
21.18 — Further Study and Transition to Book 2

---

# Locked Structure Policy

This 21-chapter structure is the authoritative **Book 1 Master TOC v1.0**. Existing canonical manuscripts 1.1–1.7 align with this structure and must not be silently renumbered or retitled. Future manuscript work must use the exact section numbers and titles in this file.

Any structural change requires:

1. Explicit approval.
2. A documented rationale.
3. A new Master TOC version.
4. Reconciliation of affected manuscript/status indexes.
5. Verification that canonical files are not silently orphaned, overwritten, or renumbered.

**Next locked manuscript section: 1.8 — Operators and Financial Calculations.**
