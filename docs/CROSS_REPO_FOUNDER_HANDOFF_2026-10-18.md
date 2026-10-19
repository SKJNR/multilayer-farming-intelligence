# Cross-repository founder handoff — farming intelligence + groundwater-aware advisory

**Prepared:** 2026-10-19. **Decision context captured through:** 2026-10-18.  
**Status:** Integrated architecture and prioritized work plan. This document does **not** assert that all components are implemented or field-validated.

## 1. The goal

Build a practical farming decision system for farmers in Andhra Pradesh/Telangana that can reason about single crops, intercrops and multilayer systems while making groundwater/weather risk, constraints, uncertainty and evidence visible. It should give useful Telugu-first farmer assistance through a low-friction channel such as WhatsApp/FPO-supported workflows, while collecting properly consented feedback and measurements.

The system is not merely a crop simulator, not merely a groundwater model, and not an LLM that invents prescriptions. It is a governed pipeline in which data services, a provenance-aware knowledge base, deterministic rules, crop-system simulation and farmer feedback each have explicit responsibilities.

## 2. Repository snapshot and source-of-truth order

- MFI repository: `SKJNR/multilayer-farming-intelligence`, main at `a6b3f45e77aa36c6748271858178522070be61a7` (2026-10-15). Open [PR #1](https://github.com/SKJNR/multilayer-farming-intelligence/pull/1), head `e7378b9dcd9eaceb880834a7cd8056837f1f46bb`.
- GWL/Agri-TWS repository: `SKJNR/agri-tws-ind`, main at `ca5819b019f93c9abb0b6a3acd2dc31e21f053c0` (2026-10-10). Open [PR #5](https://github.com/SKJNR/agri-tws-ind/pull/5), head `e2d673515b2318a331b82e2db602e6c01e081529`. [PR #4](https://github.com/SKJNR/agri-tws-ind/pull/4) for Addendum 21.3 is merged.
- MFI starting point: `README.md`, `CURRENT_STATE.md`, `docs/validation/real-world-readiness-roadmap.md`, `docs/validation/field-data-protocol.md`, relevant decision records, and PR #1 diff.
- GWL starting point: `PROJECT_STATE.md`, `download/DECISION_LOG.md`, `worklog.md`, `download/ADDENDUM21_SCOPE_PREREGISTRATION.md`, `download/task98_addendum21_1/ADDENDUM21_1_AMENDMENT.md`, relevant issues, and PR #5 diff.

The MFI README and newer PR branch documentation may not describe identical states. Where they conflict, inspect the actual branch/commit and label the status. Do not treat PR descriptions or archived AI reports as proof of current executable behavior.

## 3. Target architecture and data flow

1. **Farmer/site context intake:** capture location and its precision, soil/profile evidence, crop history, sowing/harvest window, available irrigation/well observations, current crops, labor/capital, goals and constraints. Unknown values stay unknown; ask only the most decision-relevant follow-up or use a safe fallback.
2. **Weather and groundwater context:** retrieve/cache date-stamped data with area, horizon, latest observation, source, resolution, freshness and known limitations. Separate measured readings, official reporting, model-derived covariates, farmer self-report, estimates and inference.
3. **Agricultural knowledge base (AKB):** source-backed and context-aware crop, soil, pest/disease, management and water-risk knowledge. Each card should retain source references, geography/context, evidence tier, translation/reviewer state, cautions and status. A global analogue needs local triangulation or an explicit no-local-validation label.
4. **Candidate generator:** produce a bounded set of candidate monocrop/intercrop/multilayer systems and management options based on season, crop compatibility and local availability. Avoid an unbounded universal optimizer claim in MVP.
5. **Hard constraints first:** check sowing window, compatibility/rotation/pathogen conflicts, roots and soil depth, light/shade, aeration/waterlogging sensitivity, water requirement/access, physical spacing, labor and budget. Hard constraints are not soft LLM suggestions.
6. **Process-based reference simulation:** simulate feasible candidates under reproducible and bounded soil/weather/irrigation scenarios. Return model version, parameter provenance, scenario range, diagnostics and uncertainty—not just a point estimate.
7. **Decision/ranking layer:** present trade-offs across water risk, timing, likely performance range, economic assumptions, labor, uncertainty and evidence tier. Never conceal a constraint violation inside a weighted score.
8. **Delivery and feedback:** render the structured result in plain Telugu/WhatsApp-friendly terms: what is recommended and why, what could make it fail, what is unknown, what to monitor, and when to ask a human expert. Capture farmer choice, management and observed outcomes with consent.
9. **Shadow evaluator:** compare forecasts and simulated advice to newly observed data; track coverage, stale data, errors, referrals and drift. Promote autonomy only after a pre-registered gate passes; keep rollback and human review available.

### Separation of responsibilities

- GWL service: regional/well-level risk context and data freshness, not crop choice.
- AKB: sourced knowledge and practice descriptions, not fabricated farmer-specific model output.
- MFI: feasible crop-system candidates, process simulation and trade-offs.
- Deterministic tools: units, arithmetic, threshold checks and fixed protocol enforcement.
- LLM: language understanding, clarifying questions, retrieval orchestration and explanation. It must not invent scientific constants, silently calculate doses, override hard constraints or rewrite model probabilities.

## 4. Groundwater model status and binding guardrails

The GWL project’s Task 95/Addendum 20 record reports lane-dependent expected-weight scores:

- AP-12: 0.6964; registered CI lower bound 0.6095 exceeds the 0.60 gate.
- Pooled-45: 0.5982, missing the 0.60 threshold by 0.0018.
- Telangana TS-32: 0.5541.
- The recorded AP persistence baseline is very strong and the project notes an era/persistence issue, hence “blend-not-replacement” rather than replacing local/persistence signals universally.

These are **expected-weight scores, not percent accuracy**, and not proof of probability calibration for every district/horizon. Cite the repository’s Task 95 / Addendum 20 artifact if repeating the numbers. Evaluation is mixed; no evidence here establishes that integrated crop advice has improved actual field outcomes.

Binding rules:

- Do not portray the GWL model as equally skillful for every state/district/horizon.
- Do not convert an evaluation score into a prediction probability.
- Do not apply a heuristic numeric “local recharge multiplier” to model tercile probabilities. Ponds, tanks, local recharge works and farmer observations can be described as contextual signals and monitoring prompts, but cannot numerically change calibrated model output without a new preregistered forward-evaluation lane.
- Where current well observations conflict with a forecast, display the conflict, date and provenance rather than silently choosing one.
- Never re-tune repeatedly against an already-consumed sealed test era. Use a prospective/independent holdout for future model changes.
- Stale/missing model input must trigger explicit fallback language rather than a confident substitute.

### GWL-to-MFI contract required before end-to-end integration

At minimum define: location/well identifier and spatial resolution; forecast issue time; target month/horizon; model/version; actual output fields; state/district/horizon skill/evidence tier and known caveats; most recent observation time/source; freshness and coverage; uncertainty; provenance categories; conflict/fallback semantics. Do not pass raw training metadata as a prediction interface.

## 5. MFI scientific and engineering review gates

The following are code-review findings/risks to verify at the active PR head and disposition explicitly:

1. **Land Equivalent Ratio (LER):** summing heuristic relative-yield fractions is not valid LER. Define same-basis monocrop reference yields, compatible area/time/management basis, and corresponding intercrop yields. Label unsupported yield inputs as illustrative until locally calibrated.
2. **Crop parameter provenance:** maturity dates, rooting, canopy/light traits, density, yield, price and costs need units, geography/management context, source, validity ranges, uncertainty and status (measured/sourced/estimated/inferred/unknown). Example JSON parameters must not masquerade as universal truth.
3. **Physical model vs bookkeeping:** near-zero mass residual only indicates bookkeeping consistency, not correct constitutive equations or field accuracy. Freeze equations, units, time-step convention, flux definitions and boundary conditions; test them independently.
4. **Method names:** label the actual interpolation/ET method. Do not call inverse-distance weighting kriging or call an approximate ET method FAO-56 Penman–Monteith if it is not that implementation.
5. **Particle filter alignment:** review the suspected mismatch where canopy/turgor summary may be computed before resampling but then paired with post-resampled state; add deterministic regression tests.
6. **Pond perception:** optical/SAR values alone do not establish measured pond depth, accessible storage or a guaranteed water budget. Separate sensed feature, model inference and measured observation.
7. **Unknown/negation handling:** do not default missing crop/pond into a positive assertion. “No pond” must not match “pond available”; ambiguous context should lead to clarification, abstention or an explicitly cautious generic answer.
8. **SAT naming/correctness:** a handwritten rule/enumeration checker is not a formal SAT/MaxSAT solver unless a real encoding/solver and evidence exist. Name it a constraint checker or evaluate a real solver (e.g. OR-Tools CP-SAT) with feasibility certificates/explanations and tests. Solver feasibility is not agronomic validity.
9. **Claims in PR #1:** tie claims about exact physics, identifiability, speed, zero cost, test counts and solver guarantees to source/tests at that exact PR commit. Passing CI is software evidence, not crop-model validation.
10. **Documentation status mismatch:** make the README accurately distinguish the documentation-only shared decision package, candidate source code, open feature PR and field-validation status. Avoid conflicting statements about whether executable source is present.

## 6. Scientific research and LLM-assisted synthetic generation

LLMs may propose literature queries, extract candidate values into reviewable cards, suggest edge-case families, and explain simulator behavior. They are not the authority for scientific values and must not produce unlabeled synthetic target labels.

Recommended audited workflow:

1. Register equations/parameters with source URL or DOI, unit, range, site/crop context, dependencies, version, evidence tier and review status.
2. Use bounded, seeded sampling. Preserve linked soil hydraulic properties and plausible parameter correlations; include rare-but-valid conditions. Separate deliberate invalid-input fixtures from valid scientific scenarios.
3. Define scenario families explicitly: normal, drought, extreme rain/runoff, heat, waterlogging/aeration stress, delayed sowing, irrigation loss, varied soil profile/root depth, and uncertainty in management/forcing.
4. Execute the versioned reference simulator; save source/code version, parameter hash, random seed, forcing data version, full outputs and diagnostics.
5. Test mass balance, units, positivity/bounds, boundary conditions, monotonic/metamorphic behavior and scenario coverage. Run sensitivity analysis (e.g. SALib) to identify influential or unidentifiable parameters; use property-based tests (e.g. Hypothesis) for invariant testing.
6. Label generated records `synthetic` and trace their generating scenario. Never present the count of generated scenarios as field evidence.
7. Calibrate and evaluate on independent observed data: soil moisture/profile, local weather/irrigation, crop phenology and outcomes where measured. Use separate plots/seasons/events for evaluation and preregister criteria.
8. Build an ML surrogate only after a real inference workload is measured and a benchmark shows a meaningful net benefit while preserving constraint/physics behavior. The current direction is explicit reference simulator first, surrogate deferred unless justified.

Useful model families/data sources to investigate (not auto-approved): APSIM/DSSAT/STICS/WaNuLCAS and related intercrop-capable models; FAO crop calendar/CROPWAT/AquaCrop; ICAR/ANGRAU/PJTSAU/ICAR-CRIDA/APCNF; ICRISAT and other semi-arid analog evidence. Check whether a model actually supports the intended species/intercrop process and verify licenses, source, local applicability and boundary conditions before adoption.

## 7. Farmer delivery and data collection

Ship early value through a **shadow/supervised pilot**, not autonomous unvalidated prescriptions. Start with source-backed advice, real dated weather/well context when available, deterministic constraints, explicit uncertainty, observation prompts and a correction path. Avoid presenting synthetic yield/risk results as certain or claiming impact before observation.

With farmer consent and data minimization, record: input snapshot, source/version and freshness, recommendations/options, farmer choice/action, sowing/planting date, irrigation/rain notes, management practice, labor/cost where the farmer agrees, crop/soil observations and harvest/outcome. Use field-data protocol templates; template headers are not collected measurements.

Pilot gates should include: data quality/coverage, calibration on relevant local observations, independent forward evaluation, baseline comparison by geography/horizon/crop, usability and comprehension in Telugu, safety/referral performance, drift monitoring, stale-input behavior and rollback. Do not widen crop/geography scope before these pass.

## 8. MVP sequence

**P0 — trustworthy foundation:** reconcile PR #1 against the real-world-readiness review; fix misleading LER; enforce provenance/units/status; fix unknown/negation and soft-sensor alignment; name SAT capability correctly; lock simulator equations and tests.

**P1 — narrow integration:** version GWL↔MFI schema; pull fresh context from cached, date-stamped GWL/weather service; generate a bounded shortlist for selected local crop systems; hard constraints first; return water-risk/scenario trade-offs with caveats.

**P2 — farmer pilot:** Telugu-first WhatsApp/FPO delivery, shadow evaluation, field protocol, observation feedback and human review. Promote only evidence-backed capabilities.

**P3 — expansion:** add crop/soil plugins and wider districts; revisit real SAT/CP-SAT, knowledge graph details, computer vision and surrogate ML only when workload/evidence justify each cost.

## 9. Collaboration protocol for ChatGPT, Qwen, GLM and other contributors

- Read this handoff and the repo’s canonical state file plus active PR diff at session start.
- GitHub is shared memory only after the record is committed; no private chat is automatically visible to another model.
- Cross-AI proposals must cite exact commit and file/line they amend and describe the observed current state first. “Founder directives” quoted from an AI are proposals until the founder accepts them.
- Distinguish `PROPOSED`, `REPORTED—ARTIFACTS MISSING`, `REPRODUCIBLE CLAIM—NOT RE-RUN HERE`, `INDEPENDENTLY VERIFIED SOFTWARE TEST`, and `FIELD-VALIDATED` evidence. Do not collapse those categories.
- Assign distinct reviewer hats (agronomy/soil physics, groundwater/hydrology, ML evaluation, software testing, data provenance, farmer UX/safety, adversarial reviewer) but do not claim the hats are independent subagents unless separately invoked.
- End each work session with: decisions, evidence/source refs, diff/files, commands/tests actually run, unresolved blockers, next action and any founder gates. No unlogged chat-only decisions.

## 10. Acceptance criteria for the cross-repo plan

- Versioned GWL↔MFI contract and stale/missing/conflicting-data fallbacks implemented and tested.
- Crop/soil/management parameters and output claims have auditable units/source/context/status.
- P0 code-review findings have executable tests or explicit documented dispositions.
- Synthetic outputs are labeled, reproducible and do not substitute for measured local validation.
- A narrow supervised pilot has a measurement plan, consent/data handling, preregistered evaluation and human escalation.
- No README, PR description or farmer UX implies synthetic-only code is field-validated.

## 11. Knowledge base, retrieval and three-audience UX — related decisions to carry forward

The overall platform scope also includes a source-grounded agricultural knowledge base and different UI workflows for three audiences. These are connected layers, but should not be forced into one giant MVP release.

### Knowledge base vs decision engine

- Knowledge is organized around a **crop/enterprise × condition/problem × evidence-backed practice/response**. For plant issues, records should distinguish crop and variety where known, growth stage, symptom, differential diagnosis, context, source, confidence/evidence tier, treatment method, cautions, local applicability and required human escalation. A crop name alone is not a diagnosis.
- Separate **knowledge cards** (what credible sources report), **rules/constraints** (what must or must not be suggested), **simulator primitives** (what can be calculated), and **predictive models** (what has measured predictive skill). Do not mix these into one untyped vector index.
- The discussion referenced a possible “38-method” recharge knowledge base versus a broader knowledge graph. Keep this as a scope decision: first define a reusable card schema and curate a small, high-value, locally relevant recharge-method family. Do not assert that a number of methods is complete or authoritative until the list, sources, duplicates, site prerequisites and safety review are in the repo.
- Reuse existing datasets and reference records where allowed; do not recreate tables without a clear gap. Keep source registry entries for owner, URL, license/access constraints, update cadence, geographic resolution and which claim the source can support.
- Local Andhra/Telangana and ICAR/ANGRAU/PJTSAU/APCNF/ICRISAT evidence outranks a global climate analogue when claims conflict. Global analogs can explain mechanisms or offer conditional comparisons only with explicit analog context and a “not locally validated” label if no local triangulation exists.
- Groundwater recharge advice must not promise fixed percentage improvements or imply a single structure is suitable without rainfall/runoff, soil, geology/aquifer, slope, land status, safe siting and professional review. Contextual farmer reports are not a calibrated numeric multiplier.

### Source ingestion and Telugu quality

- The companion specification proposes a schema-validated AKB with stable IDs, source references, confidence/evidence tier, Telugu text and a state preventing machine-drafted translations from being served before human sign-off.
- Proposed PDF-ingestion choice in the companion research: evaluate local OSS tooling such as Docling as primary candidate and pdfplumber/OCR as fallback before lock-in. The registered 20-document eval (messy/scanned PDFs, Telugu and tables) is a **gate to run**, not a completed evaluation. Do not treat a tooling preference as an empirical win until that test is run and logged.
- Hybrid structured SQL plus vector retrieval may be appropriate, but retrieval similarity is not a calibrated probability. Use citation-or-silence, an explicit FULL/PARTIAL/NONE coverage label, a Telugu gold set and an empirically evaluated recall/precision gate—not a universal fixed “0.7 confidence” threshold.
- No model-generated Telugu translation becomes a citable knowledge source on its own. Machine text may assist drafting; a competent human must attest the final advisory content and gold-set test should include local vocabulary, units, crop names and dialect variation.

### Three role-specific interaction patterns

1. **Farmer app / WhatsApp / voice:** Telugu-first, low typing burden; ask the minimum critical clarifying questions; display short recommendation options and why, data date/source, what is uncertain, what to inspect/measure next and the feedback button/voice reply. Do not overwhelm with raw hydrogeology statistics or solver internals. Offer offline/low-connectivity-friendly capture and clear escalation when the evidence is insufficient.
2. **FPO worker console:** a human-owned queue with risk flags, missing context, structured callback questions, referral status/SLA and feedback entry. The FPO view supports—not silently replaces—human follow-up. Emergency referrals remain in the registered human-owned process; do not introduce unapproved parallel alert channels.
3. **Surveyor / groundwater department / professional view:** technical packet with station or well identifier/distance, observation and fetch time, historical measurements, model horizon/limits, source/custody, farmer-reported well history, siting constraints and an auditable elicitation/referral log. Do not elevate the advisory model to autonomous recharge-siting authority until its separate concordance/calibration gates are met.

An internal **KB editor/reviewer** workflow is also necessary even if it is not a fourth farmer-facing customer app: source attribution, schema validation, Telugu review, versioning, change log and publish approval. Do not let raw external PDFs or LLM outputs flow straight into serving.

### Model/agent architecture and cost control

- For MVP, prefer a single governed state-graph (LangGraph-style) that calls deterministic tools and retrieval behind typed contracts. The prior product spec deliberately defers a multi-agent runtime such as CrewAI/AutoGen because of latency, cost, nondeterminism and debugging complexity.
- Use specialist “hats” and adversarial reviewers offline for design/code review. Record each reviewer’s actual input, findings, severity, evidence and disposition. Do not label simulated debate as independent multi-agent execution or count consensus as validation.
- Keep the shadow evaluator asynchronous so it does not consume the farmer interaction latency budget; prove the rule-based v0 against a gold set before considering an LLM-assisted grey-zone tier. Keep logs purpose-limited and route alerts through the existing human-owned queue.
- Voice/Indic language should be a separately measured lane. Compare an API/service option such as Bhashini against a self-hostable/open-model option such as AIKosh using the same R-TG1-style Telugu gold set for speech recognition, translation/transliteration and TTS, and include latency, quality, per-advisory cost, production access terms and data-handling terms. Any provider availability or commercial terms must be re-verified at implementation time.

### Data-source caution

Some land/asset/crop datasets can support boundaries, acreage, scheme/water-resource inventory or crop-history/stress context without measuring groundwater level, soil hydraulics or aquifer properties. Do not infer groundwater level, soil texture or infiltration from an administrative polygon or a crop-history layer alone. Each dataset needs an explicit “can support / cannot support” register and a local validation plan.

These UX, AKB and agent-governance items are **related scope to preserve**, not a claim that the apps, RAG index, Telugu gold set, Bhashini integration, recharge-method catalogue or automatic siting functionality already exist end-to-end.
