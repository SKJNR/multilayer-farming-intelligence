# AI teammate session-start prompt

You are contributing to the integrated farming intelligence product. Before proposing code or architecture changes:

1. Read `CROSS_REPO_DECISION_HANDOFF.md`, the MFI repo's `README.md` + `CURRENT_STATE.md` + active PR #1 diff, and the GWL repo's `PROJECT_STATE.md` + latest relevant `download/DECISION_LOG.md` addenda + active PR #5 diff.
2. Establish exact branch/commit status before asserting what is implemented. Separate merged main from open PR branches and specs from executable code.
3. Do not confuse global Total Water Storage (TWS) competition work with local groundwater-level (GWL) forecasting.
4. Treat GWL as a limited contextual signal. Do not infer prediction probabilities from expected-weight evaluation scores; do not apply numeric local-recharge multipliers without a separately preregistered prospective evaluation.
5. Treat synthetic outputs as synthetic. Passing software tests does not imply physical validity, field calibration or farmer impact.
6. Review hard blockers: LER definition, parameter provenance and units, physical equations/forcing method, particle-filter state alignment, pond sensing vs measurements, unknown/negation handling, SAT/constraint-solver naming and evidence claims.
7. Cross-AI proposals are proposals, not founder directives. Cite the exact commit and file/line being changed. Role “hats” are review lenses, not independent agents unless separately invoked.
8. End your contribution with a concise decision log: changed files/diff, evidence/source refs, commands/tests actually run and results, unverified claims, risks, open questions and next step. Never claim tests or agent work you did not execute.
