# DR-002 — Constrained Synthetic-Data Pipeline

**Status:** architecture accepted; implementation and coverage claims require reproducible artifacts.

## 1. Problem and objective

Create reproducible synthetic farm/soil/weather/crop scenarios for software tests, process-model analysis and (only if useful) surrogate training without promoting synthetic assumptions to agricultural evidence.

## 2. Competing proposals

- Naive independent Monte Carlo alone: simple, but may waste samples and break dependencies.
- LLM-generated farming records as facts: rejected as evidence creation.
- Constrained hybrid factory: parameter registry + designed sampler + event/scenario builders + explicit simulator + quality gates + provenance; selected.

## 3. Specialist review

Agricultural: maintain plausible soil, crop and weather conditions. Engineering: ensure reproducibility, coverage, efficiency and measurable purpose. Adversarial: test missing variables, hardpan, deluge, drought, threshold regions, malformed inputs and data leakage.

## 4. Required scenario categories

1. Valid baseline / ordinary conditions.
2. Valid but adverse scenarios (drought, storms, hardpan, waterlogging).
3. Boundary fixtures designed to exercise exact constraints.
4. Invalid-input fixtures, kept separate and expected to be rejected.
5. Real observations reserved for independent evaluation; they are not synthetic.

## 5. Parameter sampling

- Use seeded Latin hypercube or other designed sampling as appropriate, scaled to documented physical bounds.
- Sample correlated or derived soil parameters coherently. For example, a plant-available-water parameterisation may derive field capacity from wilting point and PAW under documented bounds; this does not by itself prove the profile follows a particular hydraulic model.
- Treat topsoil/subsoil conductivity ranges and correlations as evidence-backed only when local/profile data supports them. Use separate exploratory soil-profile families when distributions are unknown.
- Generate weather sequences that preserve relevant temporal dependence or replay observations; also add explicit stress fixtures.
- Do not set a target (e.g. a proportion of positive-runoff rows) and then confuse the stress-enriched design with real-world probabilities.

## 6. Quality gates

G1 schema and units; G2 parameter consistency; G3 temporal consistency; G4 numerical invariants and mass balance; G5 process plausibility against justified bounds/reference cases; G6 provenance/version/seed; G7 separation of scenarios between train/evaluation. Invalid fixtures must not be accepted as valid samples.

## 7. Decision

Build and test this factory before scaling. Do not train a model until the simulator and generator are reproducible and coverage diagnostics are meaningful. Use synthetic data to test code and estimate emulator-to-simulator error, not to establish field truth.

## 8. Open items

Parameter distributions and correlations for local soils/weather remain unestablished. Need source code, logs and scenario-level statistics to determine whether reported coverage repairs truly passed.

## 9. Next experiment

Commit the sampler, parameter registry, scenario definitions, complete simulator, tests and machine-generated coverage report. Verify runoff and aeration families are present in both the intended train coverage and independently designed evaluation set, with denominators stated.
