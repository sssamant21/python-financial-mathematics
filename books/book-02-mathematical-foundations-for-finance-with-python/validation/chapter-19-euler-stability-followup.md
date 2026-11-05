# Section 19.5 — Observed Euler decay and stability boundaries

Date: 2026-11-05. Unchanged implementation inspected at `91fc2035f500543aac8695628b8dba68db3ec475`. Checker revision: `36006c921c0c005f2812e0589f2b68e64dfc17b4`.

[Runnable checker](../chapter-19/code/check_euler_decay_stability.py) observes six actual four-step Euler paths. Exact rational amplification powers verify every callback time/state and final update. Cases cover positive and negative decaying factors, immediate extinction, the nondecaying −1 boundary, and unstable growth. The strict abs(1+h*lambda)<1 classification agrees with each reference. Three altered state/count/status records are rejected.

The initial audit passed; no numerical helper changed. [Raw evidence](chapter-19-euler-stability-followup.json) retains observations and source hashes. Run from chapter-19/code. The final Chapter 19 scope compiled 24 sources and passed 14 scripts. This is selected dyadic evidence; it does not establish arbitrary ODE stability, smoothness or financial-model validity.
