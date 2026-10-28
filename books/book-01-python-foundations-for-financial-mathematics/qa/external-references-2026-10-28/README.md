# Book 1 — External-Reference Availability and Attribution Audit

**Date:** 2026-10-28. **Reviewer / correction owner:** Codex. **Base revision:** `0dac315c88b081bae421807b5102422e08036b4e`. Corrected source hashes are retained in [source-manifest.json](source-manifest.json), and the source changes are published with this evidence. **V03: PASS for the explicit-URL, publisher/topic and version-registration scope below.** Comprehensive source, mathematical, legal and copyright acceptance remains pending.

## Scope and results

The inventory covers explicit HTTP(S) Markdown links in Book 1 manuscripts, companion solutions, indexes and QA Markdown. Repository-internal main-branch links remain part of V02. Plain filenames, unlinked bibliography entries and URLs inside code are not represented as audited citations.

| Check | Initial snapshot | Corrected snapshot |
|---|---:|---:|
| Markdown documents inventoried | 381 | 382 |
| External link occurrences | 1030 | 1046 |
| Distinct cited URLs, including fragments | 283 | 287 |
| Distinct HTTP request URLs | 254 | 259 |
| Successful request targets | 252 | 259 |
| Targets returning 404 | 2 | 0 |
| Cited fragments found | 40 | 41 |
| Missing cited fragments | 1 | 0 |

[Initial summary](initial-summary.json), [initial requests](initial-requests.json) and [initial URL results](initial-url-results.json) preserve the original failures. The [final summary](final-summary.json), [request records](final-requests.json), [URL/fragment results](final-url-results.json) and [occurrence inventory](occurrences.json) preserve the corrected results. Successful responses are availability observations at the recorded timestamps, not guarantees of future availability or of claim correctness.

## Corrections and source currency

- **F20 — Model-risk guidance:** Section 20.14 now cites the Federal Reserve's SR 26-2, dated April 17, 2026. The Fed expressly identifies SR 11-7 and SR 21-8 as superseded. The official SR 11-7 attachment is retained only as labelled historical background. The added context separates the banking guidance's applicability from the chapter's educational present-value example; no regulatory-compliance approval is implied.
- **F21 — Treasury:** six references to the former interest-rate landing path returned 404. They now point to Treasury's current Interest Rate Statistics page. Relevant curve sections also cite the methodology and FAQ, which distinguish par-yield quotation conventions from zero/spot discounting.
- **F22 — Python dictionary anchor:** two citations used an anchor absent from the moving Python documentation. They now use the Python 3.12 mapping-types anchor, matching the runtime family used in the recorded tests; the anchor was found.
- **F23 — Attribution:** broad CFA home/research portal citations were replaced with specific public material on TWR methodology, probability and rebalancing. The MWR section gained a specific GIPS methodology source. Investor.gov and FINRA labels now identify the actual corporate-bond and stocks/dividends pages. GIPS landing-page links are explicitly labelled background portals, and a NumPy label no longer implies a financial-functions package.

[corrections.json](corrections.json) records the changed manuscripts, hashes and actions. The relevant primary sources were checked directly:

