# Target System Architecture

## Guiding principle

Use agricultural evidence to define what is known, explicit process models to calculate what follows from assumptions, machine learning where it brings a measurable advantage, and field observations to test whether the system represents reality.

## Layers

1. **Farm context:** location/season, soil profile, crop species/variety and stage, planting geometry, weather, irrigation, labour/economic constraints.
2. **Agricultural knowledge base:** claims, observations, source material, crop/soil/water/pest relationships, management practices, applicability limits and conflicting evidence.
3. **Rules and feasibility constraints:** unit/range checks, eligibility, known safety limits, temporal validity and documented prohibitions.
4. **Simulation primitives:** water balance, soil-layer fluxes, root uptake, crop stress, light/resources when justified, calendar and farm economics. Each primitive needs units, assumptions, invariants, tests and a model/version identifier.
5. **Synthetic scenario factory:** parameter registry, joint sampling, weather/event scenario builder, simulator runner, quality gates, scenario provenance and stable train/test separation.
6. **Prediction models:** task-specific ML models only when there is a documented requirement; record dataset version, metrics, intended domain, calibration and known failure modes.
7. **Decision engine:** compare feasible interventions across objectives (water, yield, profit, labour, risk); report assumptions, uncertainty, evidence quality and trade-offs.
8. **Field feedback:** record recommendation timestamp, action actually taken, delays/deviations, measurement protocol, observed conditions and outcomes.

## Feedback loops

- Field measurements can calibrate parameters and evaluate model behaviour.
- New agricultural evidence can update knowledge claims, but changes should be reviewed/versioned.
- Simulator changes trigger regression testing and, if applicable, regeneration of derived synthetic datasets.
- Model updates must not overwrite past predictions; preserve model and data versions for retrospective evaluation.

## Soil-water primitive: minimum specification

- Define each layer's depth and storage state, moisture definition, lower/upper storage bounds, and units.
- Explicitly define rainfall/infiltration, runoff, evaporation, inter-layer drainage, deep drainage, irrigation and each crop's uptake.
- Calculate stress from a clearly documented state time (e.g. beginning of time step), and report the state convention consistently.
- Allocate shared water across all sinks competing for that storage; independent per-crop caps are insufficient.
- Internal transfer between layers cancels in the whole-profile mass balance.
- Test exact hardpan boundary fixtures, wet/dry limits, storage constraints, stress monotonicity only under explicitly stated preconditions, and complete profile mass-balance residual.
- Do not label the model field-validated merely because its water balance closes.

## ML / surrogate policy

A surrogate is an optional optimization, not an architectural requirement. First profile the reference simulator under the actual decision workload. If a surrogate is evaluated, split by complete scenario/trajectory, report per-output and tail errors, stress-boundary errors, constraint violations, runtime, training/model costs and speedup. Use deterministic physics/state-update code for the constraints the model must obey, and test the composition end to end.
