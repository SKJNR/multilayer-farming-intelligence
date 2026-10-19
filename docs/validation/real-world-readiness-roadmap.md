# Real-World Readiness Roadmap — Multilayer Farming Intelligence

**Status:** PROPOSED validation plan; not a field-validation certificate.  
**Baseline inspected:** GitHub `main` commit `a6b3f45e77aa36c6748271858178522070be61a7`.  
**Target primitive:** two-layer daily soil-water balance, initially motivated by shallow annual + deeper perennial root competition (example: groundnut + papaya).  
**Decision:** suitable for reproducible software experimentation; **not ready for farmer-facing recommendations**.

## 1. What the current results do and do not establish

The committed candidate includes an explicit daily flux order, two-layer storage, a simplified drought/aeration stress modifier, proportional allocation of top-layer water among evaporation and crop demands, deep drainage, and a per-step profile water-balance residual. A local rerun from the archive whose Git `HEAD` matched the inspected GitHub commit passed its existing tests. A separate seeded stress run over 2,000 generated illustrative profiles × 30 days also maintained storage bounds and small bookkeeping residuals; this is synthetic software evidence, not evidence that the flux equations describe a real field.

The generator is **not** an implementation of Saxton–Rawls or Rosetta. It generates transparent illustrative priors and couples its conductivity prior to sand fraction by a deliberately simple rule. It is not a locally validated soil-hydraulic distribution or a vertically differentiated soil-profile generator. The current `step()` requires daily potential evaporation, groundnut transpiration, papaya transpiration, and papaya root fractions as inputs; it does not derive these from weather, crop stage, canopy, or measured root profiles. Explicit rainfall and irrigation inputs are now distinguished, but event-intensity infiltration, preferential/lateral flow, capillary rise, salt effects, dynamic roots, and mechanistic hydraulic curves remain outside scope.

Important distinctions:

- **Mass balance** tests whether accounting is closed; it does not validate drainage, infiltration, uptake, or stress laws.
- **Parameter ordering** is a validity predicate, not evidence that a parameter combination belongs to a real soil.
- **Synthetic scenario coverage** is not out-of-sample field performance.
- **Calibration fit** is not independent validation.
- **A waterlogging proxy** is not a plant-disease or mortality model. Do not infer *Phytophthora* disease from simulated moisture alone.
- Timing numbers apply only to the stated code, environment, and workload; speed is not scientific validity.

## 2. Evidence gates (do not skip or merge them)