- [Federal Reserve SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm)
- [Treasury Interest Rate Statistics](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics)
- [Treasury Yield Curve Methodology](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/treasury-yield-curve-methodology)
- [Treasury Interest Rates FAQ](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/interest-rates-frequently-asked-questions)
- [Python 3.12 mapping types](https://docs.python.org/3.12/library/stdtypes.html#mapping-types-dict)
- [GIPS Standards Handbook for Firms](https://www.gipsstandards.org/standards/gips-standards-for-firms/gips-standards-handbook-for-firms/)
- [CFA probability reading: public introduction and learning outcomes](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/probability-trees-and-conditional-expectations)
- [CFA asset-allocation reading: public rebalancing summary](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-asset-allocation)

## Attribution and version review

[publisher-topic-review.json](publisher-topic-review.json) records all 259 request targets across 28 domains, with citation labels, recognized publishers, source roles, topic alignment and version policy. The review separates 108 direct API identifiers from general project documentation, government/investor education, textbook material, public course summaries, historical guidance and background portals. API identifier checks compare the requested symbol with the returned title/heading; other topic/label metadata and the substantive replacement sources were reviewed at the documented scope.

The register identifies 115 version-family/release-pinned documentation URLs and 109 moving-documentation URLs. Moving routes such as stable/latest or Python's generic version path can describe versions newer than the recorded runtime. Their availability does not establish compatibility; V04 must reconcile supported dependencies and version-sensitive behavior. A Python minor-version documentation path can also incorporate later patch-release documentation.

The CFA refresher references use only the public introduction, learning outcomes or summary; full member readings are not represented as reviewed. GIPS portal links are background navigation, not a claim that a particular equation is specified there or that the project complies with GIPS. The OpenStax book landing page has a generic dynamic title; the book identity is corroborated by the two cited, explicitly titled chapter pages.

This publisher/topic review is not sentence-by-sentence proof of every manuscript claim, independent economic validation, legal applicability analysis or permission to reproduce source content. Those broader reviews remain V07/V14 work.

## Method and reproduction

The parser uses markdown-it-py 4.0.0 and mdurl 0.1.2 under Python 3.12.14. The probe uses bounded HTTPS GET requests, normal certificate validation, sixteen workers and at most two simultaneous requests per host. Each request records UTC time, HTTP status, final URL, redirects, content type, retained-body hash and relevant title/anchor metadata. Request timeout is eighteen seconds; at most 2 MiB of body is retained in memory per target. Full source bodies are not published. The RFC 9110 response exceeded that limit, so its hash covers the retained prefix only; no complete-source identity or full-text review is inferred from that hash.

A 200 response with an error/challenge title is flagged for review. HTTP 401/403/429 are classified as access restrictions, not broken links; 404/410 are missing candidates; transport failures remain inconclusive. No access restrictions or network-inconclusive targets remained in the corrected inventory. Cited HTML fragments are checked against returned IDs/names; a failed, truncated or non-HTML response is not silently accepted as an anchor pass.

Successful probes from this audit date were reused for unchanged targets; only changed/new request targets were fetched after correction. Original timestamps and response hashes remain in the records. The script's optional cache is restricted to successful probes from the same UTC date.

From the repository root, choose a fresh output directory:

```sh
python -m venv /tmp/book1-reference-env
/tmp/book1-reference-env/bin/python -m pip install -r books/book-01-python-foundations-for-financial-mathematics/qa/external-references-2026-10-28/requirements.txt
/tmp/book1-reference-env/bin/python books/book-01-python-foundations-for-financial-mathematics/qa/external-references-2026-10-28/audit_external.py . /tmp/book1-reference-results
```

The optional fourth command argument is a prior `requests.json` file for same-date successful-probe reuse. Live responses and future counts can differ. The probe exits nonzero for unresolved availability or fragment findings. The [auditor self-checks](selftest-results.json) passed twelve controlled checks for success, redirects, 404s, restrictions, soft errors, HTML metadata, bounded reads and retained-byte hashes. Run them with:

```sh
/tmp/book1-reference-env/bin/python books/book-01-python-foundations-for-financial-mathematics/qa/external-references-2026-10-28/audit_selftest.py books/book-01-python-foundations-for-financial-mathematics/qa/external-references-2026-10-28/audit_external.py /tmp/book1-reference-selftest.json
```

[code-preservation.json](code-preservation.json) confirms that existing fenced code and the locked Master TOC are unchanged. The source edits alter references, labels and the guidance-currency paragraph; no new run of all reference tests is claimed. Structural/internal-link validation was rerun after the edits and is recorded in [structure-recheck.json](structure-recheck.json).

**Next:** V04 — Python syntax, dependency and supported-version validation. Broader progress remains in [VALIDATION-TRACKER.md](../VALIDATION-TRACKER.md).
