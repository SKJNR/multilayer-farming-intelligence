# DR-004.1 — Reference Freeze and Generator Coverage

**Status:** reference-freeze decision recorded; reported repair metrics are not independently verified here.

## Decision

Freeze a reproducible reference version of the explicit simulator to stabilise testing, and keep it distinct from an agronomically validated production recommendation engine. Defer the surrogate. Repair scenario-generation and evaluation coverage before further modeling.

## Reported repairs

A subsequent AI-submitted report claimed:

- a timing audit using 10,000 steps over 10 repetitions, mean 0.1971 seconds or 19.71 microseconds/step;
- 1,000/1,000 PAW-derived soil records passed a parameter-ordering constraint;
- a Normal, Storm and Aeration_Test scenario family each exercised some runoff/aeration events;
- a frozen reference name `v1.0.0-ref`.

The timing protocol, soil sample and scenario-family outcomes are reported in the conversation, but the actual code/log files have not been attached to this repository. The timing number also differs from prior estimates; only a fresh run using committed artifacts can reconcile that difference.

## What a frozen reference means

Freeze means source, version, dependencies and tests are versioned so later changes can be compared. It does not imply empirical calibration, broad physical validity, or suitability for farmer recommendations.

## Next gate

Acquire/commit actual source and logs; independently rerun tests; confirm realistic scenario coverage; then design calibration/evaluation against appropriate observations. Do not block the knowledge-base design forever, but do not let synthetic-only simulator outputs masquerade as field-validated facts.