| Gate | Required work | Pass evidence | Not allowed before pass |
|---|---|---|---|
| **G0 — Source and provenance** | Keep the newly authored candidate separate from the unrecovered historical `v1.0.0-ref`; recover historical scripts and logs where possible; reconcile source hashes; pin environment and commands. | Commit SHA, source, dependency lock, seeds, exact commands, raw logs, input/output artifacts, checksums. | Calling the candidate the historical implementation or asserting the historical benchmark was reproduced. |
| **G1 — Software and numerical verification** | Validate finite inputs/parameters, storage bounds, non-negative fluxes, balance terms, units, boundary cases, irrigation, and deterministic replay. Run regression, metamorphic, randomized, and extreme-value tests in CI. | Tests and randomized checks pass on a clean environment; tolerance and failure cases documented; checksum manifest excludes volatile caches. | Treating a passing test suite as physical validation. |
| **G2 — Conceptual/model verification** | Freeze the equation specification: state variables, units, timestep, order of operations, stress-state time, infiltration/runoff boundary, drainage laws, crop uptake allocation, and omitted processes. Compare with an independently implemented analytical/reference case. | Equation-to-code traceability, hand-checkable fixtures, reviewed counterexamples, versioned decision record. | Tuning parameters to compensate for unclear or incorrect equations. |
| **G3 — Soil and crop parameter provenance** | Obtain field/lab parameter measurements where feasible; otherwise use a cited PTF with versioned inputs, uncertainty, applicability limits, and transformation equations. Measure or justify layer boundaries, hardpan depth, root-depth/root-fraction profiles, and crop-stage demands. | Each parameter has value, unit, source/method, timestamp/context, uncertainty, and evidence class. | Treating illustrative generator values or map pixels as measured plot truth. |
| **G4 — Forcing and observation pipeline** | Synchronize daily rainfall, irrigation, reference ET/weather, crop stage, management events, and soil-moisture observations. Build and test the adapter that converts these into model demand inputs. | Validated data dictionary, QA report, missingness/time-zone rules, unit conversions, event records, and immutable raw data version. | Running a farm replay from unlabeled or undocumented inputs. |
| **G5 — Calibration and identifiability** | Pre-register calibration parameters, bounds/priors, observables, error model, objective, and regime windows. Fix depths from measurement wherever possible. Use sensitivity/Jacobian/profile or posterior diagnostics to expose unidentifiable parameters. | Calibration report with parameter uncertainty, residual plots, parameter correlations, wet-event and dry-down analysis, and a frozen calibration dataset. | Claiming a unique physical parameter value where the observations identify only a combination (for example, a drainage product). |
| **G6 — Independent validation** | Evaluate on entire held-out fields, seasons, or storms—not random daily rows from the same trajectories. Compare with persistence/simple baselines and, where fit-for-purpose, an independent process model. Freeze acceptance metrics before opening holdout results. | Pre-registered metrics, confidence intervals, per-layer bias/MAE/RMSE, event/tail diagnostics, coverage of predictive intervals, and documented failures. | Describing calibration-set performance as generalization or changing pass criteria after seeing the holdout. |
| **G7 — Shadow mode and decision utility** | Run predictions prospectively without allowing them to control farm actions. Have an agronomist and participating farmer review events, uncertainty, feasibility, and false alarms. Test fallback behavior and rollback. | Pre-defined utility/risk thresholds met on new observations, safety review, intervention feasibility, and prospective audit trail. | Autonomous or confident farmer-facing interventions based on the current prototype. |
| **G8 — Limited release and monitoring** | Publish model card, supported domain, prohibited uses, monitoring, version rollback, feedback capture, and recalibration triggers. Preserve every prediction with its model/input versions. | Signed release checklist and post-release monitoring/incident process. | Expanding to new soils, crops, irrigation regimes, or diseases without new evaluation. |

## 3. First real-world question must be narrow

Do not start by asking the simulator to predict “yield” or “farm success.” First define a target such as:

> Given a measured two-horizon soil profile, observed daily rainfall and irrigation, and explicitly sourced crop water-demand inputs, can the model predict volumetric soil moisture in each horizon and the timing/magnitude of wetting and dry-down events on a new plot?

This question matches the current state variables more closely. Yield, survival, root disease, profitability, and an intervention recommendation are downstream claims and require separate outcome models and evaluation.

Before field collection, choose the crop system, soil/management domain, decision supported, forecast horizon, and cost of false wet/dry alarms. If those are undecided, the experiment is still exploratory and should not be presented as validation.

## 4. Field pilot design

### 4.1 Start with measurement feasibility, then power the validation

A small pilot should first prove that farmers can keep records, sensors are calibrated, timestamps align, and field events are captured. If the previously discussed 10-field Anantapur pilot is selected, treat it as a **feasibility/heterogeneity pilot**, not automatically as a statistically powered validation sample. Use pilot variance and the intended error tolerance to plan a confirmatory sample size. Select plots deliberately across measured soil texture/profile, restrictive-layer status, management/irrigation regime, and wet/dry exposure rather than assuming one district has one soil type.

Record the actual soil profile; do not assign “Alfisol,” red soil, hardpan, or rooting depth from geography alone. Do not pool rainfed and irrigated plots without representing their inputs.

### 4.2 Minimum measurements per plot

1. **Site/horizon:** pseudonymous site and plot IDs; profile/horizon top and bottom depths; sand/silt/clay; bulk density; organic matter or soil organic carbon (keep units distinct); coarse fragments if relevant; field/lab method; sampling date; water-retention measurements where feasible; saturated conductivity/infiltration test; restrictive-layer depth and measurement method.
2. **Weather and water management:** daily plot rainfall from a gauge if possible; each irrigation event and measured/applied depth; instrument failures; reference ET or meteorological variables with source and calculation version. Store official/reanalysis gridded data separately from local gauge data and label them as estimates/proxies.
3. **Soil moisture:** calibrated volumetric water content with sensor ID, depth, timestamp, unit, calibration method, measurement uncertainty, missingness/failure flag, and occasional independent gravimetric check where feasible. Place observations to represent each modeled horizon; choose depths after the soil pit/profile survey rather than blindly copying defaults.
4. **Crop/management:** species, cultivar, planting date, spacing, stage/phenology, observed rooting information where practical, canopy/cover notes, mulch, pruning, weeding, soil amendments, pest/disease observations, harvest/yield, and deviations from the planned practice.
5. **Outcomes and context:** observed wetness/waterlogging and wilting with timestamp and protocol; farmer action and rationale; costs/labor only if evaluating a management decision. Record disease separately, with diagnosis/source; the current model does not predict pathogens.

