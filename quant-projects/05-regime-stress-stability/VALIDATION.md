# Project 05 — Validation record (2026-11-08)

An initial locally authored prototype failed four of seven tests due to unsupported pandas `DatetimeIndex.dayofweek.ne` usage. After replacing it with an array comparison, **7/7 local prototype tests passed**. The prototype's synthetic CLI completed 364 scored weeks and six scenarios, with illustrative wealth per $1: baseline 1.1762, zero cost 1.1851, 25-bps cost 1.1631, 50% shrinkage 1.1343.

The published implementation was streamlined from the locally tested prototype; its exact GitHub revision has **not yet been executed or independently verified**. A dedicated GitHub Actions job is the next acceptance gate. No real market data was fetched or redistributed; no production certification.