Use the templates under `templates/field-pilot/`. Keep personal names and phone numbers out of research IDs. If coordinates or farm records could identify a participant, store them separately with access controls and consent; public examples should use coarse/obfuscated coordinates.

### 4.3 Sampling and sensor QA

- Install, read, and calibrate sensors according to manufacturer/lab protocol; retain calibration equations and raw readings.
- Log clock/time-zone, battery, sensor replacement, soil disturbance, and gaps. Never silently interpolate a major storm or sensor outage.
- Verify rain-gauge units and catch, distinguish rainfall from irrigation, and record irrigation timing where possible.
- Take soil samples by horizon and keep laboratory results tied to sample IDs and methods.
- Prefer measured field capacity/wilting/retention data if feasible. A PTF is a prior/estimate with uncertainty, not ground truth.
- Freeze data cleaning rules before evaluating model predictions. Preserve raw data unchanged and store derived data as a versioned transformation.

## 5. Parameterization and calibration rules

1. Treat layer depths as measured geometry where possible; do not freely fit depth to improve moisture RMSE.
2. Use a documented retention/conductivity method. A Rosetta-based workflow predicts van Genuchten-type hydraulic parameters from selected texture, bulk-density, and water-content inputs; deriving the candidate's field-capacity/wilting parameters must document matric-potential assumptions, unit conversions, version, and uncertainty. It is not a drop-in equivalent to the current illustrative generator.
3. Use SoilGrids or other maps to stratify sites and create prior ranges, not to replace plot-level soil sampling. Record the map version, depth interval, prediction quantiles, and known limitations.
4. Do not fit every parameter simultaneously. First fix measurable profile depths and known inputs. Determine which parameters observations identify; estimate only a defensible subset and retain ranges for confounded parameters.
5. Calibrate to measured moisture trajectories by horizon, not merely to the global mass residual. Evaluate wetting peaks, recession/dry-down slopes, bias by moisture regime, and uncertainty. If measurements are available only in the top layer, do not claim deep drainage or layer-2 parameters were validated.
6. Split data by complete plot/field/season/event. Reserve a genuinely untouched validation set before tuning. If sample size is too small, use grouped cross-validation for development, state the limitations, and collect new prospective observations before field claims.

## 6. Acceptance metrics must be pre-registered

For every modeled horizon, report at least MAE, RMSE, mean bias, sample size, missingness, measurement uncertainty, and residual plots. For event behavior, report peak wetting error, time-to-peak error, dry-down slope error, wet/dry threshold confusion where thresholds have a sourced meaning, and performance during the most decision-relevant storm/dry-spell cases. Compare with a persistence baseline and any suitable independent model. Report uncertainty intervals and failures by site/soil/regime, not only pooled averages.

Do **not** set a universal numeric pass threshold before you know sensor uncertainty, the intended decision, and the cost of a false alarm. Use the measurement-feasibility pilot to estimate observation noise, then preregister tolerances with agronomy/soil-science input **before** the holdout is scored. Include a go/no-go decision and what new evidence would overturn it.

## 7. Review-team and multi-agent protocol

Use the existing `docs/protocol/agent-hats-and-debate-template.md`, plus these field-readiness pairings. For every high-risk workstream, assign a counter-reviewer explicitly; the same adversarial role can challenge several subagents, but every critical claim must have a concrete falsification attempt.

| Workstream lead / hat | Required adversarial counter-review |
|---|---|
| Agro-hydrology / soil physicist | Construct a storm, saturated profile, and restrictive-layer case where the assumed flux law fails. |
| Soil scientist / PTF steward | Search for implausible texture–retention–conductivity combinations and PTF extrapolation beyond its inputs. |
| Crop physiologist / agronomist | Challenge rooting fractions, crop-stage demand, stress functions, and transfer from single-crop evidence to intercropping. |
| Numerical methods / software engineer | Test alternative operator splitting, unit errors, non-finite values, bounds, and mass-ledger omissions. |
| Statistician / calibration lead | Try to break identifiability, split integrity, uncertainty coverage, and metric choice. |
| Field protocol / data QA lead | Look for sensor drift, rainfall/irrigation omissions, time misalignment, missing not at random, and label leakage. |
| Knowledge-graph/provenance steward | Trace every consequential parameter or claim to source, context, version, and uncertainty; detect estimates mislabeled as observations. |
| Farmer/deployment/economics reviewer | Stress-test labor, affordability, action reversibility, false alarms, and who bears the loss. |
| Release/safety moderator | Verify all gates are passed and ensure unsupported outputs cannot become confident recommendations. |

Recommended sequence: **step-back** (decision, users, loss); **Tree of Thoughts** (compare genuinely different modeling choices); **Graph of Thoughts** (map dependencies and feedback); independent first-pass reviews; **ReAct** evidence retrieval/tool execution; **PAL/PoT** runnable equations and tests; adversarial **chess-move** chains for second-order failure; self-consistency checks; then consensus *or recorded disagreement*. Do not force consensus. Agreement among models is not ground truth.

Treat the named roles as review hats unless separate people/models were actually invoked. When independent AI models are used, record model/tool/version, prompt/task, timestamp, raw report, and whether reviewers saw one another's conclusions. Do not publish hidden private chain-of-thought; preserve concise claims, evidence, calculations, counterexamples, tests, and decision summaries instead.

## 8. Required run artifact bundle

Every calibration/validation run must include:

- `run_manifest.json`: Git commit, model version/hash, environment/dependencies, command, seed, timestamp, units, scenario IDs, data versions, and configuration hash;
- immutable source observations and data dictionary, with consent/privacy and provenance notes;
- exact model input time series and the calculation/version used to derive crop demands and root fractions;
- predictions and fluxes by time step/layer, including rainfall, irrigation, runoff, inter-layer drainage, deep drainage, evaporation, crop uptake, and residual;
- test/QA output, per-site/per-event metrics, residual plots, confidence intervals, failed-case report, and calibration/holdout labels;
- `SHA256SUMS.txt` generated after all run artifacts are final, excluding `.git` and volatile Python/pytest caches.

The exact run must be rerunnable from the command recorded in the manifest. Preserve old runs; never overwrite a prediction after seeing the observed outcome.

## 9. Immediate next sprint

1. Recover and checksum the historical code/report artifacts, and keep the historical implementation separate from this candidate.
2. Close code-level issues and run clean tests/stress checks; generate the checksum manifest only after artifacts are stable.
3. Approve the first target question and the exact crop/soil/irrigation domain with a soil scientist/agronomist and a participating farmer.
4. Finalize templates, sensor plan, data consent/privacy, and forcing-input adapter; explicitly calculate or source crop water-demand inputs.
5. Run a measurement-feasibility pilot, preregister calibration and validation splits/metrics, then acquire the independent holdout.
6. Only after the evidence gates pass, consider shadow-mode decision support. Do not skip directly from a synthetic test to a farmer recommendation.

## 10. External reference starting points

These are reference inputs to investigate, not endorsements that they directly validate this model:

- NASA POWER Daily API: <https://power.larc.nasa.gov/docs/services/api/temporal/daily/> — gridded daily meteorological/solar products; compare against local gauges and keep source/resolution metadata.
- ISRIC SoilGrids documentation: <https://docs.isric.org/globaldata/soilgrids/> and <https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_01.html> — mapped soil properties, standard depth intervals, and prediction uncertainty; not a substitute for plot measurements.
- USDA-ARS Rosetta implementation: <https://github.com/usda-ars-ussl/rosetta-soil> — candidate PTF/reference for van Genuchten hydraulic parameters; review its model/version, inputs, output interpretation, and uncertainty before integrating.
- FAO AquaCrop: <https://www.fao.org/aquacrop> — an established crop-water/yield model and useful reference for selected crop-water questions; it is not automatically a direct comparator for the current intercropping/root-competition equations.
